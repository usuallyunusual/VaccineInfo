from CombinedResponse import CombinedResponse
from src.Emailer import Emailer


class Driver:
    """
    Co-odrinates between everything
    """

    def __init__(self):
        pass

    def run(self):
        """
        Calls everything. Execution starts here
        :return: -1 or 1
        """
        responsecombiner = CombinedResponse("294", "covaxin", "Karnataka")
        combined_data = responsecombiner.get_combined_response()
        Emailer(combined_data, "COVAXIN").send_vaccine_info()


if __name__ == "__main__":
    Driver().run()
