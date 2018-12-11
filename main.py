from pcaspy import Driver, SimpleServer
from chopper import Chopper


prefix = "V20:AIRBUS:CHOPPER"
pvdb = {
    "1:SPD": {"type": "float"},
    "1:PHS": {"type": "float"},
    "1:PHS:SP": {"type": "float"},
    "2:SPD": {"type": "float"},
    "2:PHS": {"type": "float"},
    "2:PHS:SP": {"type": "float"},
}


class ChopperDriver(Driver):
    def __init__(self):
        super(ChopperDriver, self).__init__()
        self.chopper1 = Chopper(1)
        self.chopper2 = Chopper(2)

    def read(self, reason):
        try:
            if reason == "1:SPD":
                value = self.chopper1.speed
            elif reason == "1:PHS":
                value = self.chopper1.phase
            elif reason == "1:PHS:SP":
                value = self.chopper1.req_phase
            elif reason == "2:SPD":
                value = self.chopper2.speed
            elif reason == "2:PHS":
                value = self.chopper2.phase
            elif reason == "2:PHS:SP":
                value = self.chopper2.req_phase
            else:
                value = self.getParam(reason)
            return value
        except Exception as err:
            print("Could not read value: {}".format(err))


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
