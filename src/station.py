from uagents import Agent, Context
from uagents.setup import fund_agent_if_low

from things.station_protocol import StationResponse, StationRequest

agent = Agent(
    name="station",
    seed="Station1",
    port=8001,
    endpoint=["http://127.0.0.1:8001/submit"]
)
#
fund_agent_if_low(agent.wallet.address())


@agent.on_event("startup")
async def introduce_agent(ctx: Context):
    ctx.logger.info(f"Hello, I'm agent {agent.name} and my address is {agent.address}.")


@agent.on_interval(1.0)
async def interval(ctx: Context):
    await ctx.send("agent1qw9sc5v7c0zk98xf0ht7s8ga7gteyf8lekgfpgtlct3zq8z4rhx7773t546",
                   StationRequest(msg=f"Hello this is {agent.name} with address {agent.address}"))

@agent.on_message(StationResponse)
async def getMsg(ctx: Context, sender: str, msg: StationResponse):
    print(f"Sender: {sender} sent: {msg.msg}")


if __name__ == "__main__":
    agent.run()
