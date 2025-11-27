# Copyright (c) Microsoft. All rights reserved.

"""Sequential workflow using Agent Framework with OpenAI agents."""

import asyncio
import os

from agent_framework import AgentRunUpdateEvent, WorkflowBuilder, WorkflowOutputEvent
from agent_framework.openai import OpenAIChatClient

from dotenv import load_dotenv

load_dotenv()

PROMPT = "Write a tagline for a budget-friendly eBike."


def build_agent_framework_agents():
    """Build writer and reviewer agents using Agent Framework with GitHub Models endpoint."""
    chat_client = OpenAIChatClient(
        base_url="https://models.github.ai/inference",
        api_key=os.environ["GITHUB_TOKEN"],
        model_id="openai/gpt-4.1",
    )

    writer_agent = chat_client.create_agent(
        name="WriterAgent",
        instructions="You are a concise copywriter. Provide a single, punchy marketing sentence based on the prompt.",
    )

    reviewer_agent = chat_client.create_agent(
        name="ReviewerAgent",
        instructions="You are a thoughtful reviewer. Give brief feedback on the previous assistant message.",
    )

    return writer_agent, reviewer_agent


async def run_agent_framework_example(prompt: str) -> str:
    """Run the sequential workflow using Agent Framework."""
    writer_agent, reviewer_agent = build_agent_framework_agents()

    # Build the workflow with sequential edges: writer -> reviewer
    workflow = (
        WorkflowBuilder()
        .set_start_executor(writer_agent)
        .add_edge(writer_agent, reviewer_agent)
        .build()
    )

    # Execute the workflow and process events
    final_result = ""
    last_executor_id: str | None = None

    async for event in workflow.run_stream(prompt):
        if isinstance(event, AgentRunUpdateEvent):
            # Print agent responses as they stream
            executor_id = event.executor_id
            if executor_id != last_executor_id:
                if last_executor_id is not None:
                    print()  # New line between agents
                print(f"# {executor_id}")
                last_executor_id = executor_id
            if event.data:
                # AgentRunUpdateEvent.data is AgentRunResponseUpdate with .text property
                text = event.data.text if hasattr(event.data, 'text') else str(event.data)
                print(text, end="", flush=True)
        elif isinstance(event, WorkflowOutputEvent):
            # Extract text from WorkflowOutputEvent.data
            if event.data:
                final_result = event.data.text if hasattr(event.data, 'text') else str(event.data)

    print()  # Final newline
    return final_result


async def main() -> None:
    print("===== Agent Framework Sequential Workflow =====")
    final_text = await run_agent_framework_example(PROMPT)
    print(f"\n===== Final Result =====\n{final_text}")


if __name__ == "__main__":
    asyncio.run(main())
