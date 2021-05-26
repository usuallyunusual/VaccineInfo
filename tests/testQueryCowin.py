import unittest
from unittest.mock import patch
from src.Retriever.CowinRetriever import QueryCowin


class TestQueryCowin(unittest.TestCase):
    """
    Test suite for the class QueryCowin
    """
    url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"

    @patch('src.QueryCowin.requests.get')
    def test_get_json_data_status_ok(self,mocked_request):
        """
        Tests whether method get_json_data works fine if status is OK
        """
        mocked_request.return_value.status_code = 200
        mocked_request.return_value.text = "{}"
        response = QueryCowin("something").get_json_data()
        self.assertEqual({}, response)

    @patch('src.QueryCowin.requests.get')
    def test_get_json_data_status_not_ok(self, mocked_request):
        """
        Tests whether method get_json_data works fine if status is not ok
        """
        mocked_request.return_value.status_code = 403
        mocked_request.return_value.text = "{}"
        response = QueryCowin("something").get_json_data()
        self.assertEqual(-1, response)

    @patch('src.QueryCowin.requests.get')
    def test_get_json_data_bad_response(self, mocked_request):
        """
        Tests whether method get_json_data works fine if there's a bad response
        """
        mocked_request.return_value.status_code = 200
        mocked_request.return_value.text = "{"
        response = QueryCowin("something").get_json_data()
        self.assertEqual(-1, response)
