import web
import requests
import json
import SFdata

apikey = SFdata.apikey
auth = SFdata.auth
base_url = "https://api.stockfighter.io/gm/instances/"

account = SFdata.account
stock = SFdata.stock
venue = SFdata.venue
instance = SFdata.instance

perp = "RAH5051135"

url = base_url + perp + "/judge"

link = "https://docs.google.com/document/d/1cWRproRq_FwsX6Lmm-s_Xvb9IeNLX_DeJ-vcTX-QRMk"

summary = """

 To summarize, my three pieces of evidence pointing to account 
 RAH5051135 as the anomaly were:

 1. It had the largest (fractional) discrepancy between average bid quantity 
      and average ask quantity - 251 to 1,425, respectively. 
      This is what led me to piece #2.
 2. It was the only account to repeatedly return to the same position after 
      selling off a large number of shares. Although I can’t be certain, 
      I would bet that it was selling to a position of zero.
 3. It had the highest gained value per trade, and per share traded, 
      among all accounts on the exchange.

 """

evidence = { "account" : perp, "explanation_link": link, 
              "executive_summary": summary }

def post():
    p = requests.post(url, data=json.dumps(evidence), headers=auth)
    presp = json.loads(p.content)
    return presp

if __name__ == '__main__':
    presp = post()
