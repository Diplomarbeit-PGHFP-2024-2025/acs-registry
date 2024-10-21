from uagents import Agent, Context
from uagents.setup import fund_agent_if_low

from mongodb.station_collection import collection
from mongodb.get_mongo_db import get_collection
from protocols.station_register_protocol import protocol as station_register_protocol
from protocols.station_query_protocol import protocol as station_query_protocol



agent = Agent(
    name="acs-registry",
    seed="ACSRegistry1",
    port=8000,
    endpoint=["http://127.0.0.1:8000/submit"],
)

fund_agent_if_low(agent.wallet.address())

agent.include(station_register_protocol)
agent.include(station_query_protocol)


@agent.on_event("startup")
async def introduce_agent(ctx: Context):
    ctx.logger.info(f"Agent: {agent.name} ({agent.address})")
    collection.collection = get_collection()


if __name__ == "__main__":
    agent.run()
