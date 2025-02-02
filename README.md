# Discord Raw API MCP Server

[![smithery badge](https://smithery.ai/badge/@hanweg/mcp-discord-raw)](https://smithery.ai/server/@hanweg/mcp-discord-raw)
This MCP server provides raw Discord API access through a single flexible tool. It supports both REST API calls and slash command syntax.

<a href="https://glama.ai/mcp/servers/ct3fi5s557"><img width="380" height="200" src="https://glama.ai/mcp/servers/ct3fi5s557/badge" alt="Discord Raw API Server MCP server" /></a>

## Installation

### Installing via Smithery

To install Discord Raw API for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@hanweg/mcp-discord-raw):

```bash
npx -y @smithery/cli install @hanweg/mcp-discord-raw --client claude
```

### Manual Installation
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

# Recommendations:
Put server, channel and user IDs and some examples in project knowledge to avoid having to remind the model of those, along with something like this to get it started:

"Here's how to effectively use the Discord raw API tool:
The tool is called discord_api and takes three parameters:
1. method: HTTP method ("GET", "POST", "PUT", "PATCH", "DELETE")
2. endpoint: Discord API endpoint (e.g., "guilds/{guild.id}/roles")
3. payload: Optional JSON object for the request body
Key examples I've used:
1. Creating roles:
```
discord_api
method: POST
endpoint: guilds/{server_id}/roles
payload: {
    "name": "Role Name",
    "color": 3447003,  // Blue color in decimal
    "mentionable": true
}
```
2. Creating categories and channels:
```
// Category
discord_api
method: POST
endpoint: guilds/{server_id}/channels
payload: {
    "name": "Category Name",
    "type": 4  // 4 = category
}
// Text channel in category
discord_api
method: POST
endpoint: guilds/{server_id}/channels
payload: {
    "name": "channel-name",
    "type": 0,  // 0 = text channel
    "parent_id": "category_id",
    "topic": "Channel description"
}
```
3. Moving channels to categories:
```
discord_api
method: PATCH
endpoint: channels/{channel_id}
payload: {
    "parent_id": "category_id"
}
```
4. Sending messages:
```
discord_api
method: POST
endpoint: channels/{channel_id}/messages
payload: {
    "content": "Message text with emojis \ud83d\ude04"
}
```
5. Assigning roles:
```
discord_api
method: PUT
endpoint: guilds/{server_id}/members/{user_id}/roles/{role_id}
payload: {}
```
The tool supports the full Discord API, so you can reference the Discord API documentation for more endpoints and features. The responses include IDs and other metadata you can use for subsequent requests.
Pro tips:
- Save IDs returned from creation requests to use in follow-up requests
- ~~Unicode emojis can be included directly in message content~~ ? Tell the model to use discord emoji like :champagne_glass: - Messages with unicode emoji hangs Claude Desktop?
- Channel types: 0 = text, 2 = voice, 4 = category, 13 = stage
- Role colors are in decimal format (not hex)
- Most modification endpoints use PATCH method
- Empty payloads should be {} not null"

## License

MIT License
