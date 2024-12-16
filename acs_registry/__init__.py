import socket

from uagents import Agent, Context
from uagents.setup import fund_agent_if_low

from protocols.station_query_protocol import protocol as station_query_protocol
from protocols.station_register_protocol import protocol as station_register_protocol

from protocols.station_data_object import StationDataObject

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

agent = Agent(
    name="acs-registry",
    seed="ACSRegistry1",
    port=8000,
    endpoint=["http://{}:8000/submit".format(IPAddr)],
)

fund_agent_if_low(str(agent.wallet.address()))

agent.include(station_register_protocol)
agent.include(station_query_protocol)


@agent.on_event("startup")
async def introduce_agent(ctx: Context):
    ctx.logger.info(f"Agent: {agent.name} ({agent.address})")
    ctx.storage.set("stations", [])


@agent.on_interval(period=10)
async def check_expired_stations(ctx: Context):
    stations: list[StationDataObject] = StationDataObject.list_from_json(
        ctx.storage.get("stations")
    )

    for station in stations:
        if station.is_expired():
            ctx.logger.info(f"Station expired: {station.address}")
            stations.remove(station)

    ctx.storage.set("stations", StationDataObject.list_to_json(stations))

    ctx.logger.info(f"Stations after expire check: {len(stations)}")


if __name__ == "__main__":
    agent.run()
