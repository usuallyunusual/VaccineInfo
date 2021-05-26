import json

from src.Filter.FilterVaccineCenter import FindVaccineCenter
from src.Filter.FilterVaccineStats import VaccineStats
from src.Filter.FilterCaseStats import CaseStats
from Logging import Logging


class CombinedResponse:
    """
    Class to combine the responses of two different API calls.
    Used to pass info to the presentation logic
    """

    def __init__(self, raw_json_data, vaccine, state):
        """
        The raw json data to send for filtering, the vaccine to filter by and the state to filter by
        TODO : Move this
        to Driver class. That should handle all configurations. THis should only receiver configured classes
        """
        self.logger = Logging().get_logger()
        self.raw_json_data = raw_json_data
        self.vaccine = vaccine
        self.state = state

    def get_combined_response(self):
        """
        Combines the responses
        :return: JSON obj of combines response
        """
        [vaccine_centers, vaccine_stats, case_stats] = self.get_individual_responses()
        self.logger.debug("Received all of the individual responses")
        vaccine_centers["Vaccine_Stats"] = vaccine_stats
        vaccine_centers["Case_Stats"] = case_stats
        return json.dumps(vaccine_centers, indent=2)

    def get_individual_responses(self):
        """
        Calls different API's through interfaces and returns the individual responses
        :return: returns Individual responses
        """
        centers = self.filtervaccinecenter.get_filtered_data()
        if centers == -1:
            return centers
        centers = json.loads(centers)
        vac_stats = self.vaccinestats.get_vaccine_stats()
        vac_stats = json.loads(vac_stats)
        case_stats = self.casestatsobj.get_case_stats()
        case_stats = json.loads(case_stats)
        return [centers, vac_stats, case_stats]
