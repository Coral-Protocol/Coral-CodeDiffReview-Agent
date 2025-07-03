import asyncio
import os

from camel.agents import ChatAgent
from camel.models import ModelFactory
from camel.toolkits import MCPToolkit
from camel.utils.mcp_client import ServerConfig
from camel.toolkits.mcp_toolkit import MCPClient
import urllib.parse
from dotenv import load_dotenv
import json

load_dotenv(override=True)

base_url = os.getenv("CORAL_SSE_URL")
agentID = os.getenv("CORAL_AGENT_ID")

params = {
    # "waitForAgents": 1,
    "agentId": agentID,
    "agentDescription": """An agent responsible for retrieving and formatting code diffs/changed files from a GitHub pull request. 
                           You should let me know the `repo_name` and `pr_number`"""
}
query_string = urllib.parse.urlencode(params)
MCP_SERVER_URL = f"{base_url}?{query_string}"

def get_user_message():
    return "[automated] continue collaborating with other agents. make sure to mention agents you intend to communicate with"

async def get_tools_description(tools):
    descriptions = []
    for tool in tools:
        tool_name = getattr(tool.func, '__name__', 'unknown_tool')
        schema = tool.get_openai_function_schema() or {}
        arg_names = list(schema.get('parameters', {}).get('properties', {}).keys()) if schema else []
        description = tool.get_function_description() or 'No description'
        schema_str = json.dumps(schema, default=str).replace('{', '{{').replace('}', '}}')
        descriptions.append(
            f"Tool: {tool_name}, Args: {arg_names}, Description: {description}, Schema: {schema_str}"
        )
    return "\n".join(descriptions)


async def create_math_agent(tools):
    tools_description = await get_tools_description(tools)
    print(tools_description)
    sys_msg = (
        f"""
        You are `codediff_review_agent`, responsible for retrieving and formatting code diffs from a GitHub pull request.

        1. Use `wait_for_mentions(timeoutMs=60000)` to wait for instructions from other agents.
        2. When a mention is received, record the `threadId` and `senderId`.
        3. Check if the message asks to analyze a PR with a repo name and PR number.
        4. Extract `repo_name` and `pr_number` from the message.
        5. Call `get_pull_request_files(pullNumber=pr_number, repo=repo_name)` to get code diffs.
        6. If this call fails, send the error message using `send_message` to the sender.
        7. If successful, send the formatted code diffs using `send_message` to the sender.
        8. If the message format is invalid or parsing fails, skip it silently.
        9. Do not create threads; always use the `threadId` from the mention.
        10. Wait 2 seconds and repeat from step 1. 

        These are the list of all tools: {tools_description}
        """
    )
    model = ModelFactory.create(
        model_platform=os.getenv("MODEL_PROVIDER"),
        model_type=os.getenv("MODEL_NAME"),
        api_key=os.getenv("API_KEY"),
        model_config_dict={"temperature": float(os.getenv("MODEL_TEMPERATURE"))},
    )

    camel_agent = ChatAgent(
        system_message=sys_msg,
        model=model,
        tools=tools,
        token_limit=int(os.getenv("MODEL_TOKEN"))
    )

    return camel_agent


async def main():
    # Simply add the Coral server address as a tool
    print("Starting MCP client...")
    server = MCPClient(ServerConfig(url=MCP_SERVER_URL , timeout=3000000.0, sse_read_timeout=3000000.0, terminate_on_close=True, prefer_sse=True), timeout=3000000.0)
    
    # Initialize github_client
    github_token = os.getenv("GITHUB_ACCESS_TOKEN")
    github_client = MCPClient(
        ServerConfig(command="npx",
        args=['-y', '@modelcontextprotocol/server-github'],
        env={"GITHUB_PERSONAL_ACCESS_TOKEN": github_token},
        timeout=300.0),timeout=3000000.0
    )


    mcp_toolkit = MCPToolkit([server, github_client])

    connected = await mcp_toolkit.connect()
    tools = connected.get_tools()

    selected_tool_name = [
        "list_agents",
        "create_thread",
        "add_participant",
        "remove_participant",
        "close_thread",
        "send_message",
        "wait_for_mentions",
        "get_pull_request_files"
        ]

    tools = [tool for tool in tools if getattr(tool.func, '__name__', 'unknown_tool') in selected_tool_name]

    camel_agent = await create_math_agent(tools)

    while True:
        resp = await camel_agent.astep(get_user_message())
        print(resp)
        msg0 = resp.msgs[0]
        print(msg0.to_dict())
        await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())
