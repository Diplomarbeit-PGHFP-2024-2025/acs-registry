import datetime

from aca_protocols.station_register_protocol import (
    StationRegisterRequest,
    StationRegisterResponse,
)
from uagents import Context, Protocol

import os
from dotenv import load_dotenv
from acs_registry.mongodb.get_mongo_db import get_collection

load_dotenv()

station_collection = get_collection()

protocol = Protocol()


@protocol.on_message(model=StationRegisterRequest, replies=StationRegisterResponse)
async def station_register(ctx: Context, sender: str, request: StationRegisterRequest):
    ctx.logger.info(f"Sender: {sender} sent: {request.lat} {request.long}")

    ttl = int(os.getenv("TTL"))

    stations = station_collection.find()

    expiration_date = calculate_expiration_date(ttl)

    for station in stations:
        if station["address"] == sender:
            station_collection.update_one(
                {"address": station["address"]}, {"$set": {"expireAt": expiration_date}}
            )

            ctx.logger.info(f"TTL updated for {sender}")
            await ctx.send(sender, StationRegisterResponse(ttl=ttl))
            return

    station_collection.insert_one(
        {
            "address": sender,
            "location": {
                "type": "Point",
                "coordinates": [request.long, request.lat],
            },
            "expireAt": expiration_date,
        }
    )

    await ctx.send(sender, StationRegisterResponse(ttl=ttl))


def calculate_expiration_date(ttl: int) -> datetime.datetime:
    return datetime.datetime.now(datetime.UTC) + datetime.timedelta(seconds=ttl)
