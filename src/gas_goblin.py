from uagents import Agent, Context
from uagents.setup import fund_agent_if_low

from protocols.station_register_protocol import protocol as station_register_protocol

agent = Agent(
    name="gas-goblin",
    seed="GasGoblin1",
    port=8000,
    endpoint=["http://127.0.0.1:8000/submit"]
)
agent.include(station_register_protocol)
fund_agent_if_low(agent.wallet.address())


@agent.on_event("startup")
async def introduce_agent(ctx: Context):
    ctx.logger.info(f"Agent: {agent.name} ({agent.address})")


if __name__ == "__main__":
    agent.run()
