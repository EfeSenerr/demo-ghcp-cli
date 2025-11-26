# Migration Plan: Semantic Kernel to Microsoft Agent Framework

> **⚠️ AI-Generated Content Disclaimer**
> 
> This migration plan was drafted by AI (GitHub Copilot). While it is based on the latest available documentation and best practices, please verify all information, import paths, and API patterns against the official Microsoft Agent Framework documentation before implementing any changes. The AI may not have access to the most recent updates or changes to the framework.

## Overview

This document outlines the migration plan for `semantic_kernel_agents.py` from the current Semantic Kernel agent implementation to the Microsoft Agent Framework. Based on the latest documentation, Microsoft Agent Framework is the unified successor to Semantic Kernel and AutoGen, combining their strengths with new capabilities.

## Current Implementation Analysis

### Current File: `semantic_kernel_agents.py`

The current implementation uses:
- **Semantic Kernel Agent Framework** (`semantic_kernel.agents`)
- **ChatCompletionAgent** - For creating agents with chat completion capabilities
- **SequentialOrchestration** - For orchestrating agents in a sequential pipeline
- **InProcessRuntime** - For managing agent execution
- **OpenAIChatCompletion** connector with GitHub Models endpoint

### Current Code Structure:
```python
# Imports from Semantic Kernel
from semantic_kernel.agents import Agent, ChatCompletionAgent, SequentialOrchestration
from semantic_kernel.agents.runtime import InProcessRuntime
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.contents import ChatMessageContent

# OpenAI client configuration for GitHub Models
openai_client = AsyncOpenAI(
    base_url="https://models.github.ai/inference",
    api_key=os.environ["GITHUB_TOKEN"],
)

# Agent creation pattern
writer_agent = ChatCompletionAgent(
    name="WriterAgent",
    instructions="...",
    service=chat_client,
)

# Sequential orchestration
sequential_orchestration = SequentialOrchestration(
    members=agents,
    agent_response_callback=callback,
)

# Runtime execution
runtime = InProcessRuntime()
runtime.start()
result = await sequential_orchestration.invoke(task=prompt, runtime=runtime)
```

---

## Migration Plan

### Phase 1: Install Microsoft Agent Framework

**Action:** Update dependencies from `semantic-kernel` to `agent-framework`

```bash
# Remove old dependency
pip uninstall semantic-kernel

# Install new dependency
pip install agent-framework
```

**Note:** The Microsoft Agent Framework package is currently in public preview. Ensure you check the latest version and compatibility.

### Phase 2: Update Imports

**Current Imports:**
```python
from semantic_kernel.agents import Agent, ChatCompletionAgent, SequentialOrchestration
from semantic_kernel.agents.runtime import InProcessRuntime
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.contents import ChatMessageContent
```

**New Imports (Agent Framework):**
```python
# Import from Microsoft Agent Framework
# Note: Exact imports may vary - check latest documentation
from agent_framework import Agent, ChatCompletionAgent
from agent_framework.orchestration import SequentialOrchestration
from agent_framework.runtime import InProcessRuntime
from agent_framework.connectors.openai import OpenAIChatCompletion
from agent_framework.contents import ChatMessageContent
```

