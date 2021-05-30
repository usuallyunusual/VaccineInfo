import json
from abc import abstractmethod
from src.Logging import Logging


class BaseFilterEntityStats:
    """
    Provides methods to calculate delta values and query current case load of Covid in India
    """
    populations = {"Karnataka": 65798000, "India": 1370000000}

    def __init__(self, state, entity_df):
        """
        State (str) to filter to case reponse by.
        """
        self.logger = Logging().get_logger()
        self.state = state
        self.entity_df = entity_df

    @abstractmethod
    def filter_state(self, dataframe, state):
        """
        Filters the dataframe for the given state and uses the latest info
        :param state: State to be filtered by
        :param dataframe:
        :return: Filtered dataframe
        """
        pass

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
            [diff, per_diff, tot_percentage] = self.get_diff_and_percentage(int(datalist[0].iloc[i]),
                                                                            int(datalist[1].iloc[i]),
                                                                            state)
            data[col[0]] = {"value": int(datalist[0].iloc[i]), "change": diff, "change_per": per_diff,
                            "tot_percentage": tot_percentage}
        return data

    def get_entity_stats(self):
        """
        Interface to external classes. Calls all internal classes and returns required metrics
        :return: JSON obj with required metrics
        """
        final_response = {}
        filtered_dataframe = self.filter_state(self.entity_df, self.state)
        final_response[self.state] = self.get_stats(filtered_dataframe, self.state)
        filtered_dataframe = self.filter_state(self.entity_df, "India")
        final_response["India"] = self.get_stats(filtered_dataframe, "India")
        return json.dumps(final_response, indent=2)
