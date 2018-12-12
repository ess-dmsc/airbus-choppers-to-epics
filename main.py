from pcaspy import Driver, SimpleServer
from chopper import Chopper
from threading import Thread, RLock
import time


prefix = "V20:AIRBUS:CHOPPER"
pvdb = {
    "1:SPD": {"type": "float"},
    "1:PHS": {"type": "float"},
    "1:PHS:SP": {"type": "float"},
    "2:SPD": {"type": "float"},
    "2:PHS": {"type": "float"},
    "2:PHS:SP": {"type": "float"},
    "3:SPD": {"type": "float"},
    "3:PHS": {"type": "float"},
    "3:PHS:SP": {"type": "float"},
    "4:SPD": {"type": "float"},
    "4:PHS": {"type": "float"},
    "4:PHS:SP": {"type": "float"},
}


class ChopperDriver(Driver):
    def __init__(self):
        super(ChopperDriver, self).__init__()
        self.choppers = [Chopper(1), Chopper(2), Chopper(3), Chopper(4)]

        self.monitor_lock = RLock()
        monitor_thread = Thread(target=self.update_monitors, args=())
        monitor_thread.daemon = True  # Daemonise thread
        monitor_thread.start()

    def read(self, reason):
        value = self.getParam(reason)
        return value

    def update_monitors(self):
        while True:
            with self.monitor_lock:
                for ch in self.choppers:
                    ch.update()
                    self.setParam("{}:SPD".format(ch.chopper_num), ch.speed)
                    self.setParam("{}:PHS".format(ch.chopper_num), ch.phase)
                    self.setParam("{}:PHS:SP".format(ch.chopper_num), ch.req_phase)
                self.updatePVs()
            time.sleep(1)


if __name__ == "__main__":
    print("Airbus Choppers to EPICS")
    print("Checking connection to database...")
    ans = Chopper(1)._get_data()
    if ans is not None and len(ans) > 0:
        print("...connection established")
    else:
        raise Exception("Could not connect to database")

    server = SimpleServer()
    server.createPV(prefix, pvdb)
    driver = ChopperDriver()

    # process CA transactions
    while True:
        server.process(0.1)
