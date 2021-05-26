from datetime import date


class RetrieverTestResources:
    cowin_url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict'
    covid_url_vaccine = "http://api.covid19india.org/csv/latest/cowin_vaccine_data_statewise.csv"
    covid_url_cases = "http://api.covid19india.org/csv/latest/states.csv"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 '
                             'Safari/537.36'}
    params = {'district_id': 'something', 'date': date.today().strftime("%d-%m-%Y")}