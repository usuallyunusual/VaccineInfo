import unittest
from io import StringIO
from unittest.mock import patch, Mock
from src.Retriever.CovidStatsRetrieverCSV import CovidCaseStatsRetriever
from tests.Retriever.RetrieverTestResources import RetrieverTestResources
import pandas as pd

class TestCovidStatsRetriever(unittest.TestCase):
    """
    Test suite for the class CovidStatsRetriever
    """

    @patch('src.Retriever.CowinRetriever.requests.get')
    def test_query_api_status_ok(self, mocked_request):
        """
        Tests whether method query_api works fine if status is OK
        """
        test_csv = "test,result,mocked,csv,file"
        mocked_request.return_value.status_code = 200
        mocked_request.return_value.text = test_csv
        response = CovidCaseStatsRetriever("something").query_api()
        dataframe = pd.read_csv(StringIO(test_csv))
        self.assertTrue(dataframe.equals(response))
        Mock.assert_called_with(mocked_request, RetrieverTestResources.covid_url_cases)

    @patch('src.Retriever.CowinRetriever.requests.get')
    def test_query_api_status_not_ok(self, mocked_request):
        """
        Tests whether method query_api works fine if status is not ok
        """
        mocked_request.return_value.status_code = 403
        mocked_request.return_value.text = "{}"
        response = CovidCaseStatsRetriever("vaccine").query_api()
        self.assertEqual(-1, response)
        Mock.assert_called_with(mocked_request, RetrieverTestResources.covid_url_vaccine)

    def test_get_query_url(self):
        """
        Tests whether method query url gives the right url's
        """
        url = CovidCaseStatsRetriever("something").get_query_url()
        self.assertEqual(RetrieverTestResources.covid_url_cases,url)

        url = CovidCaseStatsRetriever("vaccine").get_query_url()
        self.assertEqual(RetrieverTestResources.covid_url_vaccine,url)

        url = CovidCaseStatsRetriever("VaCcIne").get_query_url()
        self.assertEqual(RetrieverTestResources.covid_url_vaccine, url)
