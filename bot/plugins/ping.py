import tanjun

component = tanjun.Component().load_from_scope()


@component.with_slash_command
@tanjun.as_slash_command("ping", "get a pong")
async def ping(ctx: tanjun.abc.SlashContext):
    await ctx.respond("Pong!")


@tanjun.as_loader
def load(client: tanjun.abc.Client) -> None:
    client.add_component(component)


@tanjun.as_unloader
def unload(client: tanjun.Client) -> None:
    client.remove_component(component)
