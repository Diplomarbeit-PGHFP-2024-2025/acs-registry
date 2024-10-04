from uagents import Context, Protocol, Model

from domain.station import Station


class StationRegisterRequest(Model):
    lat: float
    long: float


class StationRegisterResponse(Model):
    pass


protocol = Protocol()


@protocol.on_message(model=StationRegisterRequest, replies=StationRegisterResponse)
async def station_register(ctx: Context, sender: str, request: StationRegisterRequest):
    ctx.logger.info(f"Sender: {sender} sent: {request.lat} {request.long}")

    stations: list[Station] = ctx.storage.get("stations")

    if stations is None:
        stations = []

    # todo: dedupe Stations
    stations.append(Station(request.lat, request.long, sender))
    ctx.storage.set("stations", stations)

    await ctx.send(sender, StationRegisterResponse())
