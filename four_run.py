import web
import requests
import json
import SFdata

apikey = SFdata.apikey
auth = SFdata.auth
base_url = SFdata.base_url

account = SFdata.account
stock = SFdata.stock
venue = SFdata.venue

url = base_url + "/venues/" + venue + "/stocks/" + stock + "/orders"


def update_targetprice(last):
    del last_five[0]
    last_five.append(last)
    targetprice = sum(last_five) / 5
    return targetprice

def get_quote():
    urlget = base_url + "/venues/" + venue + "/stocks/" + stock + "/quote"
    r = requests.get(urlget)
    rresp = json.loads(r.content)
    return rresp

def post(dir):
    p = requests.post(url, data=json.dumps(dir), headers=auth)
    presp = json.loads(p.content)
    return presp

def get_status(id):
    xget = requests.get(url + "/" + str(id), headers=auth)
    xstatus = json.loads(xget.content)
    return xstatus

def cancel_order(id):
    ccan = requests.post(url + "/" + str(id) + "/cancel", headers=auth)

def get_filled(status):
    qty = 0
    if len(status["fills"]) > 0:
        for i in range(0, len(status["fills"])):
            qty += status["fills"][i]["qty"]
    return qty

last_five = []
for i in range (1, 6):
    quote = get_quote()
    last_five.append(quote["last"])
targetprice = sum(last_five) / 5

buy = {
  "account":account,
  "venue":venue,
  "symbol":stock,
  "price":targetprice,
  "qty":1000,
  "direction":"buy",
  "orderType":"limit"
}

sell = {
  "account":account,
  "venue":venue,
  "symbol":stock,
  "price":targetprice,
  "qty":1000,
  "direction":"sell",
  "orderType":"limit"
}

bminus = 0
sminus = 0

inventory = 0
cash = 0

for num in range(1, 20000):

    buy["qty"] = 1000 - bminus
    sell["qty"] = 1000 - sminus

    quote = get_quote()

    targetprice = update_targetprice(quote["last"])
    buy["price"] = targetprice * 99 / 100
    sell["price"] = targetprice * 101 / 100

    if buy["qty"] > 0:
        bresp = post(buy)
        bid = bresp["id"]
    if sell["qty"] > 0:
        sresp = post(sell)
        sid = sresp["id"]

    bopen = True
    sopen = True
    cownt = 0

    while ((bopen == True) or (sopen == True)):
        bstatus = get_status(bid)
        bopen = bstatus["open"]
        sstatus = get_status(sid)
        sopen = sstatus["open"]

        cownt += 1
        if cownt == 25:
            bopen = False
            sopen = False

    bcan = cancel_order(bid)
    scan = cancel_order(sid)

    bopen = True
    sopen = True

    while ((bopen == True) or (sopen == True)):
        bstatus = get_status(bid)
        bopen = bstatus["open"]
        sstatus = get_status(sid)
        sopen = sstatus["open"]

    binv = 0
    bcost = 0
    sinv = 0
    scost = 0
    if buy["qty"] > 0:
        print "borig:", bstatus["originalQty"], "bfilled:", get_filled(bstatus), \
              "bprice: $", bstatus["price"] / 100.0
        binv = get_filled(bstatus)
        bcost = bstatus["price"] * binv
    if sell["qty"] > 0:
        print "sorig:", sstatus["originalQty"], "sfilled:", get_filled(sstatus), \
              "sprice: $", sstatus["price"] / 100.0
        sinv = get_filled(sstatus)
        scost = sstatus["price"] * sinv

    inventory += (binv - sinv)
    cash += (scost - bcost)
    print "\n", inventory, "units;   $", (cash / 100.0), "      est: $", \
          (cash + (inventory * targetprice)) / 100.0, "\n"

    bminus = 0
    sminus = 0
    if inventory > 0:
        bminus = inventory
    else:
        sminus = inventory * -1
