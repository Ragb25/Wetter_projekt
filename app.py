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
    lon, lat, address = getInfo(stadt)
    today_wetter = wetter_daten(lon, lat)
    vorhersage_wetter = vorhersage(lon, lat)

    #Stadtname, Land, Region und postalcode mitnehmen.
    i=1
    for j in address:
        if i == 1:
            info_1 = address[j]
            i += 1
        elif i == 2:
            info_2 = address[j]
            i += 1
        elif i == 3:
            info_3 = address[j]
            i += 1
        if j == "country":
            info_4 = address[j]
            break
    
        




    return render_template(
        "wetter_page.html",
        stadt_name = info_1,
        region = info_2,
        land = info_4,
        info_random = info_3,
    )
