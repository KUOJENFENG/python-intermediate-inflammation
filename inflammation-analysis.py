#!/usr/bin/env python3
"""Software for managing and analysing patients' inflammation data in our imaginary hospital."""

import argparse
import os

from inflammation import models, views, compute_data
from inflammation.compute_data import JSONDataSource, CSVDataSource, analyse_data


def main(args):
    """The MVC Controller of the patient inflammation data system.

    The Controller is responsible for:
    - selecting the necessary models and views for the current task
    - passing data between models and views
    """
    in_files = args.infiles
    if not isinstance(in_files, list):
        in_files = [args.infiles]

    for filename in in_files:
        _, extension = os.path.splitext(filename)
        if extension == '.json':
            data_source = compute_data.JSONDataSource(os.path.dirname(filename))
        elif extension == '.csv':
            data_source = compute_data.CSVDataSource(os.path.dirname(filename))
        else:
            raise ValueError(f'Unsupported data file format: {extension}')
        compute_data.analyse_data(data_source)

    for filename in in_files:
        inflammation_data = models.load_csv(filename)

        view_data = {'average': models.daily_mean(inflammation_data), 
                     'max': models.daily_max(inflammation_data), 
                     'min': models.daily_min(inflammation_data)}

        views.visualize(view_data)
    
    if args.full_data_analysis:
        _, extension = os.path.splitext(in_files[0])
        if extension == '.json':
            data_source = JSONDataSource(os.path.dirname(in_files[0]))
        elif extension == '.csv':
            data_source = CSVDataSource(os.path.dirname(in_files[0]))
        else:
            raise ValueError(f'Unsupported file format: {extension}')
        data_result = analyse_data(data_source)
        graph_data = {
            'standard deviation by day': data_result,
        }
        views.visualize(graph_data)
        return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='A basic patient inflammation data management system')

    parser.add_argument(
        'infiles',
        nargs='+',
        help='Input CSV(s) containing inflammation series for each patient')
    
    parser.add_argument(
        '--full_data_analysis',
        action='store_true',
        help='Perform a full data analysis, including standard deviation by day visualization')

    args = parser.parse_args()

    main(args)

