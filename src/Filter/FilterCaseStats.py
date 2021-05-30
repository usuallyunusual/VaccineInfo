from datetime import date, timedelta
from src.Logging import Logging
from src.Filter.BaseFilterEntityStats import BaseFilterEntityStats


class FilterCaseStats(BaseFilterEntityStats):
    """
    Provides methods to calculate delta values and query current case load of Covid in India
    """

    def __init__(self, state, entity_df):
        """
        State (str) to filter to case reponse by.
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
            dataframe_filtered = dataframe[dataframe["Date"] == dates.strftime("%Y-%m-%d")]
            dataframe_filtered = dataframe_filtered[
                ["Confirmed", "Recovered", "Deceased",
                 "Other"]]
            dataframe_filtered = dataframe_filtered.fillna(0)
            dataframe_filtered["Active"] = dataframe_filtered["Confirmed"] - (
                    dataframe_filtered["Recovered"] + dataframe_filtered["Deceased"] + dataframe_filtered["Other"])
            dataframe_filtered = dataframe_filtered.iloc[-1]
            data.append(dataframe_filtered)
        return data
