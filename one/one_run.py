import web
import requests
import json
import SFdata

auth = SFdata.auth
base_url = SFdata.base_url

account = SFdata.account
stock = SFdata.stock
venue = SFdata.venue

url = base_url + "/venues/" + venue + "/stocks/" + stock + "/orders"

def get_quote():
    urlget = base_url + "/venues/" + venue + "/stocks/" + stock + "/quote"
    r = requests.get(urlget)
    rresp = json.loads(r.content)
    return rresp

def post(dir):
    p = requests.post(url, data=json.dumps(dir), headers=auth)
    presp = json.loads(p.content)
    return presp

quote = get_quote()
targetprice = quote["last"]

buy = {
  "account":account,
  "venue":venue,
  "symbol":stock,
  "price":targetprice,
  "qty":100,
  "direction":"buy",
  "orderType":"market"
}

bresp = post(buy)
print bresp["ok"]
