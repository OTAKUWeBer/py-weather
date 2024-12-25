from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Flag and capital
def search_flag(country):
    flag_api = f"https://restcountries.com/v3.1/name/{country}"
    response = requests.get(flag_api)
    
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        if data:
            # Get the first flag URL and capital from the first country object
            flag_url = data[0]["flags"]["png"]
            capital = data[0]["capital"][0]
            
            weather_info = find_weather(capital)
            return flag_url, weather_info
        else:
            weather_info = find_weather(country)
            return None, weather_info
    else:
        weather_info = find_weather(country)
        return "No flag found", weather_info

# Weather
def find_weather(capital):
    key = "f9dba07a661b78ba12c4155e9055588a"
    weather_api = f"https://api.openweathermap.org/data/2.5/weather?q={capital}&appid={key}&units=metric"
    response = requests.get(weather_api)

    if response.status_code == 200:
        data = response.json()
        city = data.get("name")
        temperature = data["main"]["temp"]
        weather = data["weather"][0]["description"]
        wind_speed = data["wind"]["speed"]
        cloudiness = data["clouds"]["all"]

        return {
            "city": city,
            "temperature": f"{temperature:.2f}°C",
            "condition": weather.capitalize(),
            "wind_speed": wind_speed,
            "cloudiness": cloudiness
        }
    else:
        return "No information found"

@app.route("/", methods=["GET", "POST"])
def index():
    weather_info = None
    error = None

    if request.method == "POST":
        country = request.form["country"]
        flag_url, weather_info = search_flag(country)
        
        if flag_url:
            return render_template("index.html", flag_url=flag_url, weather_info=weather_info)
        else:
            error = weather_info
            return render_template("index.html", error=error, weather_info=weather_info)

    return render_template("index.html", weather_info=weather_info, error=error)

if __name__ == "__main__":
    app.run(debug=True)
