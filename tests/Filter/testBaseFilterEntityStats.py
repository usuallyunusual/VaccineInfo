from io import StringIO
from unittest import TestCase
import pandas as pd

from src.Filter.BaseFilterEntityStats import BaseFilterEntityStats


class TestBaseFilterEntityStats(TestCase):
    """
    Tests the BaseFilterEntityStats class
    """
    test_csv = "test,result,mocked,csv,file"
    dataframe = pd.read_csv(StringIO(test_csv))

    def test_get_diff_and_percentage(self):
        """
        Tests the get_diff and percentage function
        """
        [diff, per_diff, tot_diff] = BaseFilterEntityStats("Karnataka", self.dataframe).get_diff_and_percentage(200,
                                                                                                                100,
                                                                                                                "Karnataka")
        self.assertAlmostEqual(100.0, diff, delta=0.01)
        self.assertAlmostEqual(100.0, per_diff, delta=0.01)
        self.assertAlmostEqual(0.0003, tot_diff, delta=0.00001)

    def test_get_stats(self):
        """
        Tests if the get_stats_method returns the right data
        """
        expected_result = {0: {'change': 100,
                              'change_per': 100.0,
                              'tot_percentage': 0.000303960606705371,
                              'value': 200},
                          1: {'change': 100,
                              'change_per': 50.0,
                              'tot_percentage': 0.00045594091005805653,
                              'value': 300},
                          2: {'change': 100,
                              'change_per': 33.33333333333333,
                              'tot_percentage': 0.000607921213410742,
                              'value': 400},
                          3: {'change': 100,
                              'change_per': 25.0,
                              'tot_percentage': 0.0007599015167634274,
                              'value': 500}}
        my_csv = list()
        my_csv.append("200,300,400,500")
        my_csv.append("100,200,300,400")
        datalist = list()
        for csv in my_csv:
            datalist.append(pd.read_csv(StringIO(csv),header=None).iloc[0])
        data = BaseFilterEntityStats("Karnataka", self.dataframe).get_stats(datalist, "Karnataka")
        self.assertEqual(expected_result, data)
