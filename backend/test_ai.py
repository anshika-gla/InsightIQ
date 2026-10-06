import asyncio
import httpx

from ai.client import AIClient


async def main():
    client = AIClient()

    try:
        plan = await client.generate_query_plan(
            "What are the top 2 cities by profit?"
        )

        print(plan.model_dump_json(indent=2))

    except httpx.HTTPStatusError as e:
        print("STATUS:", e.response.status_code)
        print("RESPONSE:", e.response.text)


if __name__ == "__main__":
    asyncio.run(main())