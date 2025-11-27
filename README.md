# Demo GitHub Copilot CLI

A demonstration repository showcasing AI agent orchestration using **Semantic Kernel** and integration with **GitHub Copilot** agents and **MCP (Model Context Protocol) servers**.

## Table of Contents

- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [MCP Server Integration](#mcp-server-integration)
- [GitHub Copilot Agents](#github-copilot-agents)
- [Configuration](#configuration)
- [License](#license)

## Overview

This repository demonstrates how to build AI-powered applications using:

1. **Semantic Kernel Agents**: Sequential orchestration of AI agents for multi-step tasks
2. **GitHub Models Integration**: Connecting to GitHub's AI model inference API
3. **MCP Server Development**: Creating custom Model Context Protocol servers
4. **GitHub Copilot Agents**: Custom agent configurations for specialized tasks

## Repository Structure

```
├── semantic_kernel_agents.py  # Main Python script with Semantic Kernel agent orchestration
├── LOTR.md                    # MCP Server requirements for Lord of the Rings API
├── .github/
│   ├── agents/                # GitHub Copilot agent configurations
│   │   ├── Agent Framework Implementer.agent.md
│   │   └── planner.agent.md
│   └── instructions/          # Coding instructions for GitHub Copilot
│       └── MCP-instructions.instructions.md
├── .gitignore                 # Git ignore patterns
└── README.md                  # This file
```

## Features

### Semantic Kernel Sequential Orchestration

The `semantic_kernel_agents.py` script demonstrates:

- **WriterAgent**: A copywriter agent that generates concise marketing copy
- **ReviewerAgent**: A reviewer agent that provides feedback on generated content
- **Sequential Orchestration**: Agents work in sequence, with the reviewer providing feedback on the writer's output

### MCP Server Integration

The repository includes requirements for building an MCP server that:

- Connects to The One API (Lord of the Rings quotes API)
- Handles Bearer token authentication
- Exposes tools for quote retrieval

### GitHub Copilot Agents

Custom agent configurations for:

- **Agent Framework Implementer**: Specialized for implementing agent-based solutions
- **Planner**: Strategic planning and architecture assistance

## Prerequisites

- Python 3.10+
- GitHub account with access to GitHub Models
- GitHub Personal Access Token (PAT) with appropriate permissions
- Azure CLI (for Azure credential management)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/EfeSenerr/demo-ghcp-cli.git
   cd demo-ghcp-cli
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install semantic-kernel azure-identity openai python-dotenv
   ```

4. **Set up environment variables**:
   
   Create a `.env` file in the root directory:
   ```env
   GITHUB_TOKEN=your_github_token_here
   ONE_API_KEY=your_one_api_key_here  # For MCP Server integration
   ```

## Usage

### Running the Semantic Kernel Agents Example

```bash
python semantic_kernel_agents.py
```

This will execute a sequential orchestration where:
1. The **WriterAgent** generates a tagline for a budget-friendly eBike
2. The **ReviewerAgent** provides feedback on the generated tagline

**Example Output**:
```
===== Semantic Kernel Sequential Answer =====
# WriterAgent
Ride more, spend less – eBike your way to freedom!

# ReviewerAgent
Great tagline! It's catchy, emphasizes value, and evokes a sense of freedom...
```

### Customizing the Prompt

Modify the `PROMPT` variable in `semantic_kernel_agents.py`:

```python
PROMPT = "Write a tagline for a budget-friendly eBike."
```

## MCP Server Integration

The `LOTR.md` file outlines requirements for building an MCP server that integrates with The One API:

### Requirements

- **API Endpoint**: `https://the-one-api.dev/v2/quote`
- **Authentication**: Bearer token (`Authorization: Bearer your-api-key-123`)
- **Environment Variable**: API key stored as `ONE_API_KEY` in `.env`

### Implementation Guidelines

See `.github/instructions/MCP-instructions.instructions.md` for detailed MCP server development guidelines, including:

- Using `uv` for project management
- FastMCP server setup
- Tool, resource, and prompt decorators
- Best practices for error handling and async operations

## GitHub Copilot Agents

This repository includes custom GitHub Copilot agent configurations:

### Agent Framework Implementer

A specialized agent for creating, updating, and refactoring code using the Python version of Microsoft Agent Framework.

### Planner

A strategic planning and architecture assistant focused on:
- Understanding codebases
- Clarifying requirements
- Developing implementation strategies

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GITHUB_TOKEN` | GitHub Personal Access Token for GitHub Models API | Yes |
| `ONE_API_KEY` | API key for The One API (Lord of the Rings) | For MCP Server |

### Model Configuration

The default model used is `openai/gpt-4.1` via GitHub Models. To change the model, modify the `chat_client` configuration in `semantic_kernel_agents.py`:

```python
chat_client = OpenAIChatCompletion(
    async_client=openai_client,
    ai_model_id="openai/gpt-4.1",  # Change model here
)
```

### Available Models via GitHub Models

- `openai/gpt-4.1`
- `openai/gpt-4o`
- `openai/gpt-4o-mini`
- And more...

## Dependencies

- **semantic-kernel**: Microsoft Semantic Kernel for AI orchestration
- **azure-identity**: Azure authentication library
- **openai**: OpenAI Python client
- **python-dotenv**: Environment variable management

## License

Copyright (c) Microsoft. All rights reserved.

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For questions or issues, please open a GitHub issue in this repository.
