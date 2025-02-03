import tanjun
import os
from typing import Final

component = tanjun.Component().load_from_scope()


@component.with_message_command
@tanjun.as_message_command("eval", "ev")
async def admin_eval(ctx: tanjun.abc.MessageContext):
    PREFIX: Final[str] = os.environ.get("BOT_PREFIX")
    OWNER: Final[str] = os.environ.get("OWNER_ID")

    prompt: str = " ".join(
        ctx.message.content.removeprefix(PREFIX).strip().split(" ")[1:]
    )

    if str(ctx.author.id) == OWNER:
        eval(prompt)


@tanjun.as_loader
def load(client: tanjun.abc.Client) -> None:
    client.add_component(component)


@tanjun.as_unloader
def unload(client: tanjun.Client) -> None:
    client.remove_component(component)
