import time
import web
import requests
import json
from ws4py.client.threadedclient import WebSocketClient
import SFdata
import sys
import subprocess

apikey = SFdata.apikey
auth = SFdata.auth
base_url = SFdata.base_url
base_urlws = SFdata.base_urlws

account = SFdata.account
stock = SFdata.stock
venue = SFdata.venue

all_accounts = []

url = base_url + "/venues/" + venue + "/stocks/" + stock + "/orders"

dirpath = "C:/Users/20596566/mystuff/projects/stockfighter/STOCKS/wssub.py "

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

class DummyClient(WebSocketClient):
    def opened(self):
        print "Websocket opened\n"

    def closed(self, code, reason=None):
        print "Websocket closed", code, reason

    def received_message(self, m):
        source = m.data.decode("utf-8")
        n = json.loads(source)
        
        print "\nAccount:", n["account"]
        print "Direction:", n["order"]["direction"]
        print "Original Quantity:", n["order"]["originalQty"]
        print "Type:", n["order"]["orderType"]
        rawprice = int(n["order"]["price"]) / 100.0
        price = "%.2f" % rawprice
        print "Price: $" + str(price)
        if n["order"]["id"] == n["standingId"]:
            id.to_check = n["incomingId"]
        else:
            id.to_check = n["standingId"]
        print "Other party's id:", id.to_check
        
        #if len(m) == 175:
        self.close(reason='Bye bye')

for i in range(1,400):
    if __name__ == '__main__':
        try:
            ws = DummyClient(urlws, protocols=['http-only', 'chat'])
            ws.connect()
            ws.run_forever()
        except KeyboardInterrupt:
            ws.close()

    time.sleep(1)
    cancel_text = cancel_order(id.to_check)
    print "\n"
    unedited = cancel_text["error"][-12:-1]
    if unedited[2] == " ":
        account = unedited[3:]
    elif unedited[1] == " ":
        account = unedited[2:]
    elif unedited[0] == " ":
        account = unedited[1:]
    else:
        account = unedited
    print account
    if account not in all_accounts:
        all_accounts.append(account)
        uaccount = account.encode("utf-8")
        args = [dirpath, uaccount]
        subprocess.Popen([sys.executable,  args],\
                         creationflags = subprocess.CREATE_NEW_CONSOLE)

    urlws = set_urlws()

print len(all_accounts)
