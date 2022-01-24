import requests
import json
from datetime import datetime
from datetime import timedelta
import time
import os


# Rapt API calls
def getToken(username, password):

    url = "https://id.rapt.io/connect/token"

    payload = f'client_id=rapt-user&grant_type=password&username={username}&password={password}'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    result = json.loads(response.text)

    result['expiry_time'] = result.get('expires_in') + time.time()

    return(result)

def getTelemetry(hydrometerId, token):

    #sample Date: 2021-12-20T07:32:46.467Z

    #end date is now
    enddate = datetime.utcnow()
    startdate = enddate - timedelta(hours=1000)


    url = f"https://api.rapt.io/api/Hydrometers/GetTelemetry?hydrometerId={hydrometerId}&startDate={startdate[:-3]}Z&endDate={enddate[:-3]}Z"

    payload = {}
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return json.loads(response.text)

def getHydrometerDetails(hydrometerId, token):
    url = f"https://api.rapt.io/api/Hydrometers/GetHydrometer?hydrometerId={hydrometerId}"

    payload = {}
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return(json.loads(response.text))


#Brewdather API calls
def postBFUpdates(url, hydrodetails, telemetry):
    payload = {
          "name": hydrodetails.get('name', hydrodetails['id']), # Required field, this will be the ID in Brewfather
          "temp": telemetry['temperature'],
          "temp_unit": "C", # C, F, K
          "gravity": telemetry['gravity'],
          "gravity_unit": "G", # G, P
          "battery": telemetry['battery']
        }

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

    print(response.text)

    

hydroKey = os.environ.get('HYDRO_KEY')
RAPT_USER = os.environ.get('RAPT_USER')
RAPT_PW = os.environ.get('RAPT_PW')
BF_PASS = os.environ.get('BF_PASS')
token = json.loads(os.environ.get('TOKEN', ''))

if __name__ == '__main__':
    if time.time() < token.get('expiry_time'):
        token = getToken(RAPT_USER, RAPT_PW)
        os.environ["TOKEN"] = json.dumps(token)

    hydrometerDetails = getHydrometerDetails(hydroKey, token['access_token'])
    data = getTelemetry(hydroKey, token['access_token'])
    postBFUpdates(f'http://log.brewfather.net/stream?id={BF_PASS}',hydrometerDetails, data[-1])
    pass
