from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime
from math import ceil
import pandas as pd
import json
import urllib.parse
import pytz
import re


hostName = '127.0.0.1'
serverPort = 8000


def to_latin(string):
    if 'ае' in string:
        string = string.replace('ае', 'aye')
    if 'ое' in string:
        string = string.replace('ое', 'oye')
    if 'ье' in string:
        string = string.replace('ье', '’ye')
    dictionary = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'ë',
                  'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
                  'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh',
                  'ц': 'c', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '”', 'ы': 'y', 'ь': '’', 'э': 'e',
                  'ю': 'yu', 'я': 'ya', 'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'Ye',
                  'Ж': 'Zh', 'З': 'Z', 'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N',
                  'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'Kh',
                  'Ц': 'C', 'Ч': 'CH', 'Ш': 'Sh', 'Щ': 'Sch', 'Ы': 'Y', 'Э': 'E',
                  'Ю': 'Yu', 'Я': 'Ya'}
    for key in dictionary:
        string = string.replace(key, dictionary[key])
    return string


def pick_one(latin, cyrill):
    inf = df.loc[(df["name"] == latin) | (df["alternatenames"].str.contains("," + cyrill + ","))
                      | (df["alternatenames"].str.startswith(cyrill + ","))
                      | (df["alternatenames"].str.endswith("," + cyrill))
                      | (df["alternatenames"].str == cyrill)]
    if inf.shape[0] > 0:
        inf = inf.loc[inf["population"].idxmax()]
    return inf


def diff_between_tz(inf1, inf2):
    dt = datetime.now()
    tz1 = pytz.timezone(inf1.loc["timezone"])
    tz2 = pytz.timezone(inf2.loc["timezone"])
    if inf1.loc["longitude"] > inf2.loc["longitude"]:
        timedelta = tz1.utcoffset(dt) - tz2.utcoffset(dt)
    else:
        timedelta = tz2.utcoffset(dt) - tz1.utcoffset(dt)
    return abs(int(timedelta.seconds // 3600))


def get_indexes(page, count_city_list):
    numbers_of_rows = len(df.index)
    max_page = ceil(numbers_of_rows / count_city_list)
    if 1 <= page <= max_page and count_city_list <= numbers_of_rows:
        ind_start = (page - 1) * count_city_list
        ind_end = page * count_city_list - 1
        if ind_end >= numbers_of_rows:
            ind_end = numbers_of_rows
        return [ind_start, ind_end]
    else:
        return []


class CitiesServer(BaseHTTPRequestHandler):
    def getCityInfo(self):
        geonameid = int(self.path[self.path.find("=")+1:])
        inf = df[df["geonameid"] == geonameid]
        if inf.empty:
            response = json.dumps({})
            self.wfile.write(response.encode())
        else:
            response = json.dumps(json.loads(inf.to_json(orient='index'))[str(inf.index[0])], ensure_ascii=False)
            self.wfile.write(response.encode())

    def getCityList(self):
        path_list = self.path[self.path.find("=")+1:].split('&number=')
        page = int(path_list[0])
        count_city_list = int(path_list[1])
        index = get_indexes(page, count_city_list)
        if not index:
            response = json.dumps({})
            self.wfile.write(response.encode())
        else:
            inf = df.loc[index[0]:index[1]]
            response = json.dumps(json.loads(inf.to_json(orient='index')), ensure_ascii=False)
            self.wfile.write(response.encode())

    def getTwoCitiesInfo(self):
        url = urllib.parse.unquote(self.path[self.path.find("=")+1:])
        path_list = url.split('&city2=')
        city1_cyrill = str(path_list[0])
        city2_cyrill = str(path_list[1])
        city1_latin = to_latin(city1_cyrill)
        city2_latin = to_latin(city2_cyrill)
        inf1 = pick_one(city1_latin, city1_cyrill)
        inf2 = pick_one(city2_latin, city2_cyrill)
        if inf1.empty or inf2.empty:
            response = json.dumps({})
            self.wfile.write(response.encode())
        else:
            response_dict = dict()
            response_dict["city1"] = inf1.to_dict()
            response_dict["city2"] = inf2.to_dict()
            if inf1.loc["latitude"] > inf2.loc["latitude"]:
                response_dict["NorthernCity"] = inf1.loc["name"]
            else:
                response_dict["NorthernCity"] = inf2.loc["name"]
            if inf1.loc["timezone"] == inf2.loc["timezone"]:
                response_dict["SameTimeZone"] = True
            else:
                response_dict["SameTimeZone"] = False
                hours = diff_between_tz(inf1, inf2)
                response_dict["TimeZoneDifferenceInHours"] = hours
            response = json.dumps(response_dict, ensure_ascii=False)
            self.wfile.write(response.encode())

    def getHint(self):
        city = str(urllib.parse.unquote(self.path[self.path.find("=")+1:]))
        inf = df.loc[((df["alternatenames"].str.startswith(city)) |
                           (df["alternatenames"].str.contains("," + city)))]
        if inf.empty:
            response = json.dumps({})
            self.wfile.write(response.encode())
        else:
            name_set = set()
            for name in inf['alternatenames']:
                name = name[name.find(city):]
                if name.find(",") != -1:
                    name = name[:name.find(",")]
                name_set.add(name)
            response = json.dumps({"hint": list(name_set)}, ensure_ascii=False)
            self.wfile.write(response.encode())

    def do_GET(self):
        pattern1 = r"\A\/getCityInfo\?geonameid\=\d+\Z"
        pattern2 = r"\A\/getCityList\?page\=\d+\&number\=\d+\Z"
        pattern3 = r"\A\/getTwoCitiesInfo\?city1\=.+\&city2\=.+"
        pattern4 = r"\A\/getHint\?city\=.+"
        patterns = [(pattern1, self.getCityInfo), (pattern2, self.getCityList), (pattern3, self.getTwoCitiesInfo),
                    (pattern4, self.getHint)]
        for pattern, handler in patterns:
            if re.match(pattern, self.path):
                self.send_response(200)
                self.send_header('content-type', 'text/json')
                self.end_headers()
                handler()
                return
        self.send_response(404)
        self.send_header('content-type', 'text/json')
        self.end_headers()
        response = json.dumps({"Error": 404})
        self.wfile.write(response.encode())


if __name__ == '__main__':
    columns = ["geonameid", "name", "asciiname", "alternatenames", "latitude", "longitude", "feature class",
               "feature code", "country code", "cc2", "admin1 code", "admin2 code", "admin3 code",
               "admin4 code", "population", "elevation", "dem", "timezone", "modification date"]
    df = pd.read_csv('RU.txt', sep='\t', encoding='utf8', header=None, names=columns, low_memory=False)
    webServer = HTTPServer((hostName, serverPort), CitiesServer)
    print("Server is running")
    webServer.serve_forever()


