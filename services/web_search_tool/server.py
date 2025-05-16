import os, httpx, asyncio
from fastmcp import FastMCP

SERPER_API_KEY = os.environ.get("SERPER_API_KEY")

app = FastMCP(name="web_search_tool")


@app.tool(name="web_search", description="Search the web for information")
async def search(query: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://google.serper.dev/search",
            headers={"X-API-KEY": SERPER_API_KEY},
            json={"q": query},
        )
        return response.json()


if __name__ == "__main__":
    asyncio.run(app.run_http_async(host="0.0.0.0", port=7003))
