from unittest.mock import Mock
import sys
import os
import pytest
import math

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from inflammation.compute_data import analyse_data, CSVDataSource


def test_analyse_data_mock_source():
  
  data_source = Mock()
  mock_data = [[[0, 2, 0]],
              [[0, 1, 0]]]
  data_source.load_inflammation_data.return_value = mock_data
  analyse_data(data_source)

import numpy.testing as npt

@pytest.mark.parametrize('data,expected_output', [
    ([[[0, 1, 0], [0, 2, 0]]], [0, 0, 0]),
    ([[[0, 2, 0]], [[0, 1, 0]]], [0, math.sqrt(0.25), 0]),
    ([[[0, 1, 0], [0, 2, 0]], [[0, 1, 0], [0, 2, 0]]], [0, 0, 0])
],
ids=['Two patients in same file', 'Two patients in different files', 'Two identical patients in two different files'])
def test_compute_standard_deviation_by_day(data, expected_output):
    from inflammation.compute_data import compute_standard_deviation_by_day

    result = compute_standard_deviation_by_day(data)
    npt.assert_array_almost_equal(result, expected_output)
