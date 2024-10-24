import socket

from uagents import Agent, Context
from uagents.setup import fund_agent_if_low

from aca_protocols.station_query_protocol import (
    StationQueryRequest,
    StationQueryResponse,
)

from aca_protocols.acs_registry_id import acs_id

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

agent = Agent(
    name="car",
    seed="Car1",
    port=8002,
    endpoint=["http://{}:8002/submit".format(IPAddr)],
)

fund_agent_if_low(agent.wallet.address())


@agent.on_event("startup")
async def introduce_agent(ctx: Context):
    ctx.logger.info(f"Agent: {agent.name} ({agent.address})")
    await ctx.send(
        acs_id,
        StationQueryRequest(lat=1.0, long=1.0, radius=5.0),
    )


@agent.on_message(StationQueryResponse)
async def on_is_registered(ctx: Context, sender: str, msg: StationQueryResponse):
    ctx.logger.info(f"stations: ${msg}")


if __name__ == "__main__":
    agent.run()
