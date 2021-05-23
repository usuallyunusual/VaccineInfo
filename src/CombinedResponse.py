import json

from FindVaccineCenter import FindVaccineCenter
from VaccineStats import VaccineStats
from CaseStats import CaseStats
import os


class CombinedResponse:
    """
    Class to combine the responses of two different API calls.
    Used to pass info to the presentation logic
    """

    def __init__(self, raw_json_data, vaccine, state):
        self.raw_json_data = raw_json_data
        self.vaccine = vaccine
        self.state = state

    def get_combined_response(self):
        """
        Combines the responses
        :return: JSON obj of combines response
        """
        [vaccine_centers, vaccine_stats, case_stats] = self.get_individual_responses()
        vaccine_centers["Vaccine_Stats"] = vaccine_stats
        vaccine_centers["Case_Stats"] = case_stats
        return json.dumps(vaccine_centers, indent=2)

    def get_findvaccinecenter_obj(self, raw_json_data, vaccine):
        """
        Returns obj of findVaccineCenter class with parameters supplied
        :return: FindVaccineCenter object
        """
        return FindVaccineCenter(raw_json_data, vaccine)

    def get_vaccinestats_obj(self, state):
        """
        Returns obj of VaccineStats class with parameters supplied
        :return: VaccineStats object
        """
        return VaccineStats(state)

    def get_casestats_obj(self, state):
        """
        Returns obj of CaseStats class with parameters supplied
        :return: VaccineStats object
        """
        return CaseStats(state)

    def get_individual_responses(self):
        """
        Calls different API's through interfaces and returns the individual responses
        :return: returns Individual responses
        """
        findvaccinecenter = self.get_findvaccinecenter_obj(self.raw_json_data, self.vaccine)
        centers = findvaccinecenter.get_data()
        if centers == -1:
            return centers
        centers = json.loads(centers)
        vaccinestats = self.get_vaccinestats_obj(self.state)
        vac_stats = vaccinestats.get_vaccine_stats()
        vac_stats = json.loads(vac_stats)
        casestatsobj = self.get_casestats_obj(self.state)
        case_stats = casestatsobj.get_case_stats()
        case_stats = json.loads(case_stats)
        return [centers, vac_stats, case_stats]
