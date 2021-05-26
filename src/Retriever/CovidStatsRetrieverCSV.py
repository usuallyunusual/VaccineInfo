from io import StringIO

import requests
import pandas as pd
from src.Logging import Logging


class CovidCaseStatsRetriever:
    """
    Queries the Covid19.org API for statewise case stats or statewise vaccine stats depending on the url
    """

    base_url = "http://api.covid19india.org/csv/latest"

    def __init__(self, data):
        """
        Gets the data parameter used to decide the query endpoint
        """
        self.data = data
        self.logger = Logging().get_logger()

    def query_api(self):
        """
        Queries the API and returns the CSV file
        :return: Returns a pandas dataframe
        """
        try:
            url = self.get_query_url()
            data = requests.get(url)
            self.logger.debug(f"Queried {url} with response code : {data.status_code}")
            if data.status_code != 200:
                raise Exception("Bas status code", data.status_code)
            dataframe = pd.read_csv(StringIO(data.text))
            return dataframe
        except Exception as e:
            self.logger.error(f"Error occurred : {e}")
            return -1

    def get_query_url(self):
        """
        Returns the url based on the data parameter
        """
        if self.data.lower() is "vaccine":
            return f"{self.base_url}/cowin_vaccine_data_statewise.csv"
        else:
            return f"{self.base_url}/states.csv"
