import web
import requests
import json
import SFdata

auth = SFdata.auth
base_url = "https://api.stockfighter.io/gm/instances/"

instance = SFdata.instance

perp = "SM33488048"

url = base_url + str(instance) + "/judge"

link = "https://docs.google.com/document/d/1cWRproRq_FwsX6Lmm-s_Xvb9IeNLX_DeJ-vcTX-QRMk"

summary = """

To summarize, my three pieces of evidence pointing to account 
SM33488048 as the anomaly were:

1. It had the largest (fractional) discrepancy between average bid quantity 
     and average ask quantity. This is what led me to piece #2. 
2. It was the only account to repeatedly return to the same position after
     selling off a large number of shares. Although I can't be certain, 
     I would bet that it was selling to a position of zero. 
3. It had the highest gained value per trade, and per share traded, 
     among all accounts on the exchange. 

"""

evidence = {
  "account":perp,
  "explanation_link":link, 
  "executive_summary":summary
}

def post():
    p = requests.post(url, data=json.dumps(evidence), headers=auth)
    presp = json.loads(p.content)
    return presp

if __name__ == '__main__':
    presp = post()
    print presp
