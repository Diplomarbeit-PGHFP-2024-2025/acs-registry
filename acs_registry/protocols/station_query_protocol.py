from aca_protocols.station_query_protocol import (
    StationQueryRequest,
    StationQueryResponse,
)
from uagents import Context, Protocol

from .station_data_object import StationDataObject

protocol = Protocol()


@protocol.on_message(model=StationQueryRequest, replies=StationQueryResponse)
async def station_query(ctx: Context, sender: str, request: StationQueryRequest):
    ctx.logger.info(f"Car: {sender} requested: {request}")

    stations_list = filter_stations(ctx.storage.get("stations"), request)
    ctx.logger.info(f"Found {stations_list} stations")

    await ctx.send(sender, StationQueryResponse(stations=stations_list))


def filter_stations(
    stations: list[StationDataObject], request: StationQueryRequest
) -> list[str]:
    return [
        station.address
        for station in filter_stations_within_radius(
            stations, (request.lat, request.long), request.radius
        )
    ]


def euclidean_distance(
    coord1: tuple[float, float], coord2: tuple[float, float]
) -> float:
    """
    Calculate the Euclidean distance between two points in a plane.
    :param coord1: Tuple (x1, y1) for the first point.
    :param coord2: Tuple (x2, y2) for the second point.
    :return: Distance between the two points.
    """
    x1, y1 = coord1
    x2, y2 = coord2
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


def filter_stations_within_radius(
    stations: list[StationDataObject], center: tuple[float, float], radius: float
) -> list[StationDataObject]:
    """
    Filters StationDataObject instances within a specific radius on a 2D plane.
    :param stations: List of StationDataObject instances.
    :param center: Tuple (x, y) of the center point.
    :param radius: Radius in the same units as coordinates.
    :return: List of StationDataObject instances within the radius.
    """
    return [
        station
        for station in stations
        if euclidean_distance(station.coordinates, center) <= radius
    ]
