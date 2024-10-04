from uagents import Agent, Context, Protocol, Model
from ai_engine import UAgentResponse, UAgentResponseType


class StationRequest(Model):
    msg: str


class StationResponse(Model):
    msg: str


register_station_protocol = Protocol()


@register_station_protocol.on_message(model=StationRequest, replies=StationResponse)
async def station_register(ctx: Context, sender: str, msg: StationRequest):
    print(f"Sender: {sender} sent: {msg.msg}")
    await ctx.send(
        sender, StationResponse(msg=f"Ack: {msg.msg}")
    )

