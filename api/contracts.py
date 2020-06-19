"""Contracts module to identify contracts integrity and types"""

class ContractEvent():
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
            "battery_level": 3.90,
            "rssi": -90,
            "jocker": "string"}
        self.contract_keys = {key:key for key in self.contract}
        self.contract_types = {key: (type(value))
                               for (key, value) in self.contract.items()}
