# Migration Plan: Semantic Kernel to Microsoft Agent Framework

## Overview

This document outlines the migration plan from Semantic Kernel to Microsoft Agent Framework for the existing PoC that demonstrates two agents solving tasks collaboratively using sequential orchestration.

## Current Implementation (Semantic Kernel)

The current `semantic_kernel_agents.py` uses:
- `ChatCompletionAgent` from `semantic_kernel.agents`
- `SequentialOrchestration` for multi-agent coordination
- `InProcessRuntime` for execution
- `OpenAIChatCompletion` connector with GitHub Models API

### Current Architecture
```
WriterAgent → ReviewerAgent → Final Result
```

## Target Implementation (Microsoft Agent Framework)

The migrated `agent_framework_agents.py` will use:
- `ChatAgent` with `OpenAIChatClient` from `agent_framework`
- `SequentialBuilder` for workflow orchestration
- Event-based streaming with `WorkflowOutputEvent`

### Target Architecture
```
writer (ChatAgent) → reviewer (ChatAgent) → WorkflowCompletedEvent
```

## Migration Checklist

### 1. Package Dependencies
- [ ] Replace `semantic-kernel` with `agent-framework`
- [ ] Keep `openai` for custom client configuration
- [ ] Keep `python-dotenv` for environment loading
- [ ] Remove `azure-identity` if not needed for Azure authentication

### 2. Import Changes
| Semantic Kernel | Agent Framework |
|-----------------|-----------------|
| `from semantic_kernel.agents import ChatCompletionAgent` | `from agent_framework import ChatAgent` |
| `from semantic_kernel.agents import SequentialOrchestration` | `from agent_framework import SequentialBuilder` |
| `from semantic_kernel.agents.runtime import InProcessRuntime` | (not needed - handled internally) |
| `from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion` | `from agent_framework.openai import OpenAIChatClient` |

### 3. Agent Creation Changes
**Before (Semantic Kernel):**
```python
writer_agent = ChatCompletionAgent(
    name="WriterAgent",
    instructions="...",
    service=chat_client,
)
```

**After (Agent Framework):**
```python
writer = chat_client.create_agent(
    name="writer",
    instructions="...",
)
```

### 4. Orchestration Changes
**Before (Semantic Kernel):**
```python
sequential_orchestration = SequentialOrchestration(
    members=build_semantic_kernel_agents(),
    agent_response_callback=sk_agent_response_callback,
)
runtime = InProcessRuntime()
runtime.start()
result = await sequential_orchestration.invoke(task=prompt, runtime=runtime)
```

**After (Agent Framework):**
```python
workflow = SequentialBuilder().participants([writer, reviewer]).build()
async for event in workflow.run_stream(prompt):
    if isinstance(event, WorkflowOutputEvent):
        # Process final result
```

### 5. Response Handling Changes
**Before:** Callback-based with `agent_response_callback`
**After:** Event stream-based with `WorkflowOutputEvent` and `AgentRunUpdateEvent`

## Key Differences

| Feature | Semantic Kernel | Agent Framework |
|---------|-----------------|-----------------|
| Agent base class | `ChatCompletionAgent` | `ChatAgent` |
| Orchestration | `SequentialOrchestration` | `SequentialBuilder` |
| Runtime | Explicit `InProcessRuntime` | Built-in to workflow |
| Response model | Callback-based | Event stream-based |
| Chat client | `OpenAIChatCompletion` | `OpenAIChatClient` |

## Testing Plan

1. Run both implementations side-by-side
2. Verify both produce similar output quality
3. Ensure event streaming works correctly
4. Test with the same prompt: "Write a tagline for a budget-friendly eBike."

## Notes

- The Microsoft Agent Framework is the unified successor to Semantic Kernel and AutoGen
- The Agent Framework provides a more streamlined API for multi-agent workflows
- Both implementations use GitHub Models API as the inference endpoint

## References

- [Agent Framework Documentation](https://learn.microsoft.com/agent-framework/overview/agent-framework-overview)
- [Agent Framework Migration Guide](https://learn.microsoft.com/en-us/semantic-kernel/support/migration/agent-framework-rc-migration-guide)
- [Sequential Orchestration](https://learn.microsoft.com/en-us/agent-framework/user-guide/workflows/orchestrations/sequential)
