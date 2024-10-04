from uagents import Context, Protocol, Model

from domain.station import Station


class StationQueryRequest(Model):
    lat: float
    long: float
    radius: float


class StationQueryResponse(Model):
    stations: list[str]


protocol = Protocol()


@protocol.on_message(model=StationQueryRequest, replies=StationQueryResponse)
async def station_query(ctx: Context, sender: str, request: StationQueryRequest):
    ctx.logger.info(f"Car: {sender} requested: {request}")

    stations: list[Station] = ctx.storage.get("stations")

    result = []

    for station in stations:
        distance_square = (station[0] - request.lat) ** 2 + (
            station[1] - request.long
        ) ** 2

        if distance_square < request.radius**2:
            result.append(station[2])

    await ctx.send(sender, StationQueryResponse(stations=result))
