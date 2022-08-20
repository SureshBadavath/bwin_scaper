import datetime
import requests
from flask import Flask, jsonify


API_URL = "https://sports.bwin.com/en/sports/api/widget?layoutSize=Large&page=SportLobby&sportId="

SPORTS = {
        "Tennis" : 5, 
        "Basketball" : 7,
        "Football" : 4,
        "Ice Hockey" : 12, 
        "handball": 16
    }

app = Flask(__name__)


def fetch_bwin_schema(data):
    """
    Fetches the schema for the given api response.
    """
    schema  = []
    try:
        for fixture in data['widgets'][1]['payload']['fixtures']:
            fixture_dict = {
                "tournament": fixture['tournament']['name']['value'],
                "eventName": fixture['name']['value'],
                "player1": fixture['participants'][0]['name']['value'],
                "player2": fixture['participants'][1]['name']['value'],
                "player1_odds": fixture['games'][0]['results'][0]['odds'],
                "player2_odds": fixture['games'][0]['results'][1]['odds'],
                "eventDate": fixture['startDate'],
                "lastUpdate": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            schema.append(fixture_dict)
    except KeyError:
        return schema
    return schema
    
def extractor(sport):
    print(sport)
    """
    Extracts the data from the API and returns a JSON object.
    """
    try:
        url = API_URL + str(sport)
        response = requests.get(url, headers={'User-Agent': 'Chrome'})
        status_code = response.status_code
        data = response.json()
        bwin_schema = fetch_bwin_schema(data)
        return bwin_schema, status_code
    except Exception as e:
        return e, 500

@app.route('/sports')
def sports():
    return jsonify(SPORTS)

@app.route('/extract/sport/<sport>')
def extract(sport):
    try:
        data, status_code = extractor(SPORTS[sport])
        if status_code == 403:
            return jsonify({"error": "Forbidden"}), 403
        elif status_code == 404:
            return jsonify({"error": "Not Found"}), 404
        elif status_code == 200:
            return data
    except KeyError:
        return "Sport not found"


if __name__ =='__main__':  
    app.run(debug = True)  
