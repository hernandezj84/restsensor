
class ContractEvent():
    def __init__(self):
        self.device_id = "device_id"
        self.status = "status"
        self.alarm = "alarm"
        self.acc_time = "acc_time"
        self.timestamp = "timestamp"
        self.concent_gas = "concent_gas"
        self.contract = {"device_id": "xxxx", "status": "1", "alarm": "0", "acc_time": "1", "timestamp": "00000", "concent_gas": "00%"}
        self.contract_types = {key:(type(value)) for (key, value) in self.contract.items()}