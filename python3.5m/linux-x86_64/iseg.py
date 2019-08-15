# pyDevSup imports
import devsup.db as db
import devsup.ptable as PT
import signal

import json
import time
import threading
from websocket import create_connection


# Workaround CTRL+C not working
signal.signal(signal.SIGINT, signal.SIG_DFL)

class isegSupport(PT.TableBase):
    trigger = PT.Parameter()
    a = PT.Parameter()
    b = PT.Parameter()
    s = PT.Parameter(iointr=True)
    time = PT.Parameter(iointr=True)
    temp = PT.Parameter(iointr=True)
    
    def __init__(self, name):
        super().__init__(name='iseg')    

    def calls(self,ws):
        for i in range(10):
            received = ws.recv()
            jsoned = json.loads(received)
            for js in jsoned:            
                if 'c' in js:
                    for item in js['c']:
                        typ = item['d']['i']
                        if typ == "System.time":
                            self.time.value = item['d']['v']
                            self.time.notify()
                        if typ == "Status.temperature0" or typ == "Status.temperature1":
                            self.temp.value = item['d']['v']
                            self.temp.notify()

    @trigger.onproc
    def do_trigger(self):
        ws = create_connection("ws://192.168.1.101:8080",timeout=40)
        login_request = '''{
	                    "i": "",
	                    "t": "login",
	                    "c": {
		                    "l": "user",
		                    "p": "user",
		                    "t": ""
	                    },
	                    "r": "websocket"
                        }'''
        ws.send(login_request)
        login_message = ws.recv()
        session_id = json.loads(login_message)['i']
        getVoltage= '''{
	                "i": "%s",
	                "t": "request",
	                "c": [
		                    {
			                    "c": "getItem",
			                    "p": {
				                    "p": {
					                    "l": "0",
					                    "a": "*",
					                    "c": "*"
				                    },
				                    "i": "Control.voltageSet",
				                    "v": "",
				                    "u": ""
			                    }
		                    }
	                ],
	                "r": "websocket"
                    }''' % session_id
        ws.send(getVoltage)
        self.calls(ws)


        #self.time.value = received
        #self.time.notify()
        #self.temp.value = 72.981
        #self.temp.notify()

def build():
    return isegSupport('iseg')

