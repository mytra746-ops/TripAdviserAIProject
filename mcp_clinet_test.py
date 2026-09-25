from asyncio import subprocess
from psycopg import connection_async
from langchain_core import tools
from tools.tavily_tools import client
import os
import asyncio
import certifi
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient

os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()
load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

client=MultiServerMCPClient(
    {
        "tavily": {
            "transport": "streamable-http",
            "url": f"https://mcp.tavily.com/mcp/?tavilyApiKey={TAVILY_API_KEY}"
            }
    }
)


async def get_all_tools():
    tools=await client.get_tools()
    print("\nAvailable tools from Tavily MCP:\n",len(tools))
    for tool in tools:
        print(tool.name)

# this return travily search tool object 
travily_search_tool=None

async def get_travely_search_tool():
    global travily_search_tool
    if travily_search_tool is not None:
        return

    tools = await client.get_tools()
    print("\nAvailable MCP Tools:")

    for tool in tools:
        print(tool.name)
    
    travily_search_tool=next(
        tool
        for tool in tools
        if tool.name=="tavily_search"
    )

#this function can be used to call the travily search tool
async def travily_mcp_search(query:str):
    await get_travely_search_tool()
    result = await travily_search_tool.ainvoke(
        {
        "query":query
        }
    )

    return result
    #print(result)
 
        