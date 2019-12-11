import json
import requests

URL = 'http://[BRIDGE_IP]/api/[AUTHKEY]/'


class Light:
    def __init__(self, _id):
        self.GetInitialStatus(_id)

    def GetInitialStatus(self, _id):
        try:
            res = requests.get(URL + 'lights/' + _id)
            data = json.loads(res.text)
            self.SetInitialStatus(data)          
        except:
            print("Error")

    def SetInitialStatus(self, dictionary):
        try:
            self.state = dictionary["state"]
            self.swupdate = dictionary["swupdate"]
            self.type = dictionary["type"]
            self.name = dictionary["name"]
            self.modelid = dictionary["modelid"]
            self.manufacturername = dictionary["manufacturername"]
            self.productname = dictionary["productname"]
            self.capabilities = dictionary["capabilities"]
            self.config = dictionary["config"]
            self.uniqueid = dictionary["uniqueid"]
            self.swversion = dictionary["swversion"]
            self.productid = dictionary["productid"]
        except:
            print("Error parsing initial light status")

    def ToggleLight(self, _id, state):
        payload = { 'on': state }
        req = None
        try:
            res = requests.put(URL + 'lights/' + _id + '/state', data=json.dumps(payload))
            data = res.json()
            print(data)
        except requests.exceptions.RequestException as e:
            if req != None:
                print(req.text)
            print(e)
            raise

    def ChangeBrightness(self, _id, value):
        payload = { 'bri': value }
        req = None
        try:
            res = requests.put(URL + 'lights/' + _id + '/state', data=json.dumps(payload))
            data = res.json()
            print(data)
        except requests.exceptions.RequestException as e:
            if req != None:
                print(req.text)
            print(e)
            raise

    def ChangeColor(self, _id, xy):
        payload = { 'xy': xy }
        req = None
        try:
            res = requests.put(URL + 'lights/' + _id + '/state', data=json.dumps(payload))
            data = res.json()
            print(data)
        except requests.exceptions.RequestException as e:
            if req != None:
                print(req.text)
            print(e)
            raise