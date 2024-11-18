import socket

from uagents import Agent, Context
from uagents.setup import fund_agent_if_low

from protocols.station_query_protocol import protocol as station_query_protocol
from protocols.station_register_protocol import protocol as station_register_protocol

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


if __name__ == "__main__":
    agent.run()
