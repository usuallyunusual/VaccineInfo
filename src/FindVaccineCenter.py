import json
import os


class FindVaccineCenter:
    """
    Queries the Cowin API to get required data
    """

    def __init__(self, raw_json_data, vaccine):
        self.raw_json_data = raw_json_data
        self.vaccine = vaccine

    def tag_updated(self, data):
        """
        Checks if last query gave same results and tags it "updates":yes or "updated":no
        :param data: The queried data from API
        :return:
        """
        last_call_file = os.path.dirname(os.path.realpath(__file__)) + "/last_call_" + self.vaccine.lower() + ".txt"
        try:
            with open(last_call_file, 'r') as last_call_data:
                prev_data = json.loads(last_call_data.read())
            if prev_data == data:
                data["updated"] = False
            else:
                with open(last_call_file, "w") as last_call_data:
                    last_call_data.write(json.dumps(data, indent=2))
                    data["updated"] = True
            return data
        except Exception as e:
            with open(last_call_file, "w") as last_call_data:
                last_call_data.write(json.dumps(data, indent=2))
                data["updated"] = True
                return data

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
        if self.raw_json_data != -1:
            filtered_response = self.filter_results(self.raw_json_data)
            tagged_response = self.tag_updated(filtered_response)
            return json.dumps(tagged_response, indent=2)
        else:
            return -1
