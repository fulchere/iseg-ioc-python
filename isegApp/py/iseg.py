# pyDevSup imports
import devsup.db as db
import devsup.ptable as PT

import signal
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
        login_message = ws.recv()
        session_id = login_message.split('"')[3]

    @trigger.onproc
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

def build():
    return isegSupport(name='iseg')

