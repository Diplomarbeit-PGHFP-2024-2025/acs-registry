import json
from typing import List

from uagents import Model
import datetime


class StationDataObject(Model):
    address: str  # Address of the station
    expiration_timestamp: (
        float  # Expiry timestamp of station registration (Unix timestamp)
    )
    coordinates: tuple[float, float]  # x and y coordinates of the station

    def to_json(self):
        """
        Converts the object into a JSON string representation. The method serializes the attributes
        of the object into JSON format, leveraging the default behavior to convert any unsupported
        types through their `__dict__` attribute. The resulting JSON string is indented for
        readability and sorted by keys.

        :return: A string containing the JSON representation of the object.
        :rtype: str
        """
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    @staticmethod
    def list_to_json(data: List["StationDataObject"]) -> List[str]:
        """
        Converts a list of StationDataObject instances to a list of JSON strings.

        This method iterates through the provided list of StationDataObject instances
        and invokes their respective `to_json()` method to obtain their JSON
        representations. The resulting JSON strings are collected in a new list, which
        is then returned.

        :param data: A list of StationDataObject instances to be converted to JSON strings.
        :type data: List[StationDataObject]
        :return: A list of JSON strings representing the given StationDataObject instances.
        :rtype: List[str]
        """
        return [obj.to_json() for obj in data]

    @staticmethod
    def from_json(data: str):
        """
        Converts a JSON string into a StationDataObject using the provided JSON decoding and
        object hook. This method deserializes the JSON input into a Python object by mapping
        its keys to the attributes of the StationDataObject class.

        :param data: JSON-formatted string containing station data
        :type data: str
        :return: A StationDataObject instance constructed from the provided JSON data
        :rtype: StationDataObject
        """
        return json.loads(data, object_hook=lambda d: StationDataObject(**d))

    @staticmethod
    def list_from_json(data: List[str]) -> List["StationDataObject"]:
        """
        Converts a list of JSON strings into a list of StationDataObject instances.

        This static method iterates through each JSON string in the provided list,
        parses them into StationDataObject instances using the from_json method,
        and compiles them into a new list. This is useful for quickly transforming
        a collection of serialized data into usable StationDataObject objects.

        :param data: A list of JSON strings, where each string represents the
                     serialized data conforming to the StationDataObject structure.
        :return: A list of StationDataObject instances created by parsing
                 the provided JSON strings.
        :rtype: List[StationDataObject]
        """
        return [StationDataObject.from_json(json_object) for json_object in data]

    def is_expired(self) -> bool:
        """
        Determines whether the current object's expiration timestamp has elapsed based
        on the current time.

        Checks the `expiration_timestamp` attribute of the instance and compares it
        to the current timestamp retrieved from the system clock.

        :return: True if the instance's expiration timestamp is earlier than the current
                 timestamp, indicating expiration. Otherwise, False.
        :rtype: bool
        """
        return self.expiration_timestamp < datetime.datetime.now().timestamp()
