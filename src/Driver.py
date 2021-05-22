import yaml

from CombinedResponse import CombinedResponse
from Emailer import Emailer
import os
from QueryCowin import QueryCowin

class Driver:
    """
    Co-ordinates between everything
    """

    def __init__(self):
        pass

    def run(self):
        """
        Calls everything. Execution starts here
        :return: -1 or 1
        """
        raw_json_data = QueryCowin("294").get_json_data()
        receiver_config = self.get_receivers_configs()
        for vaccine in receiver_config:
            responsecombiner = CombinedResponse(raw_json_data, vaccine, "Karnataka")
            combined_data = responsecombiner.get_combined_response()
            Emailer(combined_data, vaccine, receiver_config[vaccine]).send_vaccine_info()

    def get_script_path(self):
        """
        Returns the current script path
        """
        return os.path.dirname(os.path.realpath(__file__))

    def get_receivers_configs(self):
        """
        Reads the reciever emails along with their configs
        """
        with open(self.get_script_path() + "/receiver_config.yaml") as receiver_config:
            return yaml.load(receiver_config.read(), Loader=yaml.FullLoader)



if __name__ == "__main__":
    Driver().run()
