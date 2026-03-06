# Project Documentation

## Technical Stack

- **Language:** Python
- **Core Library:** semantic_kernel_agents.py (custom logic)
- **Project Management:** No explicit package manager or requirements file detected
- **MCP Server Integration:** Follows MCP instructions for Python server development (see .github/instructions/MCP-instructions.instructions.md)

## Business Logic

This project appears to implement agent-based logic using Semantic Kernel and MCP server patterns. The main business logic is likely contained in `semantic_kernel_agents.py`, which may define tools, resources, and prompts for agent operations. The system is designed to register tools and resources, handle structured outputs, and support both stdio and HTTP transports for agent communication.

## Key Files

- `semantic_kernel_agents.py`: Main agent logic and tool/resource registration
- `.github/instructions/MCP-instructions.instructions.md`: Development guidelines for MCP server integration

## Usage

- Run the server using MCP patterns (see instructions file for details)
- Tools and resources are registered via decorators and type hints
- Supports structured output for machine-readable data

## Notes

- Ensure type hints and structured outputs for compatibility
- Follow MCP instructions for best practices and error handling
