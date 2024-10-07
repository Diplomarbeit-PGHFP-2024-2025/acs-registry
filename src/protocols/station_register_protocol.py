from aca_protocols.station_register_protocol import StationRegisterRequest, StationRegisterResponse, protocol
from uagents import Context

from domain.station import Station


@protocol.on_message(model=StationRegisterRequest, replies=StationRegisterResponse)
async def station_register(ctx: Context, sender: str, request: StationRegisterRequest):
    ctx.logger.info(f"Sender: {sender} sent: {request.lat} {request.long}")

    # todo: store stations in DB
    stations: list[Station] = ctx.storage.get("stations")

    if stations is None:
        stations = []

    # todo: dedupe Stations
    stations.append(Station(request.lat, request.long, sender))
    ctx.storage.set("stations", stations)

    await ctx.send(sender, StationRegisterResponse())
