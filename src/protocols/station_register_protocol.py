from uagents import Context, Protocol, Model


class StationRequest(Model):
    lat: float
    long: float


class StationResponse(Model):
    pass


protocol = Protocol()


@protocol.on_message(model=StationRequest, replies=StationResponse)
async def station_register(ctx: Context, sender: str, msg: StationRequest):
    print(f"Sender: {sender} sent: {msg.lat} {msg.long}")
    await ctx.send(sender, StationResponse())
