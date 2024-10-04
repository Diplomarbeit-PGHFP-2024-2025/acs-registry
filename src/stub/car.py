from uagents import Agent, Context
from uagents.setup import fund_agent_if_low

from protocols.station_query_protocol import StationQueryRequest, StationQueryResponse

agent = Agent(
    name="car",
    seed="Car1",
    port=8002,
    endpoint=["http://127.0.0.1:8002/submit"],
)

fund_agent_if_low(agent.wallet.address())


@agent.on_event("startup")
async def introduce_agent(ctx: Context):
    ctx.logger.info(f"Agent: {agent.name} ({agent.address})")
    await ctx.send(
        "agent1qw9sc5v7c0zk98xf0ht7s8ga7gteyf8lekgfpgtlct3zq8z4rhx7773t546",
        StationQueryRequest(lat=1.0, long=1.0, radius=5.0),
    )


@agent.on_message(StationQueryResponse)
async def on_is_registered(ctx: Context, sender: str, msg: StationQueryResponse):
    ctx.logger.info(f"stations: ${msg}")


if __name__ == "__main__":
    agent.run()
