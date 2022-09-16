import http.client
from urllib import request
import json

class ApiFootball:
    encodes = { #dict per ottenere i parametri per effettuare la richiesta
        'leagues': {
            'encode': "/v2/leagues",
            'link': "api-football-v1.p.rapidapi.com"
        },
        'teams': {
            #'encode': "/v3/teams?country=Italy",
            'encode': "/v3/teams?id=4399",
            'link': "api-football-v1.p.rapidapi.com"
        }
    }

    def set_params(self, active):
        self.link = self.encodes[active]['link']
        self.conn = http.client.HTTPSConnection(self.link)
        
        self.encode = self.encodes[active]['encode']

        self.headers = {
            'X-RapidAPI-Key': "987bd9b2f6msh096a10b27865b48p11788djsn5eab36718bcd",
            'X-RapidAPI-Host': self.link
            }

    def make_request(self):
        self.conn.request("GET", self.encode, headers=self.headers)

        res = self.conn.getresponse()
        data = res.read()

        self.string_data = data.decode("utf-8")

    def save_data(self, name):
        file_path = 'datasets/'+name+'.json'
        to_dict = json.loads(self.string_data) #convert string to dict

        with open(file_path, 'w') as outfile:
            json_object = json.dumps(to_dict, indent = 4) #convert dict to JSON string
            outfile.write(json_object)