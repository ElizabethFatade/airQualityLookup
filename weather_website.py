from flask import Flask, render_template, url_for
from flask import request, redirect
import requests, zipcodes
import json

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')  #this is used to basically generate the home page with the / symbol

@app.route("/", methods=["GET", "POST"])    #on the home page when a zip code is entered the aqinfo function is called and template rendered
def aqinfo():
    if request.method == "POST":
        zip_code = request.form["zipc"]

        if zipcodes.is_real(zip_code):
            try:
                api_request = requests.get("https://www.airnowapi.org/aq/forecast/zipCode/?format=application/json&zipCode=" + zip_code +
                                           "&date=2021-01-10&distance=25&API_KEY=46ADD3D7-4BE7-45EB-8D83-C4ED39DC131C")
                api = json.loads(api_request.content)
                city = api[0]['ReportingArea']
                quality = api[0]['AQI']
                category = api[0]['Category']['Name']
                latitude = api[0]['Latitude']
                longitude = api[0]['Longitude']

                description = get_quality(category)

                return render_template("aqinfo.html", description=description, city=city, quality=quality, category=category, latitude=latitude, longitude=longitude)
            except Exception as e:
                return redirect(url_for("error"))
        else:
            return redirect(url_for("error"))
    else:
        return render_template('home.html')

@app.route("/errorfound", methods=["GET", "POST"])
def error():
    return render_template("error.html")

def get_quality(quality):

    if quality == "Good":
        description = "Air quality is satisfactory, and air pollution poses little or no risk."

    elif quality == "Moderate":
        description = "Air quality is acceptable. However, there may be a risk for some people, " \
                      "particularly those who are unusually sensitive to air pollution."

    elif quality == "Unhealthy for Sensitive Groups":
        description = "Members of sensitive groups may experience health effects. The general public is less likely to be affected."

    elif quality == "Unhealthy":
        description = "Some members of the general public may experience health effects; members of " \
        "sensitive groups may experience more serious health effects."

    elif quality == "Very Unhealthy":
        description = "Health alert: The risk of health effects is increased for everyone."

    else:
        description = "Health warning of emergency conditions: everyone is more likely to be affected."

    return description
if __name__ == '__main__':  # sets up the page to only be debugging
    app.run(debug=True)

