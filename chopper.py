from serial import Serial, PARITY_NONE, EIGHTBITS, STOPBITS_ONE
from xml.etree import ElementTree as ET
import time


# Set the cache lifetime in seconds
CACHE_LIFETIME = 5


class Chopper:
    def __init__(self, port_num, system_num=0):
        self.port_num = port_num
        self.time_out = 1
        self.system_num = system_num
        self._cache = {"last_update": 0.0, "values": {}}

    def _send_receive(self, command):
        with Serial(
            self.port_num,
            baudrate=9600,
            parity=PARITY_NONE,
            bytesize=EIGHTBITS,
            stopbits=STOPBITS_ONE,
            rtscts=True,
            timeout=1,
        ) as ser:
            ser.write(command)
            ser.flush()
            time.sleep(0.1)
            data = ser.readline()
            return str(data)

    def _construct_read_request(self, parameters):
        pars_str = " ".join(parameters)

        cmd = (
            "#CRQ#"
            "<Msg>"
            "<SysName>Tisane</SysName>"
            '<Param SysType="NCS" SysNo="{}" '
            "{}"
            "/>"
            "</Msg>"
        ).format(self.system_num, pars_str)

        return cmd

    def _construct_set_request(self, parameter, value):
        cmd = (
            "#CRQ#"
            "<Msg>"
            "<SysName>Tisane</SysName>"
            '<Param SysType="NCS" SysNo="{}" '
            '{}="{}"'
            "/>"
            "</Msg>"
        ).format(self.system_num, parameter, value)

        return cmd

    def request_parameters(self):
        if time.time() < self._cache["last_update"] + CACHE_LIFETIME:
            # Use cached values
            return self._cache["values"]

        parameters = ["ReqSpeed", "ActSpeed", "ReqPhase", "ActPhase"]

        cmd = self._construct_read_request(parameters)
        response = self._send_receive(cmd).replace("#SRP#", "")

        data = {}

        xml = ET.fromstring(response)
        for node in xml.findall(".//Param"):
            for pn in parameters:
                try:
                    data[pn] = float(node.attrib[pn])
                except KeyError as err:
                    print(err)

        # Update cache
        self._cache["last_update"] = time.time()
        self._cache["values"] = data

        return data

    def _get_parameter(self, name):
        values = self.request_parameters()
        if name in values:
            return values[name]

        # Some issue with reading parameters
        print("Could not read {}".format(name))

    @property
    def req_speed(self):
        return self._get_parameter("ReqSpeed")

    @property
    def speed(self):
        return self._get_parameter("ActSpeed")

    @property
    def req_phase(self):
        return self._get_parameter("ReqPhase")

    @property
    def phase(self):
        return self._get_parameter("ActPhase")

    def set_speed(self, value):
        # TODO: need to play with the hardware to see what the real behaviour is.
        # I have had to guess a little how this works because the docs are not clear

        # Set the speed using: ReqSpeed="123"
        cmd = self._construct_set_request("ReqSpeed", value)
        response = self._send_receive(cmd).replace("#SRP#", "")

        # I think the response will be a confirmation of the requested value,
        # i.e. ReqSpeed="123"
        # If it fails, it may be ReqSpeed="Failure ..."
        xml = ET.fromstring(response)
        for node in xml.findall(".//Param"):
            try:
                req_speed = node.attrib["ReqSpeed"]
                if req_speed.startswith("Failure"):
                    print(req_speed)
                    return False
            except KeyError as err:
                print(err)
                return False
        return True
