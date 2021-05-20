import json
from datetime import date, timedelta
from io import StringIO

import pandas as pd
import requests


class VaccineStats:
    """
    Class provides methods to get data about the number of vaccines administered
    """
    populations = {"Karnataka": 65798000, "India": 1370000000}

    def __init__(self, state):
        self.state = state

    def query_api(self):
        """
        Queries the API and returns the CSV file
        :return: Returns a pandas dataframe
        """
        try:
            data = requests.get("http://api.covid19india.org/csv/latest/cowin_vaccine_data_statewise.csv")
            if data.status_code != 200:
                raise Exception("Bas status code", data.status_code)
            dataframe = pd.read_csv(StringIO(data.text))
            return dataframe
        except Exception as e:
            print(e)

    def filter_state(self, dataframe, state):
        """
        Filters the dataframe for the given state and uses the latest info
        :param state: State to be filtered by
        :param dataframe:
        :return: Filtered dataframe
        """
        dataframe = dataframe[dataframe["State"] == state]
        today = date.today()
        yesterday = today - timedelta(days=1)
        daybefore = yesterday - timedelta(days=1)
        data = []
        for dates in [yesterday, daybefore]:
            dataframe_filtered = dataframe[dataframe["Updated On"] == dates.strftime("%d/%m/%Y")]
            dataframe_filtered = dataframe_filtered[
                ["First Dose Administered", "Second Dose Administered", "Total Covaxin Administered",
                 "Total CoviShield Administered", "Total Doses Administered"]]
            dataframe_filtered = dataframe_filtered.fillna(0)
            dataframe_filtered = dataframe_filtered.iloc[-1]
            data.append(dataframe_filtered)
        return data

    def get_diff_and_percentage(self, first, second, state):
        """
        Returns the differnce value and the percentage difference between two numbers and percentage compared to entire population
        :param state: The atate to get population of
        :param first: Number
        :param second: Number
        :return: List of difference and percentage difference
        """
        difference = first - second
        per_difference = (difference / second) * 100
        total_percentage = (first / self.populations[state]) * 100
        return [difference, per_difference, total_percentage]

    def get_stats(self, datalist, state):
        """
        Returns a json object with important stats using the data of two days
        1. Change in one day
        2. Percetnage change
        3. Overall percentage vaccinated
        :param state: State to use population of
        :param datalist: The list containing yesterdays and daybefores vaccine data
        :return: json object containing original data tagged with stats
        """
        data = {}
        for i, col in zip(range(5), datalist[0].items()):
            [diff, per_diff, tot_percentage] = self.get_diff_and_percentage(datalist[0].iloc[i], datalist[1].iloc[i],
                                                                            state)
            data[col[0]] = {"value": datalist[0].iloc[i], "change": diff, "change_per": per_diff,
                            "tot_percentage": tot_percentage}
        return data

    def get_vaccine_stats(self):
        """
        Interface to external classes. Calls all internal classes and returns required metrics
        :return: JSON obj with required metrics
        """
        final_response = {}
        dataframe = self.query_api()
        filtered_dataframe = self.filter_state(dataframe, self.state)
        final_response[self.state] = self.get_stats(filtered_dataframe, self.state)
        filtered_dataframe = self.filter_state(dataframe, "India")
        final_response["India"] = self.get_stats(filtered_dataframe, "India")
        return json.dumps(final_response, indent=2)
