from dotenv import load_dotenv
from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import noise_cancellation, google
from prompts import AGENT_INSTRUCTION, SESSION_INSTRUCTION
from tools import get_weather, search_web, send_email
from langdetect import detect
import logging

load_dotenv()

# 🧠 Language Detection → Voice Mapping
def detect_language(text: str) -> str:
    """
    Detect user's language from text and return the appropriate Google voice ID.
    """
    try:
        lang = detect(text)
        if lang.startswith("hi"):
            logging.info("🗣️ Detected Hindi - Using voice hi-IN-Standard-A")
            return "hi-IN-Standard-A"  # Hindi
        elif lang.startswith("te"):
            logging.info("🗣️ Detected Telugu - Using voice te-IN-Standard-A")
            return "te-IN-Standard-A"  # Telugu
        else:
            logging.info("🗣️ Defaulting to English - Using voice en-IN-Standard-B")
            return "en-IN-Standard-B"  # English
    except Exception as e:
        logging.warning(f"Language detection failed: {e}")
        return "en-IN-Standard-B"


# 🎯 Assistant Class
class Assistant(Agent):
    def __init__(self, sample_text="Hello") -> None:
        # Detect voice based on initial text/language
        selected_voice = detect_language(sample_text)

        super().__init__(
            instructions=AGENT_INSTRUCTION,
            llm=google.beta.realtime.RealtimeModel(
                voice=selected_voice,   # 🎙️ Voice dynamically set
                temperature=0.8,
            ),
            tools=[get_weather, search_web, send_email],
        )


# 🚀 Entrypoint for CASK
# 🚀 Entrypoint for CASK
async def entrypoint(ctx: agents.JobContext):
    """
    Entry point that starts the assistant session in a LiveKit room.
    Automatically greets the user when it starts.
    """
    session = AgentSession()

    # You can pass sample text like "నమస్తే" or "नमस्ते" for auto-detect
    assistant = Assistant(sample_text="Hello")

    await session.start(
        room=ctx.room,
        agent=assistant,
        room_input_options=RoomInputOptions(
            video_enabled=True,
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    await ctx.connect()

    # ✅ Auto introduction when agent starts
    intro_message = "Hello boss, I am CASK — your multilingual voice assistant. How can I help you today?"
    await session.send_text(intro_message)

    # Optionally follow up with session logic (if you use memory/context)
    await session.generate_reply(instructions=SESSION_INSTRUCTION)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
