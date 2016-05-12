import pandas as pd
import bs4
from bs4 import BeautifulSoup
import requests
import html5lib
import re

s = open("rt-wts.html", encoding="ISO-8859-1").read()
parser = BeautifulSoup(s, 'html5lib')
films = parser.find_all("li", class_="bottom_divider media")

save = {}

for film in films:
    name = film.find("a")["title"]
    save[name] = {}
    
    _score = film.find("span", class_="tMeterScore")
    if _score is None:
        score = 0
    else:
        score = int(_score.string.split("%")[0])
        
    save[name]["Score"] = score

    r = film.find("p", class_="subtle small").text.split(" -")[1]
    if "," in r:
        r = r.split(",")[1]

    hrs_match = re.match("(?:\d*\.)?\d+ hr", r)
    mins_match = re.search("(?:\d*\.)?\d+ min", r)

    if hrs_match is not None:
        hrs = hrs_match.group().split()[0]
    else:
        hrs = 0

    if mins_match is not None:
        mins = mins_match.group().split()[0]
    else:
        mins = 0

    save[name]["Runtime"] = (int(hrs) * 60) + int(mins)
    print(save[name]["Runtime"])

thats_better = pd.DataFrame.from_dict(save, orient="index")
thats_better.sort_values("Score", ascending=False)
