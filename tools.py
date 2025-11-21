import logging
from livekit.agents import function_tool, RunContext
import requests
from langchain_community.tools import DuckDuckGoSearchRun
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional
from langdetect import detect
from deep_translator import GoogleTranslator  # ✅ Replaced googletrans

# ✅ Detect the user's language (Hindi, Telugu, or English)
def detect_language(text: str) -> str:
    """Detect language code (hi, te, en)."""
    try:
        lang = detect(text)
        if lang.startswith("hi"):
            return "hi"
        elif lang.startswith("te"):
            return "te"
        else:
            return "en"
    except Exception as e:
        logging.warning(f"Language detection failed: {e}")
        return "en"


# ✅ Translate responses using Deep Translator
def translate_response(response: str, target_lang: str) -> str:
    """Translate responses to Hindi or Telugu if needed."""
    if target_lang in ["hi", "te"]:
        try:
            translated_text = GoogleTranslator(source="auto", target=target_lang).translate(response)
            return translated_text
        except Exception as e:
            logging.warning(f"Translation failed: {e}")
            return response
    return response


# 🌤️ Weather Tool
@function_tool()
async def get_weather(context: RunContext, city: str) -> str:
    """
    Get the current weather for a given city.
    Responds in English, Hindi, or Telugu depending on user input.
    """
    user_lang = detect_language(city)
    try:
        response = requests.get(f"https://wttr.in/{city}?format=3")
        if response.status_code == 200:
            weather_info = response.text.strip()
            logging.info(f"Weather for {city}: {weather_info}")
            result = f"The current weather in {city} is {weather_info}."
            return translate_response(result, user_lang)
        else:
            msg = f"Could not retrieve weather for {city}."
            return translate_response(msg, user_lang)
    except Exception as e:
        msg = f"An error occurred while retrieving weather for {city}."
        logging.error(f"{msg} Error: {e}")
        return translate_response(msg, user_lang)


# 🌐 Web Search Tool
@function_tool()
async def search_web(context: RunContext, query: str) -> str:
    """
    Search the web using DuckDuckGo.
    Automatically returns result in user's language.
    """
    user_lang = detect_language(query)
    try:
        results = DuckDuckGoSearchRun().run(tool_input=query)
        logging.info(f"Search results for '{query}': {results}")
        return translate_response(results, user_lang)
    except Exception as e:
        logging.error(f"Error searching the web for '{query}': {e}")
        msg = "An error occurred while searching the web."
        return translate_response(msg, user_lang)


# 📧 Email Tool
@function_tool()
async def send_email(
    context: RunContext,  # type: ignore
    to_email: str,
    subject: str,
    message: str,
    cc_email: Optional[str] = None
) -> str:
    """
    Send an email through Gmail.
    Automatically acknowledges success/failure in user’s language.
    """
    user_lang = detect_language(message)
    try:
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        gmail_user = os.getenv("GMAIL_USER")
        gmail_password = os.getenv("GMAIL_APP_PASSWORD")

        if not gmail_user or not gmail_password:
            msg = "Email sending failed: Gmail credentials not configured."
            logging.error(msg)
            return translate_response(msg, user_lang)

        # Create message
        msg_obj = MIMEMultipart()
        msg_obj["From"] = gmail_user
        msg_obj["To"] = to_email
        msg_obj["Subject"] = subject

        recipients = [to_email]
        if cc_email:
            msg_obj["Cc"] = cc_email
            recipients.append(cc_email)

        msg_obj.attach(MIMEText(message, "plain"))

        # Connect and send
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, recipients, msg_obj.as_string())
        server.quit()

        success_msg = f"Email sent successfully to {to_email}."
        logging.info(success_msg)
        return translate_response(success_msg, user_lang)

    except smtplib.SMTPAuthenticationError:
        msg = "Email sending failed: Authentication error. Please check Gmail credentials."
        logging.error(msg)
        return translate_response(msg, user_lang)
    except smtplib.SMTPException as e:
        msg = f"SMTP error occurred: {e}"
        logging.error(msg)
        return translate_response(msg, user_lang)
    except Exception as e:
        msg = f"An error occurred while sending the email: {e}"
        logging.error(msg)
        return translate_response(msg, user_lang)
