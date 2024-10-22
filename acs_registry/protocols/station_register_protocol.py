from aca_protocols.station_register_protocol import (
    StationRegisterRequest,
    StationRegisterResponse,
)
from uagents import Context, Protocol

from domain.station import Station

import os
from dotenv import load_dotenv

from mongodb.get_mongo_db import get_collection

load_dotenv()

station_collection = get_collection()

protocol = Protocol()


@protocol.on_message(model=StationRegisterRequest, replies=StationRegisterResponse)
async def station_register(ctx: Context, sender: str, request: StationRegisterRequest):
    ctx.logger.info(f"Sender: {sender} sent: {request.lat} {request.long}")

    stations = station_collection.find()

    for station in stations:
        if station["address"] == sender:

            station_collection.update_one({"address": station["address"]}, {"$set":{"ttl": int(os.getenv("TTL"))}})
            ctx.logger.info(f"TTL updated for {sender}")
            await ctx.send(sender, StationRegisterResponse(ttl=int(os.getenv("TTL"))))
            return


    station_collection.insert_one({"address": sender,
                                   "location": {
                                       "type": "Point",
                                       "coordinates": [request.lat, request.long]
                                   },
                                   "ttl": int(os.getenv("TTL"))
                                   })


    await ctx.send(sender, StationRegisterResponse(ttl=int(os.getenv("TTL"))))
