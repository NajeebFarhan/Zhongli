import tanjun
import requests
import json
import os
from typing import Final

component = tanjun.Component().load_from_scope()


async def get_reponse(user_prompt: str) -> str:
    OLLAMA_API_URL: Final[str] = os.environ.get("LLM_URL")

    with open(os.path.abspath("bot/prompt.json"), "r") as f:
        prompt = json.load(f)

    prompt["prompt"] = user_prompt

    response = requests.post(OLLAMA_API_URL, json=prompt)

    data = response.json()
    data["response"] = data["response"].split("</think>")[1].strip()

    return data


@component.with_message_command
@tanjun.as_message_command("text", "description")
async def message_command(ctx: tanjun.abc.MessageContext) -> None:
    PREFIX = os.environ.get("BOT_PREFIX")
    prompt = (
        ctx.message.content.removeprefix(PREFIX).strip().removeprefix("text").strip()
    )

    data = await get_reponse(prompt)

    await ctx.respond(data["response"])


@tanjun.as_loader
def load(client: tanjun.abc.Client) -> None:
    client.add_component(component)


@tanjun.as_unloader
def unload(client: tanjun.Client) -> None:
    client.remove_component(component)
