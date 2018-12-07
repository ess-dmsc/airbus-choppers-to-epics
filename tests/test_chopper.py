from unittest.mock import MagicMock
from chopper import Chopper


PARAMETERS_RESPONSE = (
    "#SRP#"
    "<Msg>"
    "<SysName>Tisane</SysName>"
    '<Param SysType="NCS" SysNo="0" ReqSpeed="2000" ActSpeed="-2000" ReqGear="0" '
    'ReqDir="1" ActDir="CounterClockwise" ReqPhase="123" ActPhase="456"/>'
    "</Msg>"
)

SET_SPEED_OKAY_RESPONSE = (
    "#SRP#"
    "<Msg>"
    "<SysName>Tisane</SysName>"
    '<Param SysType="NCS" SysNo="0" ReqSpeed="200"/>'
    "</Msg>"
)

SET_SPEED_ERROR_RESPONSE = (
    "#SRP#"
    "<Msg>"
    "<SysName>Tisane</SysName>"
    '<Param SysType="NCS" SysNo="0" ReqSpeed="Failure, something went wrong"/>'
    "</Msg>"
)


class TestChopper:
    def test_requesting_basic_parameters_updates_values(self):
        # Set up mocking
        chopper = Chopper("COM1")
        chopper._send_receive = MagicMock(return_value=PARAMETERS_RESPONSE)

        response = chopper.request_parameters()

        assert response["ReqSpeed"] == 2000
        assert response["ActSpeed"] == -2000
        assert response["ReqPhase"] == 123
        assert response["ActPhase"] == 456

    def test_setting_speed_is_okay(self):
        # Set up mocking
        chopper = Chopper("COM1")
        chopper._send_receive = MagicMock(return_value=SET_SPEED_OKAY_RESPONSE)

        response = chopper.set_speed(100)

        assert response

    def test_setting_speed_is_not_okay(self):
        # Set up mocking
        chopper = Chopper("COM1")
        chopper._send_receive = MagicMock(return_value=SET_SPEED_ERROR_RESPONSE)

        response = chopper.set_speed(100)

        assert not response
