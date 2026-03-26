
import asyncio
import json

from groq import AsyncGroq
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client


client = AsyncGroq(api_key="api_key")


async def main() -> None:
    server = StdioServerParameters(command="py", args=["server.py"])

    async with stdio_client(server) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            mcp_tools = await session.list_tools()
            tools = [
                {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.inputSchema,
                    },
                }
                for tool in mcp_tools.tools
            ]

            messages = [
                {
                    "role": "system",
                    "content": "For time/date/month/year questions, call the provided tool and answer from tool output.",
                },
                {
                    "role": "user",
                    "content": "what is the date now",
                }
            ]

            response = await client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                max_tokens=1000,
                messages=messages,
                tools=tools,
                tool_choice="auto",
            )

            msg = response.choices[0].message
            messages.append({"role": "assistant", "content": msg.content or "", "tool_calls": msg.tool_calls})

            if msg.tool_calls:
                for tool_call in msg.tool_calls:
                    tool_name = tool_call.function.name
                    arguments = json.loads(tool_call.function.arguments or "{}")

                    tool_result = await session.call_tool(tool_name, arguments)
                    tool_text = "\n".join(
                        item.text for item in getattr(tool_result, "content", []) if hasattr(item, "text")
                    )

                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": tool_name,
                            "content": tool_text or "Tool executed successfully.",
                        }
                    )

                final_response = await client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    max_tokens=1000,
                    messages=messages,
                )
                print(final_response.choices[0].message.content)
            else:
                print(msg.content)


if __name__ == "__main__":
    asyncio.run(main())
