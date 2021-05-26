import unittest
from unittest.mock import patch, Mock
from src.Retriever.CowinRetriever import CowinRetriever
from tests.Retriever.RetrieverTestResources import RetrieverTestResources


class TestCowinRetriever(unittest.TestCase):
    """
    Test suite for the class CowinRetriever
    """

    @patch('src.Retriever.CowinRetriever.requests.get')
    def test_get_json_data_status_ok(self, mocked_request):
        """
        Tests whether method get_json_data works fine if status is OK
        """
        mocked_request.return_value.status_code = 200
        mocked_request.return_value.text = "{}"
        response = CowinRetriever("something").get_json_data()
        self.assertEqual({}, response)
        Mock.assert_called_with(mocked_request, RetrieverTestResources.cowin_url,
                                headers=RetrieverTestResources.headers,
                                params=RetrieverTestResources.params)

    @patch('src.Retriever.CowinRetriever.requests.get')
    def test_get_json_data_status_not_ok(self, mocked_request):
        """
        Tests whether method get_json_data works fine if status is not ok
        """
        mocked_request.return_value.status_code = 403
        mocked_request.return_value.text = "{}"
        response = CowinRetriever("something").get_json_data()
        self.assertEqual(-1, response)
        Mock.assert_called_with(mocked_request, RetrieverTestResources.cowin_url,
                                headers=RetrieverTestResources.headers,
                                params=RetrieverTestResources.params)

    @patch('src.Retriever.CowinRetriever.requests.get')
    def test_get_json_data_bad_response(self, mocked_request):
        """
        Tests whether method get_json_data works fine if there's a bad response
        """
        mocked_request.return_value.status_code = 200
        mocked_request.return_value.text = "{"
        response = CowinRetriever("something").get_json_data()
        self.assertEqual(-1, response)
        Mock.assert_called_with(mocked_request, RetrieverTestResources.cowin_url,
                                headers=RetrieverTestResources.headers,
                                params=RetrieverTestResources.params)
