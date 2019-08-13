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

    @trigger.onproc
    def do_trigger(self):
        self.s.value = self.a.value + self.b.value
        self.s.notify()

def build():
    return isegSupport(name='iseg')

