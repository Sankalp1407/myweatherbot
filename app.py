from flask import Flask, request, make_response
import os, json
from flask_cors import CORS, cross_origin
from weather_data import WeatherData

app = Flask(__name__)
CORS(app)

weather_obj = WeatherData()   # ✅ create globally

@app.route('/')
def index():
    return 'Web App with Python Flask!'

@app.route('/webhook', methods=['POST'])
@cross_origin()
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=2))

    res = weather_obj.processRequest(req)   # ✅ fixed

    res = json.dumps(res)
    print(res)

    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)