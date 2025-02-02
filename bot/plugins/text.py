import hikari
import tanjun
import requests
from typing import Final

component = tanjun.Component().load_from_scope()

# OLLAMA_API_URL: Final[str] = "http://localhost:11434/api/generate"


# @component.with_slash_command
# @tanjun.as_slash_command("text", "Gives an AI generated response based on your prompt")
# @tanjun.with_option("message")
# async def test(ctx: tanjun.abc.MessageContext) -> None:
#     await ctx.respond("Placeholder text. It will be an AI reponse next time")
#     # print(ctx.message)


# @tanjun.with_option(
#     "reason", "--reason", "-r", default=None
# )  # This can be triggered as --reason or -r
# @tanjun.with_multi_option(
#     "users", "--user", "-u", default=None
# )  # This can be triggered as --user or -u
# @tanjun.with_greedy_argument("content")
# @tanjun.with_argument("days", converters=int)
@component.with_command
@tanjun.as_message_command("text", "description")
async def message_command(ctx: tanjun.abc.MessageContext) -> None:
    await ctx.respond("testing")


@tanjun.as_loader
def load(client: tanjun.abc.Client) -> None:
    client.add_component(component)


@tanjun.as_unloader
def unload(client: tanjun.Client) -> None:
    client.remove_component(component)
