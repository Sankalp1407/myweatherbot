from app_logger import logger
from app_exception.exception import AppException
from pyowm.owm import OWM
import sys


class WeatherData:
    def __init__(self):
        self.owmapikey = '14ec6eeebb63aeeb793591ced4eb6bf5'
        self.owm = OWM(self.owmapikey)
        self.mgr = self.owm.weather_manager()

    def processRequest(self, req):
        try:
            result = req.get("queryResult", {})
            parameters = result.get("parameters", {})
            city = parameters.get("city_name")

            if not city:
                return {
                    "fulfillmentText": "City not found in request"
                }

            observation = self.mgr.weather_at_place(city)
            weather = observation.weather

            wind_speed = weather.wind().get("speed")
            humidity = weather.humidity
            temp = weather.temperature("celsius")

            speech = (
                f"Weather in {city}: "
                f"Humidity {humidity}, "
                f"Wind Speed {wind_speed}, "
                f"Min Temp {temp.get('temp_min')}, "
                f"Max Temp {temp.get('temp_max')}"
            )

            return {
                "fulfillmentText": speech,
                "displayText": speech
            }

        except Exception as e:
            raise AppException(e, sys)