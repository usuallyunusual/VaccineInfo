from datetime import date, timedelta

from src.Filter.BaseFilterEntityStats import BaseFilterEntityStats
from src.Logging import Logging


class FilterVaccineStats(BaseFilterEntityStats):
    """
    Class provides methods to get data about the number of vaccines administered
    """

    def __init__(self, state, entity_df):
        """
        State (str) to filter information from the json response.
        """
        super().__init__(state, entity_df)
        self.logger = Logging().get_logger()

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
