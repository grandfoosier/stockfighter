import time
import web
import requests
import json
from ws4py.client.threadedclient import WebSocketClient
import SFdata
import sys

apikey = SFdata.apikey
auth = SFdata.auth
base_url = SFdata.base_url
base_urlws = SFdata.base_urlws

account = sys.argv[1]
stock = SFdata.stock
venue = SFdata.venue

path = "C:/users/20596566/mystuff/projects/stockfighter/docs/" + account + ".txt"
acct_file = open(path, 'w')
acct_file.write(account + "\n")

url = base_url + "/venues/" + venue + "/stocks/" + stock + "/orders"

class Identification(object):
    def __init__(self):
        to_check = 1

id = Identification()

def set_urlws():
    urlws = base_urlws + "/ws/" + account + "/venues/" + \
            venue + "/executions/stocks/" + stock
    return urlws

urlws = set_urlws()

def get_status(id):
    xget = requests.get(url + "/" + str(id), headers=auth)
    xstatus = json.loads(xget.content)
    return xstatus

def cancel_order(id):
    ccan = requests.post(url + "/" + str(id) + "/cancel", headers=auth)
    cstatus = json.loads(ccan.content)
    return cstatus

class Position(object):
    def __init__(self):
        self.shares = 0
        self.cash = 0
pos = Position()

class DummyClient(WebSocketClient):
    def opened(self):
        print "Websocket opened\n"

    def closed(self, code, reason=None):
        print "Websocket closed", code, reason

    def received_message(self, m):
        source = m.data.decode("utf-8")
        n = json.loads(source)

        rawprice = int(n["order"]["price"]) / 100.0
        price = "%.2f" % rawprice
        rawpricef = int(n["price"]) / 100.0
        pricef = "%.2f" % rawpricef

        mult = 1
        if n["order"]["direction"] == "sell": mult = -1
        pos.shares += n["filled"] * mult
        rawcash = (int(n["filled"]) * int(n["price"])) / 100.0 * mult * -1
        pos.cash += rawcash
        est = pos.cash + (pos.shares * (int(n["price"])) / 100.0)
        if (pos.shares ** 2) < 10000: 
            print "\nAccount:", n["account"]
            print "\nPosition:", pos.shares, "shares,  $%.2f" % pos.cash,\
                  "  est:  $%.2f" % est

        timein = n["order"]["ts"][12:]
        timeout = n["filledAt"][12:]

        acct_file.write("%s, %s, $%s, %s, %s, $%s, %s\n" % 
                        (n["order"]["direction"], n["order"]["originalQty"], 
                        price, timein, n["filled"], pricef, timeout))

        if len(m) == 175:
            self.close(reason='Bye bye')

for i in range(1, 100):
    if __name__ == '__main__':
        try:
            ws = DummyClient(urlws, protocols=['http-only', 'chat'])
            ws.connect()
            ws.run_forever()
        except KeyboardInterrupt:
            ws.close()

pause = raw_input()
