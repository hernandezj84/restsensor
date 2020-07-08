"""Create, read, update and delete helper"""
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from api.models import Device, Event, GasType, Alarm, DeviceType, ApiUser
from api.firebase import Firebase

MODEL_CONTRACT_MAP = {
    Device.__name__: "registry",
    Event.__name__: "event"
}

CONTRACTS_MAP = {
    "event": {
        "device": "device_id",
        "alarm": "alarm_level",
        "gas_percent": "gas_percent",
        "measured_volts": "measured_volts",
        "acc_time": "acc_time",
        "gas_type": "gas_type",
        "time_stamp": "time_stamp",
        "battery_level": "battery_level",
        "rssi": "rssi",
        "jocker": "jocker"
    },
    "registry": {
        "device_id": "device_id",
        "device_type": "device_type",
        "serial": "serial",
        "time_stamp": "time_stamp"
    },
    "signup": {
        "user_name": "username",
        "user_email": "email",
        "password": "password"
    }
}


class Crud:
    """Object that helps to insert the json in database"""

    def __init__(self):
        self.fields_types = ["ForeignKey", "AutoField", "BooleanField"]

    def save_model(self, model, json_post):
        """Saves with the rest of the data provided by json_post"""
        model_structure = {field.name: model._meta.get_field(
            field.name).get_internal_type() for field in model._meta.get_fields()}
        for field in model_structure:
            if model_structure[field] not in self.fields_types:
                model_contract_map = MODEL_CONTRACT_MAP[model.__class__.__name__]
                contract_map = CONTRACTS_MAP[model_contract_map]
                json_field = contract_map[field]
                setattr(
                    model, field, json_post[json_field])

        model.save()

    def save_event(self, json_post):
        """Saves event model from json_post"""

        device = Device.objects.get(device_id=json_post["device_id"])
        alarm = Alarm.objects.get(alarm=json_post["alarm_level"])
        gas_type = GasType.objects.get(gas_type=json_post["gas_type"])
        event = Event(device=device, alarm=alarm, gas_type=gas_type)
        self.save_model(event, json_post)
        firebase_api = Firebase()
        firebase_api.set_event(json_post)
        return event

    @staticmethod
    def create_get_device_type(name):
        """Creates device_type"""
        device_type = DeviceType.objects.filter(name=name)
        if len(device_type) == 0:
            device_type = DeviceType(name=name)
            device_type.save()
        else:
            device_type = device_type[0]
        return device_type

    @staticmethod
    def get_create_device(device_id, serial, device_type):
        """Creates device"""
        device = Device.objects.filter(device_id=device_id, serial=serial)
        if len(device) == 0:
            device = Device(device_type=device_type, active=True)
        else:
            device = device[0]
            device.active = True
            device.device_type = device_type
        return device

    def save_registry(self, json_post):
        """Saves registry (Device model) from json_post"""
        device_type = self.create_get_device_type(json_post["device_type"])
        device = self.get_create_device(
            json_post["device_id"], json_post["serial"], device_type)
        self.save_model(device, json_post)
        return device

    @staticmethod
    def save_user(json_post):
        """Creates a new user"""
        user = User.objects.create_user(
            username=json_post["user_email"], email=json_post["user_email"], password=json_post["password"])
        ApiUser.objects.create(user=user, user_name=json_post["user_name"])
        token = Token.objects.get_or_create(user=user)
        return token[0].key

    @staticmethod
    def login(json_post):
        """Gives token to user"""
        user = User.objects.get(
            username=json_post["user_email"])
        token = Token.objects.get_or_create(user=user)
        return token[0].key

    @staticmethod
    def get_token(token):
        return Token.objects.get(key=token).user.username