**Important:** The exact import paths for Microsoft Agent Framework should be verified against the latest [Microsoft Agent Framework Python repository](https://github.com/microsoft/agent-framework/tree/main/python) as the SDK is in active development.

### Phase 3: Update Agent Creation

The current agent creation pattern may need updates:

**Current Pattern:**
```python
chat_client = OpenAIChatCompletion(
    async_client=openai_client,
    ai_model_id="openai/gpt-4.1",
)

writer_agent = ChatCompletionAgent(
    name="WriterAgent",
    instructions="...",
    service=chat_client,
)
```

**Potential New Pattern (Agent Framework):**
- Consider using Azure AI Foundry services for new projects (as recommended)
- Use the new `service` configuration pattern if available
- Check if `plugins` parameter is now supported directly in constructor

### Phase 4: Update Orchestration Pattern

The Sequential Orchestration pattern should remain similar, but check for any API changes:

**Current Pattern:**
```python
sequential_orchestration = SequentialOrchestration(
    members=agents,
    agent_response_callback=callback,
)

runtime = InProcessRuntime()
runtime.start()

orchestration_result = await sequential_orchestration.invoke(
    task=prompt, 
    runtime=runtime
)
final_message = await orchestration_result.get(timeout=20)
```

**Potential Changes:**
- Verify the `SequentialOrchestration` class exists in Agent Framework
- Check for new orchestration patterns (graph-based architecture with executors and edges)
- Consider workflow-based orchestrations if they provide better control

### Phase 5: Update Thread/Context Management

Based on the Semantic Kernel RC migration guide, thread management has been updated:

**New Thread Management Pattern:**
```python
from agent_framework.agents import ChatHistoryAgentThread

# Thread-based state management
thread = ChatHistoryAgentThread()

response = await agent.get_response(
    messages="user input",
    thread=thread,
)
# Thread is returned with response for continuation
thread = response.thread
```

### Phase 6: Update Response Callback

**Current Callback:**
```python
async def skAgent_response_callback(
    message: ChatMessageContent | Sequence[ChatMessageContent],
) -> None:
    # ... handle message
```

**New Callback Pattern:**
- May need to use `agent_response_callback` parameter
- Human-in-the-loop pattern available via `human_response_function`

---

## Key Differences Summary

| Feature | Current (Semantic Kernel) | New (Agent Framework) |
|---------|---------------------------|----------------------|
| Package | `semantic-kernel` | `agent-framework` |
| Primary Focus | SK-specific patterns | Unified framework (SK + AutoGen) |
| Service Config | Via constructor | Via constructor + Azure AI Foundry recommended |
| Thread Management | InProcessRuntime | Thread-based (`AgentThread`) |
| Orchestration | `SequentialOrchestration` | Graph-based workflows available |
| Middleware | N/A | Middleware support for intercepting actions |
| Context | Limited | Context providers for agent memory |

---

## Recommended Actions

1. **Before Migration:**
   - [ ] Pin current `semantic-kernel` version for stability
   - [ ] Review [Microsoft Agent Framework documentation](https://learn.microsoft.com/agent-framework/overview/agent-framework-overview)
   - [ ] Check [Migration Guide from Semantic Kernel](https://learn.microsoft.com/agent-framework/migration-guide/from-semantic-kernel/)
   - [ ] Review Python samples in [Agent Framework repository](https://github.com/microsoft/agent-framework/tree/main/python/samples)

2. **During Migration:**
   - [ ] Update package dependencies
   - [ ] Update imports
   - [ ] Update agent creation code
   - [ ] Update orchestration patterns
   - [ ] Update thread/context management
   - [ ] Update response handling

3. **After Migration:**
   - [ ] Test all agent workflows
   - [ ] Verify GitHub Models integration works
   - [ ] Update documentation
   - [ ] Consider leveraging new Agent Framework features (middleware, context providers, workflows)

---

## Alternative: Stay with Semantic Kernel RC APIs

If Microsoft Agent Framework is not yet stable or doesn't meet your needs, you can alternatively migrate to the latest **Semantic Kernel Release Candidate APIs** which have also been significantly updated:

### Key Updates in SK Python 1.26.1+:

1. **Consolidated Imports:**
```python
from semantic_kernel.agents import (
    ChatCompletionAgent,
    SequentialOrchestration,
    ChatHistoryAgentThread,
)
```

2. **New Thread-Based Invocation:**
```python
response = await agent.get_response(messages="user input", thread=thread)
thread = response.thread
```

3. **Direct Plugin Support:**
```python
agent = ChatCompletionAgent(
    service=AzureChatCompletion(),
    name="<name>",
    instructions="<instructions>",
    plugins=[SamplePlugin()],
)
```

---

## Notes

- Microsoft Agent Framework is currently in **public preview** and changes rapidly
- Always consult the latest documentation before implementing changes
- The exact API may differ from what's documented here
- Consider creating a feature branch for testing the migration before merging
- GitHub Models endpoint integration should continue to work with the new framework

---

## Resources

- [Microsoft Agent Framework Overview](https://learn.microsoft.com/agent-framework/overview/agent-framework-overview)
- [Agent Framework Python Repository](https://github.com/microsoft/agent-framework/tree/main/python)
- [Agent Framework Python Samples](https://github.com/microsoft/agent-framework/tree/main/python/samples)
- [Semantic Kernel Agent Framework RC Migration Guide](https://learn.microsoft.com/en-us/semantic-kernel/support/migration/agent-framework-rc-migration-guide)
- [Sequential Orchestration Documentation](https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/agent-orchestration/sequential)
