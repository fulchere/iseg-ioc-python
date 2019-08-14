# pyDevSup imports
import devsup.db as db
import devsup.ptable as PT

import signal

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

    @trigger.onproc
    def do_trigger(self):
        self.s.value = self.a.value + self.b.value
        self.s.notify()
        self.time.value = "4:23:46"
        self.temp.value = "72oC"
        self.time.notify()
        self.temp.notify()

def build():
    return isegSupport('iseg')

