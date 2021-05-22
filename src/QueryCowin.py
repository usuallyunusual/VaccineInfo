from datetime import datetime, date
import requests
import json


class QueryCowin():
    """
    Class provides methods to query Cowin endpoint and return Json data
    """
    def __init__(self,district_id):
        """
        Gets district id as parameter
        """
        self.district_id = district_id

    def get_json_data(self):
        """
        Queries the Cowin API and returns the JSON response.
        Everything to do with the request params and exception catching is done here
        :return: JSON obj
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
