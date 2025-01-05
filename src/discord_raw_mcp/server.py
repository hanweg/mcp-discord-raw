import os
import asyncio
import logging
import json
from typing import Any, List

import aiohttp
import discord
from discord.ext import commands
from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("discord-raw-mcp-server")

# Discord bot setup
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN environment variable is required")

# Initialize Discord bot with necessary intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Initialize MCP server
app = Server("discord-raw-server")

# Store Discord client reference and API version
discord_client = None
DISCORD_API_VERSION = "10"
DISCORD_API_BASE = f"https://discord.com/api/v{DISCORD_API_VERSION}"

@bot.event
async def on_ready():
    global discord_client
    discord_client = bot
    logger.info(f"Logged in as {bot.user.name}")

async def execute_discord_api(method: str, endpoint: str, payload: dict = None) -> dict:
    """Execute a raw Discord API request."""
    if not discord_client:
        raise RuntimeError("Discord client not ready")
    
    async with aiohttp.ClientSession() as session:
        headers = {
            "Authorization": f"Bot {DISCORD_TOKEN}",
            "Content-Type": "application/json",
        }
        
        url = f"{DISCORD_API_BASE}/{endpoint.lstrip('/')}"
        
        async with session.request(
            method=method.upper(),
            url=url,
            headers=headers,
            json=payload if payload else None
        ) as response:
            if response.status == 204:  # No content
                return {"success": True}
                
            response_data = await response.json()
            
            if not response.ok:
                error_msg = f"Discord API error: {response.status} - {response_data.get('message', 'Unknown error')}"
                logger.error(error_msg)
                return {
                    "success": False,
                    "error": error_msg,
                    "status": response.status,
                    "details": response_data
                }
                
            return response_data

@app.list_tools()
async def list_tools() -> List[Tool]:
    """List available Discord tools."""
    return [
        Tool(
            name="discord_api",
            description="Execute raw Discord API commands. Supports both REST API calls and application commands.",
            inputSchema={
                "type": "object",
                "properties": {
                    "method": {
                        "type": "string",
                        "description": "HTTP method (GET, POST, PUT, PATCH, DELETE)",
                        "enum": ["GET", "POST", "PUT", "PATCH", "DELETE"]
                    },
                    "endpoint": {
                        "type": "string",
                        "description": "Discord API endpoint (e.g., 'guilds/{guild.id}/roles' or command like '/role create')"
                    },
                    "payload": {
                        "type": "object",
                        "description": "Optional request payload/body"
                    }
                },
                "required": ["method", "endpoint"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Any) -> List[TextContent]:
    """Handle Discord API tool calls."""
    
    if name != "discord_api":
        raise ValueError(f"Unknown tool: {name}")
        
    if not isinstance(arguments, dict):
        raise ValueError("Invalid arguments format")

    method = arguments.get("method", "").upper()
    endpoint = arguments.get("endpoint", "")
    payload = arguments.get("payload")

    # Handle slash command syntax
    if endpoint.startswith('/'):
        # Convert slash command to API call
        command_parts = endpoint[1:].split()  # Remove leading / and split
        
        if len(command_parts) < 2:
            return [TextContent(
                type="text",
                text=f"Invalid slash command format. Must include command and subcommand."
            )]
            
        command, subcommand, *args = command_parts
        
        # Example: Convert /role create to appropriate API call
        if command == "role":
            if subcommand == "create":
                # Parse arguments from the command string
                arg_dict = {}
                for arg in args:
                    if ":" in arg:
                        key, value = arg.split(":", 1)
                        arg_dict[key] = value
                
                # Modify method and endpoint for role creation
                method = "POST"
                guild_id = arg_dict.get("guild_id", payload.get("guild_id") if payload else None)
                if not guild_id:
                    return [TextContent(
                        type="text",
                        text="guild_id is required for role creation"
                    )]
                
                endpoint = f"guilds/{guild_id}/roles"
                payload = {
                    "name": arg_dict.get("name", "New Role"),
                    "permissions": arg_dict.get("permissions", "0"),
                    "color": int(arg_dict.get("color", "0"), 16) if "color" in arg_dict else 0,
                    "hoist": arg_dict.get("hoist", "false").lower() == "true",
                    "mentionable": arg_dict.get("mentionable", "false").lower() == "true"
                }

    try:
        result = await execute_discord_api(method, endpoint, payload)
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
    except Exception as e:
        logger.error(f"Error executing Discord API call: {str(e)}")
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]

async def main():
    # Start Discord bot in the background
    asyncio.create_task(bot.start(DISCORD_TOKEN))
    
    # Run MCP server
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())