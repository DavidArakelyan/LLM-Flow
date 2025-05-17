#!/usr/bin/env python
import asyncio
import httpx
import uuid
from typing import List

BACKEND_URL = "http://localhost:8000"


async def chat_loop():
    print("Welcome to LLM Flow Chat!")
    print("Type 'exit' to quit")
    print("-" * 50)

    history: List[str] = []
    client = httpx.AsyncClient(base_url=BACKEND_URL)

    try:
        while True:
            # Get user input
            user_input = input("\nYou: ").strip()
            if user_input.lower() == "exit":
                break

            # Prepare the chat message
            message = {
                "id": str(uuid.uuid4()),
                "content": user_input,
                "history": history,
            }

            try:
                # Send message to backend
                response = await client.post("/chat", json=message)
                response.raise_for_status()
                result = response.json()

                # Print response
                if "answer" in result:
                    print("\nAssistant:", result["answer"])
                elif "response" in result:
                    print("\nAssistant:", result["response"])
                else:
                    print("\nAssistant:", "No response received")

                # Update history
                history.append(user_input)

            except httpx.HTTPError as e:
                print(f"\nError communicating with backend: {str(e)}")
            except Exception as e:
                print(f"\nUnexpected error: {str(e)}")

    finally:
        await client.aclose()


if __name__ == "__main__":
    asyncio.run(chat_loop())
