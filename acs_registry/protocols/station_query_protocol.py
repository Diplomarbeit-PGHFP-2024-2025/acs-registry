from aca_protocols.station_query_protocol import (
    StationQueryRequest,
    StationQueryResponse,
)
from uagents import Context, Protocol

from mongodb.get_mongo_db import get_collection

station_collection = get_collection()

protocol = Protocol()


@protocol.on_message(model=StationQueryRequest, replies=StationQueryResponse)
async def station_query(ctx: Context, sender: str, request: StationQueryRequest):
    ctx.logger.info(f"Car: {sender} requested: {request}")

    stations_list = filter_stations2(station_collection, request)

    await ctx.send(sender, StationQueryResponse(stations=stations_list))


def filter_stations2(collection, request: StationQueryRequest) -> list[str]:
    cursor = collection.find(
        {
            "location": {
                "$near": {
                    "$geometry": {
                        "type": "Point",
                        "coordinates": [request.long, request.lat],
                    },
                    "$minDistance": 0,
                    "$maxDistance": request.radius,  # in meters
                }
            }
        },
        {"_id": 0, "address": 1},
    )

    return station_cursor_to_address(cursor)


def station_cursor_to_address(cursor) -> list[str]:
    stations_list: list[str] = []
    for station in cursor:
        stations_list.append(station["address"])

    return stations_list
