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
    stations = filter_stations(stations, request)

    await ctx.send(sender, StationQueryResponse(stations=stations))


def filter_stations(stations: list[Station], request: StationQueryRequest) -> list[str]:
    def is_in_range(station: Station):
        lat_dif = station[0] - request.lat
        long_dif = station[1] - request.long
        distance_square = lat_dif**2 + long_dif**2

        return distance_square < request.radius**2

    def to_address(station: Station):
        return station[2]

    stations = filter(is_in_range, stations)
    stations = map(to_address, stations)

    return list(stations)
