from aca_protocols.station_register_protocol import (
    StationRegisterRequest,
    StationRegisterResponse,
)
from uagents import Context, Protocol

from domain.station import Station

import os
from dotenv import load_dotenv

from mongodb.station_collection import station_collection

load_dotenv()

protocol = Protocol()


@protocol.on_message(model=StationRegisterRequest, replies=StationRegisterResponse)
async def station_register(ctx: Context, sender: str, request: StationRegisterRequest):
    ctx.logger.info(f"Sender: {sender} sent: {request.lat} {request.long}")

    # todo: store stations in DB
    stations: list[Station] = ctx.storage.get("stations")

    stations = station_collection.find()

    if stations is None:
        stations = []

    for station in stations:
        if station.address == sender:
            # todo: update TTL in DB
            ctx.logger.info(f"TTL updated for {sender}")
            await ctx.send(sender, StationRegisterResponse(ttl=os.getenv("TTL")))
            return

    stations.append(Station(request.lat, request.long, sender))

    station_collection.insert_one({"address": sender,
                                   "location": {
                                       "type": "Point",
                                       "coordinates": [request.lat, request.long]
                                   }
                                   })

    ctx.storage.set("stations", stations)

    await ctx.send(sender, StationRegisterResponse(ttl=os.getenv("TTL")))
