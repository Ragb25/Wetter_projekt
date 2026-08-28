from flask import request
from markupsafe import escape
from flask import Flask 
from api import getInfo, wetter_daten, vorhersage, daten_organisation 
from flask import render_template




app = Flask(__name__)
@app.route("/")
def welcome_page():
# Wert von Hannover für das Welcome_page
    hannover_lon, hannover_lan, hannover_address = getInfo("hannover")
    hannover_stadt, hannover_land = "Hannover", "Deutschland"
    hannover_temperatur = int(wetter_daten(hannover_lon, hannover_lan)[1])

    return render_template("welcome_page.html",
        hannover_temperatur = hannover_temperatur, hannover_stadt = hannover_stadt, hannover_land = hannover_land,
    )


@app.route("/wetter")
def wetter():
    stadt = request.args.get("ville")
    lon, lat, address = getInfo(stadt)

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
    
    # Eigentliche Wetterdaten mitnehmen:
    current_date, current_temperature, current_wind_speed, current_relative_humidity, wetter_vorhersage = daten_organisation(lon, lat)
    current_wetter = f" \ndate                       Temperatur(°C)              Luftgeschwindigkeit(m/s)             Luftfleuchtigkeit(°C)\n\n{current_date}        {float("{:.1f}".format(current_temperature))}                        {float("{:.1f}".format(current_wind_speed))}                                 {float("{:.1f}".format(current_relative_humidity))}"

    # Jetzt möchte ich die Wetterdaten von der Woche einzeln entnehmen. Sodass es einfacher wird diese in meinem html Datei darzustellen.
    for i in wetter_vorhersage:
        if i == "date":
            date = wetter_vorhersage[i]
        elif i == "temperature_2m_max":
            temperatur_max = wetter_vorhersage[i]
        elif i == "temperature_2m_min":
                temperatur_min = wetter_vorhersage[i]
        else: break
    tag = " \n\nTag    date                                           Temperatur max(°C)    Temperatur min(°C)\n"
    for i in range(7):
        tag += f"{i+1}      {date[i]}                      {temperatur_max[i]:.1f}                  {float("{:.1f}".format(temperatur_min[i]))}\n"
            

    return render_template(
        "wetter_page.html",
        stadt_name = info_1,
        region = info_2,
        land = info_4,
        info_random = info_3,
        current_wetter = current_wetter,
        tag = tag,
        
        
)
