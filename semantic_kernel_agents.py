# Copyright (c) Microsoft. All rights reserved.

"""Side-by-side sequential orchestrations for Agent Framework and Semantic Kernel."""

import asyncio
from collections.abc import Sequence
from typing import cast
import os

from azure.identity import AzureCliCredential
from semantic_kernel.agents import Agent, ChatCompletionAgent, SequentialOrchestration
from semantic_kernel.agents.runtime import InProcessRuntime
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion 
from semantic_kernel.contents import ChatMessageContent

from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

PROMPT = "Write a tagline for a budget-friendly eBike."

openaiClient = AsyncOpenAI(
    base_url = "https://models.github.ai/inference",
    api_key = os.environ["GITHUB_TOKEN"],
    default_query = {
        "api-version": "2024-08-01-preview",
    },
)

chat_client = OpenAIChatCompletion(
        async_client=openaiClient,
        ai_model_id="openai/gpt-4.1",
    )

######################################################################
# Semantic Kernel orchestration path
######################################################################


def build_semantic_kernel_agents() -> list[Agent]:
    credential = AzureCliCredential()

    writer_agent = ChatCompletionAgent(
        name="WriterAgent",
        instructions=("You are a concise copywriter. Provide a single, punchy marketing sentence based on the prompt."),
        service=chat_client,
    )

    reviewer_agent = ChatCompletionAgent(
        name="ReviewerAgent",
        instructions=("You are a thoughtful reviewer. Give brief feedback on the previous assistant message."),
        service=chat_client,
    )

    return [writer_agent, reviewer_agent]


async def sk_agent_response_callback(
    message: ChatMessageContent | Sequence[ChatMessageContent],
) -> None:
    if isinstance(message, ChatMessageContent):
        messages: Sequence[ChatMessageContent] = [message]
    elif isinstance(message, Sequence) and not isinstance(message, (str, bytes)):
        messages = list(message)
    else:
        messages = [cast(ChatMessageContent, message)]

    for item in messages:
        content = item.content or ""
        print(f"# {item.name}\n{content}\n")

async def run_semantic_kernel_example(prompt: str) -> str:
    sequential_orchestration = SequentialOrchestration(
        members=build_semantic_kernel_agents(),
        agent_response_callback=sk_agent_response_callback,
    )

    runtime = InProcessRuntime()
    runtime.start()

    try:
        orchestration_result = await sequential_orchestration.invoke(task=prompt, runtime=runtime)
        final_message = await orchestration_result.get(timeout=20)
        if isinstance(final_message, ChatMessageContent):
            return final_message.content or ""
        return str(final_message)
    finally:
        await runtime.stop_when_idle()

async def main() -> None:
    print("===== Semantic Kernel Sequential =====")
    final_text = await run_semantic_kernel_example(PROMPT)
    print(final_text)


if __name__ == "__main__":
    asyncio.run(main())