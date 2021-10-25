import os
import requests
from twilio.rest import Client
import env_variables


HOURS_TO_CHECK = 12  # For how many hours to check for rain (MAX 47)
YOUR_PHONE_NUMBER = ""  # Give phone number to get SMS on
YOUR_LATITUDE = 0.000000
YOUR_LONGITUDE = 0.000000

# Get high valuable enviroment variables
env_variables.set_enviroment()

# APIs setting
account_sid = "ACd733f8492a4756ba569894fb13b89c79"
auth_token = os.environ.get("AUTHORISATION_TOKEN")
api_key = os.environ.get("WEATHER_API_KEY")
weather_webside_endpoint = "https://api.openweathermap.org/data/2.5/onecall"
api_parameters = {
    "lat": YOUR_LATITUDE,
    "lon": YOUR_LONGITUDE,
    "appid": api_key,
    "exclude": "current,minutely,daily",
}

# Request API with weather data
weather_data = requests.get(url=weather_webside_endpoint, params=api_parameters)
weather_data.raise_for_status()
json_weather_data = weather_data.json()

# Checking a number of hours gived in "HOURS_TO_CHECK" variable for rain
will_rain_in_couple_hours = []
for hour in range(0, HOURS_TO_CHECK):
    if json_weather_data["hourly"][hour]["weather"][0]["id"] < 700:
        will_rain_in_couple_hours.append(True)
    else:
        will_rain_in_couple_hours.append(False)

# Sending SMS to a number gived in "YOUR_PHONE_NUMBER" variable if rain is detected
if any(will_rain_in_couple_hours):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body="It will rain today. Remember to bring your umbrella! ☂️",
        from_="+13192846432",
        to=YOUR_PHONE_NUMBER,
    )
    print(message.status)
