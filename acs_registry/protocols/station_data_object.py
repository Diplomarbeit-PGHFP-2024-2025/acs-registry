import json

from uagents import Model
import datetime


class StationDataObject(Model):
    address: str
    expireAt: float
    coordinates: tuple[float, float]

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    @staticmethod
    def list_to_json(data: list["StationDataObject"]) -> list[str]:
        jsons: list[str] = []
        for obj in data:
            jsons.append(obj.to_json())

        return jsons

    @staticmethod
    def from_json(data: str):
        return json.loads(data, object_hook=lambda d: StationDataObject(**d))

    @staticmethod
    def list_from_json(data: list[str]) -> list["StationDataObject"]:
        objects = []
        for json_object in data:
            objects.append(StationDataObject.from_json(json_object))

        return objects

    def expired(self):
        return self.expireAt < datetime.datetime.now().timestamp()
