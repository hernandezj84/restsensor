"""Contracts module to identify contracts integrity and types"""


class ContractHelper():
    """Exposes reusable methods"""
    @staticmethod
    def get_contract_keys(contract):
        """Returns contracts key"""
        return {key: key for key in contract}

    @staticmethod
    def get_contract_types(contract):
        """Returns types of contracts"""
        return {key: (type(value))
                for (key, value) in contract.items()}


class EventContract():
    """Event contract model"""

    def __init__(self):
        self.contract = {
            "device_id": "TTTTTT-LLLL-IIIII",
            "alarm_level": 1,
            "gas_percent": 75,
            "measured_volts": 3.02,
            "acc_time": 100,
            "gas_type": 1,
            "time_stamp": 1592605050,
            "battery_level": 10,
            "rssi": -90,
            "jocker": "string"
        }
        self.contract_keys = ContractHelper.get_contract_keys(self.contract)
        self.contract_types = ContractHelper.get_contract_types(self.contract)


class RegistryContract():
    """Registry contract model"""

    def __init__(self):

        self.contract = {
            "device_id": "TTTTTT-LLLL-IIIII",
            "device_type": "DEVICE_TYPE_STRING",
            "serial": "SERIAL_NUMBER_STRING",
            "time_stamp": 1592605050
        }
        self.contract_keys = ContractHelper.get_contract_keys(self.contract)
        self.contract_types = ContractHelper.get_contract_types(
            self.contract)
