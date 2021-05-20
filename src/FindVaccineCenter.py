import json
from datetime import datetime, date

import requests


class FindVaccineCenter:
    """
    Queries the Cowin API to get required data
    """

    def __init__(self, district_id, vaccine):
        self.district_id = district_id
        self.vaccine = vaccine

    def get_json_data(self):
        """
        Queries the Cowin API and returns the JSON response.
        Everything to do with the request params and exception catching is done here
        :return:
        """
        try:
            response = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict",
                                    params={"district_id": self.district_id,
                                            "date": date.today().strftime("%d-%m-%Y")},
                                    headers={'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) "
                                                           "AppleWebKit/537.36 (KHTML, "
                                                           "like Gecko) Chrome/39.0.2171.95 Safari/537.36"})
            if response.status_code != 200:
                raise Exception("Bad Response code: ", response.status_code)
            return json.loads(response.text)
        except Exception as e:
            print(f" Exception: {datetime.now()} : {e}")
            return -1

    def filter_results(self, response):
        """
        Filters the response object by vaccine type, availability etc
        :param response:
        :return:
        """
        filtered_responses = []
        for center in response["centers"]:
            for session in center["sessions"]:
                filtered_center = {"center_id": center["center_id"], "name": center["name"],
                                   "address": center["address"], "state_name": center["state_name"],
                                   "district_name": center["district_name"], "block_name": center["block_name"],
                                   "pincode": center["pincode"], "lat": center["lat"], "long": center["long"],
                                   "from": center["from"], "to": center["to"], "fee_type": center["fee_type"]}
                if center["fee_type"] == "Paid":
                    if center.get("vaccine_fees", False):
                        fee = ""
                        for key in center["vaccine_fees"][0]:
                            fee += f"{key.title()} : {center['vaccine_fees'][0][key]}\n "
                        filtered_center["fee_type"] = fee
                filtered_sessions = []
                if session["available_capacity"] == 0 or session["vaccine"] != self.vaccine:
                    continue
                filtered_sessions.append(session)
            if len(filtered_sessions) != 0:
                filtered_center["sessions"] = filtered_sessions
                filtered_responses.append(filtered_center)
        if len(filtered_responses) == 0:
            filtered_responses.append({"No centers available ": "("})
        filtered_responses = {"centers": filtered_responses}
        return filtered_responses

    def get_data(self):
        """
        The main interface used by external entities, Calls the other methods in class
        filters the results and returns a json object of filtered results
        :return: Dict (JSON obj) of filtered responses
        """
        raw_json_data = self.get_json_data()
        if raw_json_data != -1:
            filtered_response = self.filter_results(raw_json_data)
            return json.dumps(filtered_response, indent=2)
        else:
            return -1
