# Discord Raw API MCP Server

This MCP server provides raw Discord API access through a single flexible tool. It supports both REST API calls and slash command syntax.

## Installation

1. Set up your Discord bot:
   - Create a new application at [Discord Developer Portal](https://discord.com/developers/applications)
   - Create a bot and copy the token
   - Enable required privileged intents:
     - MESSAGE CONTENT INTENT
     - PRESENCE INTENT
     - SERVER MEMBERS INTENT
   - Invite the bot to your server using OAuth2 URL Generator

2. Clone and install the package:
```bash
# Clone the repository
git clone https://github.com/hanweg/mcp-discord-raw.git
cd mcp-discord-raw

# Create and activate virtual environment
uv venv
.venv\Scripts\activate

### If using Python 3.13+ - install audioop library: `uv pip install audioop-lts`

# Install the package
uv pip install -e .
```

## Configuration

Add this to your `claude_desktop_config.json`
```json
    "discord-raw": {
      "command": "uv",
      "args": [
        "--directory", 
        "PATH/TO/mcp-discord-raw",
        "run",
        "discord-raw-mcp"
      ],
      "env": {
        "DISCORD_TOKEN": "YOUR-BOT-TOKEN"
      }
    }
```

## Usage

### REST API Style

```python
{
    "method": "POST",
    "endpoint": "guilds/123456789/roles",
    "payload": {
        "name": "Bot Master",
        "permissions": "8",
        "color": 3447003,
        "mentionable": true
    }
}
```

### Slash Command Style

```python
{
    "method": "POST",
    "endpoint": "/role create name:Bot_Master color:blue permissions:8 mentionable:true guild_id:123456789"
}
```

## Examples

1. Create a role:
```json
{
    "method": "POST",
    "endpoint": "/role create name:Moderator color:red permissions:moderate_members guild_id:123456789"
}
```

2. Send a message:
```json
{
    "method": "POST",
    "endpoint": "channels/123456789/messages",
    "payload": {
        "content": "Hello from the API!"
    }
}
```

3. Get server information:
```json
{
    "method": "GET",
    "endpoint": "guilds/123456789"
}
```

## License

MIT License