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
    ws = None
    session_id = None
    volt0 = PT.Parameter(iointr=True)
    volt1 = PT.Parameter(iointr=True)
    volt2 = PT.Parameter(iointr=True)
    volt3 = PT.Parameter(iointr=True)
    volt4 = PT.Parameter(iointr=True)
    volt5 = PT.Parameter(iointr=True)
    volt6 = PT.Parameter(iointr=True)
    volt7 = PT.Parameter(iointr=True)

    def __init__(self, name):
        super().__init__(name='iseg')
        self.ws = create_connection("ws://192.168.1.101:8080",timeout=40)
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
        self.ws.send(login_request)
        login_message = self.ws.recv()
        self.session_id = json.loads(login_message)['i']

    def thread_call(self):
        for i in range(1):
            received = self.ws.recv()
            jsoned = json.loads(received)
            for js in jsoned:            
                if 'c' in js:
                    for item in js['c']:
                        typ = item['d']['i']
                        if typ == "System.time":
                            self.time.value = item['d']['v']
                            self.time.notify()
                        if typ == "Status.temperature0" or typ == "Status.temperature1":
                            self.temp.value = float(item['d']['v'])
                            self.temp.notify()
                        if typ == "Status.voltageMeasure":
                            val = float(item['d']['v'])
                            if item['d']['p']['c'] == '0':
                                self.volt0.value = val
                                self.volt0.notify()
                            if item['d']['p']['c'] == '1':
                                self.volt1.value = val
                                self.volt1.notify()
                            if item['d']['p']['c'] == '2':
                                self.volt2.value = val
                                self.volt2.notify()
                            if item['d']['p']['c'] == '3':
                                self.volt3.value = val
                                self.volt3.notify()
                            if item['d']['p']['c'] == '4':
                                self.volt4.value = val
                                self.volt4.notify()
                            if item['d']['p']['c'] == '5':
                                self.volt5.value = val
                                self.volt5.notify()
                            if item['d']['p']['c'] == '6':
                                self.volt6.value = val
                                self.volt6.notify()
                            if item['d']['p']['c'] == '7':
                                self.volt7.value = val
                                self.volt7.notify()

    @trigger.onproc
    def do_trigger(self):
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
                    }''' % self.session_id
        self.ws.send(getVoltage)
        thread = threading.Thread(target=self.thread_call)
        thread.start()
        thread.join()

def build():
    return isegSupport('iseg')

