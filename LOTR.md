**MCP Server Requirements:**
- Implement a custom MCP server that connects to The One API
- Handle Bearer token authentication: `Authorization: Bearer your-api-key-123`
- API key stored in .env locally, as ONE_API_KEY
- Expose tools for quote retrieval (https://the-one-api.dev/v2/quote)
- Agent should be able to access a custom MCP server to retrieve Lord of the Rings quotes from an API (https://the-one-api.dev/v2/quote)