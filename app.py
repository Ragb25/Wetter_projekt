from flask import request
from markupsafe import escape
from flask import Flask 
from api import getInfo, wetter_daten, vorhersage 
from flask import render_template




app = Flask(__name__)
@app.route("/")
def welcome_page():
    return render_template("welcome_page.html")

@app.route("/wetter")
def wetter():
    stadt = request.args.get("ville")
    lon, lat = getInfo(stadt)
    daten = wetter_daten(lon, lat)
    vorher = vorhersage(lon, lat)
    return f"""Stadt: {escape(stadt)} <br>
    Daten: {escape(daten)} <br>
    vorhersagen: {escape(vorher)} </p>"""
