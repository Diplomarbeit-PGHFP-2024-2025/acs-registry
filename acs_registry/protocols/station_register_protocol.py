import datetime

from aca_protocols.station_register_protocol import (
    StationRegisterRequest,
    StationRegisterResponse,
)
from uagents import Context, Protocol

import os
from dotenv import load_dotenv

from .station_data_object import StationDataObject

load_dotenv()

protocol = Protocol()


@protocol.on_message(model=StationRegisterRequest, replies=StationRegisterResponse)
async def station_register(ctx: Context, sender: str, request: StationRegisterRequest):
    ctx.logger.info(f"Sender: {sender} sent: {request.lat} {request.long}")

    ttl = int(os.getenv("TTL"))

    expiration_date = calculate_expiration_date(ttl)

    stations: list[StationDataObject] = StationDataObject.list_from_json(
        ctx.storage.get("stations")
    )

    index = -1
    for i, station in enumerate(stations):
        if station.address == sender:
            index = i
            break

    to_save = StationDataObject(
        address=sender,
        expiration_timestamp=expiration_date,
        coordinates=(request.lat, request.long),
    )

    if index == -1:
        stations.append(to_save)
        msg = f"Station added for {sender}"
    else:
        stations[index] = to_save
        msg = f"TTL updated for {sender}"

    ctx.storage.set("stations", StationDataObject.list_to_json(stations))

    ctx.logger.info(msg)

    await ctx.send(sender, StationRegisterResponse(ttl=ttl))


def calculate_expiration_date(ttl: int) -> float:
    """
    Calculates the expiration date timestamp based on the provided time-to-live (TTL) value.
    :param ttl: The time-to-live value in seconds
    :return: The expiration date as a UNIX-like timestamp in float format,
    :rtype: float
    """
    return (
        datetime.datetime.now(datetime.UTC) + datetime.timedelta(seconds=ttl)
    ).timestamp()
