import yaml
from src.Combiner.CombinedResponse import CombinedResponse
from Emailer import Emailer
import os
from src.Retriever.CowinRetriever import CowinRetriever
import argparse
from src.Logging import Logging
import time
from src.Retriever.CovidStatsRetrieverCSV import CovidCaseStatsRetriever
from src.Filter.FilterVaccineCenter import FilterVaccineCenter
from src.Filter.FilterCaseStats import FilterCaseStats
from src.Filter.FilterVaccineStats import FilterVaccineStats


class Driver:
    """
    Co-ordinates between everything
    """

    def __init__(self):
        self.logger = Logging().get_logger()

    def get_query_cowin(self, district_id):
        """
        Getter method to instantiate an object of QueryCowin class and return this new object
        """
        return CowinRetriever(district_id)

    def get_filtervaccinecenter_obj(self, raw_json_data, vaccine):
        """
        Returns obj of findVaccineCenter class with parameters supplied
        :return: FindVaccineCenter object
        """
        return FilterVaccineCenter(raw_json_data, vaccine)

    def get_filtervaccinestats_obj(self, state):
        """
        Returns obj of VaccineStats class with parameters supplied
        :return: VaccineStats object
        """
        return FilterVaccineStats(state)

    def get_filtercasestats_obj(self, state):
        """
        Returns obj of CaseStats class with parameters supplied
        :return: VaccineStats object
        """
        return FilterCaseStats(state)

    def run(self, force_send):
        """
        Calls everything. Execution starts here
        :return: -1 or 1 (supposed to)
        """
        self.state = "Karnataka"
        self.logger.debug(f"Force-send flag is {force_send}")
        query_cowin_obj = self.get_query_cowin("294")
        raw_json_data = query_cowin_obj.get_json_data()
        vaccine_df = self.get_filtervaccinestats_obj(self.state)
        cases_df = self.get_filtercasestats_obj(self.state)
        if raw_json_data == -1:
            return -1
        receiver_config = self.get_receivers_configs()
        if receiver_config == -1:
            return -1
        for vaccine in receiver_config:
            self.logger.debug(f"Vaccine : {vaccine.upper()}")
            responsecombiner = CombinedResponse(raw_json_data, vaccine, "Karnataka")
            combined_data = responsecombiner.get_combined_response()
            Emailer(combined_data, vaccine, receiver_config[vaccine], force_send).send_vaccine_info()

    def get_script_path(self):
        """
        Returns the current script path
        """
        return os.path.dirname(os.path.realpath(__file__))

    def get_receivers_configs(self):
        """
        Reads the receiver emails along with their configs
        """
        try:
            with open(self.get_script_path() + "/receiver_config.yaml") as receiver_config:
                self.logger.debug("Reading Receiver config")
                return yaml.load(receiver_config.read(), Loader=yaml.FullLoader)
        except Exception as e:
            self.logger.error(f"Error occurred : {e}")
            return -1


if __name__ == "__main__":
    # TODO : Update the description
    parser = argparse.ArgumentParser(description='Send email to an email list')
    parser.add_argument('-f', '--force-send', help="Force send the email irrespective of the same API response",
                        action='store_true')
    args = parser.parse_args()
    if args.force_send:
        Driver().run(True)
    else:
        print("Process is going to keep running. Press CTRL + C to quit")
        while True:
            Driver().run(False)
            time.sleep(180)
