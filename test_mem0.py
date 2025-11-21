from dotenv import load_dotenv
from mem0 import MemoryClient
import logging
import json
import os

# Load your environment variables
load_dotenv()

api_key = os.getenv("MEM0_API_KEY")
if not api_key:
    raise ValueError("❌ MEM0_API_KEY not found in .env file!")

# Initialize Mem0 client
mem0 = MemoryClient(api_key=api_key)
user_name = "Tarun"

def add_memory():
    messages_formatted = [
        {"role": "user", "content": "I really like Linkin Park."},
        {"role": "assistant", "content": "That is a good choice."},
        {"role": "user", "content": "I think so too."},
        {"role": "assistant", "content": "What is your favorite song by them?"},
    ]

    # ✅ Use user_id and agent_id directly for ADD
    response = mem0.add(
        messages_formatted,
        user_id=user_name,
        agent_id="voice_assistant"
    )

    print("✅ Memory Added Successfully:")
    print(json.dumps(response, indent=2))


def get_memory_by_query():
    query = f"What are {user_name}'s preferences?"

    # ✅ Use filters for SEARCH (required by v1.0.0)
    results = mem0.search(
        query,
        filters={"user_id": user_name, "agent_id": "voice_assistant"}
    )

    print("\n🧠 Retrieved Memories:")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    add_memory()
    get_memory_by_query()
