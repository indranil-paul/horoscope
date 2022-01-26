from flask import Blueprint, redirect, url_for, render_template
from .pyastro import Pyastro


scraper = Blueprint('scraper', __name__, template_folder='templates/scraper')
ALLTIMEFRAMES = []
ALLSUNSIGNS = []
ASTRO_OBJ = None
ZODIAC = {}


@scraper.before_request
def load_template():
    global ALLTIMEFRAMES, ALLSUNSIGNS, ASTRO_OBJ, ZODIAC
    ASTRO_OBJ = Pyastro(_json_filepath='static/data/zodiac.json')
    ALLTIMEFRAMES = [freq.strip() for freq in ASTRO_OBJ.timeframes.split(',')]
    ALLSUNSIGNS = [zodiac.strip() for zodiac in ASTRO_OBJ.sunsigns.split(',')]
    ZODIAC = ASTRO_OBJ.zodiac_details


## This page will show the horoscope based on given sign & freq
@scraper.route("/horoscope/<_sign>/<_freq>")
def show_horoscope(_sign, _freq):
    try:
        ## Get the horoscope
        ASTRO_OBJ.sign = _sign
        ASTRO_OBJ.frequency = _freq
        horoscope_data = ASTRO_OBJ.horoscope
        
        zodiac_details = None
        for zdc in ZODIAC:
            if zdc['name'].lower() == _sign.lower():
                zodiac_details = zdc.copy()
                break

        return render_template("horoscope.html", data=horoscope_data, sign=_sign, freq=_freq, timeframe=ALLTIMEFRAMES, zodiac=zodiac_details)     
    except Exception as e:
        return render_template("400.html", err_msg=str(e))


## The home page
@scraper.route("/home")
def home():
    return render_template("index.html", zodiac=ZODIAC)
