from datetime import datetime, date
import requests
import json
from Logging import Logging


class QueryCowin:
    """
    Class provides methods to query Cowin endpoint and return Json data
    """

    def __init__(self, district_id):
        """
        Gets district id as parameter
        """
        self.logger = Logging().get_logger()
        self.district_id = district_id

    def get_json_data(self):
        """
        Queries the Cowin API and returns the JSON response.
        Everything to do with the request params and exception catching is done here
        :return: JSON obj
        """
        try:
            url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
            response = requests.get(url,
                                    params={"district_id": self.district_id,
                                            "date": date.today().strftime("%d-%m-%Y")},
                                    headers={'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) "
                                                           "AppleWebKit/537.36 (KHTML, "
                                                           "like Gecko) Chrome/39.0.2171.95 Safari/537.36"})
            self.logger.debug(f"Queried : {url} with params district_id = "
                              f"{self.district_id} date = {date.today().strftime('%d-%m-%Y')}"
                              f"with response code : {response.status_code}")

            if response.status_code != 200:
                self.logger.debug(f"Response Code : {response.status_code}")
                raise Exception("Bad Response code: ", response.status_code)
            return json.loads(response.text)
        except Exception as e:
            self.logger.error(f" Exception: {datetime.now()} : {e}")
            return -1
