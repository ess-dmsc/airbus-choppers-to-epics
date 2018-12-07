from pcaspy import Driver, SimpleServer
from chopper import Chopper


prefix = "V20:AIRBUS:CHOPPER1:"
pvdb = {"SPD:SP": {"type": 'float'}, "SPD": {"type": 'float'}}


class ChopperDriver(Driver):
    def __init__(self, port):
        super(ChopperDriver, self).__init__()
        self.chopper = Chopper(port)

    def read(self, reason):
        try:
            if reason == 'SPD':
                value = self.chopper.speed
            elif reason == 'SPD:SP':
                value = self.chopper.req_speed
            elif reason == 'PHS':
                value = self.chopper.phase
            elif reason == 'PHS:SP':
                value = self.chopper.req_phase
            else:
                value = self.getParam(reason)
            return value
        except Exception as err:
            print("Could not read value: {}".format(err))


if __name__ == "__main__":
    server = SimpleServer()
    server.createPV(prefix, pvdb)
    driver = ChopperDriver("COM1")

    # process CA transactions
    while True:
        server.process(0.1)
