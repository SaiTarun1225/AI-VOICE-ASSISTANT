🎤 AI Voice Assistant

A smart, lightweight voice assistant built using Python, capable of understanding speech, recognizing user intent, and responding using text-to-speech. The assistant supports multiple languages (e.g., English, Hindi, Telugu) and performs tasks such as answering questions, opening apps, searching the web, and more.

🚀 Features

🎙 Speech Recognition

🧠 Intent Recognition (NLU / NLP)

🔊 Text-to-Speech Responses

🌍 Multilingual Support (English, Hindi, Telugu, etc.)

🔎 Web Search & General Knowledge Queries

📁 System Tasks (Open apps, read files, etc.)

❓ Fallback Responses when unknown command

🔌 Modular & Extensible Codebase

🛠️ Tech Stack
Component	Technology
Programming Language	Python 3.x
Speech-to-Text	SpeechRecognition, Google API
NLP / Intent Classification	spaCy / NLTK / Transformer model (depending on version)
Text-to-Speech	pyttsx3 / gTTS
Optional Enhancements	transformers, deep learning models

*/-----------------------------------------------------------------*/
📂 Project Structure
📁 AI-Voice-Assistant
 ┣ 📁 models
 ┃ ┗ intent_model.pkl
 ┣ 📁 data
 ┃ ┗ intents.json
 ┣ main.py
 ┣ speak.py
 ┣ listen.py
 ┣ intent_classifier.py
 ┣ requirements.txt
 ┗ README.md
