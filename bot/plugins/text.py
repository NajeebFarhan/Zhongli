import tanjun
import requests
import os
from typing import Final

from .prompt import get_prompt

component = tanjun.Component().load_from_scope()


def get_reponse(id: str, user_prompt: str) -> str:
    OLLAMA_API_URL: Final[str] = os.environ.get("LLM_URL")

    prompt = get_prompt(id)

    user_message = {"role": "user", "content": user_prompt}
    prompt["messages"].append(user_message)

    prompt["prompt"] = "\n".join(
        [f"{msg['role'].capitalize()}: {msg['content']}" for msg in prompt["messages"]]
    )

    response = requests.post(OLLAMA_API_URL, json=prompt)

    if response.status_code != 200:
        raise Exception("LLM not loaded yet")

    data = response.json()
    data["response"] = data["response"].split("</think>")[-1].strip()

    assistant_message = {"role": "assistant", "content": data["response"]}
    prompt["messages"].append(assistant_message)

    return data


@component.with_message_command
@tanjun.as_message_command("text", "txt")
async def text(ctx: tanjun.abc.MessageContext) -> None:
    if ctx.author.is_bot:
        return

    PREFIX = os.environ.get("BOT_PREFIX")
    prompt = (
        ctx.message.content.removeprefix(PREFIX).strip().removeprefix("text").strip()
    )

    msg = await ctx.respond("Hold on! Wait a minute!...")

    data = get_reponse(ctx.author.id, prompt)

    await msg.edit(data["response"])


@tanjun.as_loader
def load(client: tanjun.abc.Client) -> None:
    client.add_component(component)


@tanjun.as_unloader
def unload(client: tanjun.Client) -> None:
    client.remove_component(component)
