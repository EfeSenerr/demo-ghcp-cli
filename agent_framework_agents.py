# Copyright (c) Microsoft. All rights reserved.

"""Sequential orchestration using Microsoft Agent Framework.

This module demonstrates a migration from Semantic Kernel to Microsoft Agent Framework,
showcasing two agents (writer and reviewer) working together in a sequential workflow.
"""

import asyncio
import os
from typing import Any

from dotenv import load_dotenv

from agent_framework import ChatAgent, SequentialBuilder, WorkflowOutputEvent, ChatMessage, Role
from agent_framework.openai import OpenAIChatClient

load_dotenv()

PROMPT = "Write a tagline for a budget-friendly eBike."


def create_chat_client() -> OpenAIChatClient:
    """Create an OpenAI chat client configured for GitHub Models API."""
    return OpenAIChatClient(
        api_key=os.environ["GITHUB_TOKEN"],
        base_url="https://models.github.ai/inference",
        model_id="openai/gpt-4.1",
    )


def build_agents(chat_client: OpenAIChatClient) -> list[ChatAgent]:
    """Create the writer and reviewer agents.
    
    Args:
        chat_client: The OpenAI chat client to use for the agents.
        
    Returns:
        A list containing the writer and reviewer agents.
    """
    writer = chat_client.create_agent(
        name="writer",
        instructions=(
            "You are a concise copywriter. Provide a single, punchy marketing sentence based on the prompt."
        ),
    )

    reviewer = chat_client.create_agent(
        name="reviewer",
        instructions=(
            "You are a thoughtful reviewer. Give brief feedback on the previous assistant message."
        ),
    )

    return [writer, reviewer]


async def run_agent_framework_example(prompt: str) -> str:
    """Run the sequential workflow with writer and reviewer agents.
    
    Args:
        prompt: The task prompt for the agents to process.
        
    Returns:
        The final text result from the workflow.
    """
    chat_client = create_chat_client()
    agents = build_agents(chat_client)
    
    # Build sequential workflow: writer -> reviewer
    workflow = SequentialBuilder().participants(agents).build()
    
    # Run the workflow and process events
    output_event: WorkflowOutputEvent | None = None
    async for event in workflow.run_stream(prompt):
        if isinstance(event, WorkflowOutputEvent):
            output_event = event
    
    if output_event:
        # Print the conversation flow
        print("===== Conversation Flow =====")
        messages: list[ChatMessage] | Any = output_event.data
        for i, msg in enumerate(messages, start=1):
            name = msg.author_name or ("assistant" if msg.role == Role.ASSISTANT else "user")
            print(f"# {name}\n{msg.text}\n")
        
        # Return the last assistant message as the final result
        assistant_messages = [m for m in messages if m.role == Role.ASSISTANT]
        if assistant_messages:
            return assistant_messages[-1].text
    
    return ""


async def main() -> None:
    """Main entry point for the Agent Framework sequential orchestration demo."""
    print("===== Agent Framework Sequential =====")
    final_text = await run_agent_framework_example(PROMPT)
    print("===== Final Result =====")
    print(final_text)


if __name__ == "__main__":
    asyncio.run(main())
