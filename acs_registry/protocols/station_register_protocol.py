import datetime

from aca_protocols.station_register_protocol import (
    StationRegisterRequest,
    StationRegisterResponse,
)
from uagents import Context, Protocol

import os
from dotenv import load_dotenv
from mongodb.get_mongo_db import get_collection

load_dotenv()

station_collection = get_collection()

protocol = Protocol()


@protocol.on_message(model=StationRegisterRequest, replies=StationRegisterResponse)
async def station_register(ctx: Context, sender: str, request: StationRegisterRequest):
    ctx.logger.info(f"Sender: {sender} sent: {request.lat} {request.long}")

    ttl = int(os.getenv("TTL"))

    expiration_date = calculate_expiration_date(ttl)

    result = station_collection.update_one(
        {"address": sender},
        {
            "$set": {
                "expireAt": expiration_date,
                "location": {
                    "type": "Point",
                    "coordinates": [request.long, request.lat],
                },
            }
        },
        upsert=True,
    )

    if result.matched_count > 0:
        ctx.logger.info(f"TTL updated for {sender}")
    else:
        ctx.logger.info(f"New station added for {sender}")

    await ctx.send(sender, StationRegisterResponse(ttl=ttl))


def calculate_expiration_date(ttl: int) -> datetime.datetime:
    return datetime.datetime.now(datetime.UTC) + datetime.timedelta(seconds=ttl)
