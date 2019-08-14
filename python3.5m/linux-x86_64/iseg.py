# pyDevSup imports
import devsup.db as db
import devsup.ptable as PT

import signal
import json
import threading
from websocket import create_connection

import sys
assert sys.version >= (3,0)

# Workaround CTRL+C not working
signal.signal(signal.SIGINT, signal.SIG_DFL)

class isegSupport(PT.TableBase):
    trigger = PT.Parameter()
    a = PT.Parameter()
    b = PT.Parameter()
    s = PT.Parameter(iointr=True)
    time = PT.Parameter()
    temperature = PT.Parameter()
    ws = None

    def __init__(self):
        super().__init__(name='iseg')
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
        login_json = json.loads(ws.recv())
        session_id = login_json['i']


    def do_trigger(self):
        self.s.value = self.a.value + self.b.value
        self.s.notify()

        generic_request = '''{
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
				                "i": "Status.voltageMeasure",
				                "v": "",
				                "u": ""
			                }
		                }
	                ],
	                "r": "websocket"
                    }''' % (session_id,)
        ws.send(generic_request)
        while True:
            print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXx")
            received = ws.recv()
            jsoned = json.loads(received)
            if 'c' in jsoned[0]:
                for item in jsoned[0]['c']:
                    if item['d']['i'] == 'System.time':
                        self.time.value = item['d']['v']
                    if item['d']['i'] == 'Status.temperature1':
                        self.temperature.value = item['d']['v']

    @trigger.onproc
    def for_thread(self):
        thread = threading.Thread(target=self.do_trigger)
        thread.start()
        thread.join()
                
def build():
    return isegSupport(name='iseg')

