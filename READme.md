# Armenian Bank AI Voice Assistant

AI Voice Assistant: Get answers to your questions about credits, deposits, and branches for Ameriabank, Araratbank, and Idram.
My system uses Crawl4AI to automatically scrape real-time banking data from websites and store it in a structured info.json file. This data is then processed within the LiveKit ecosystem using Whisper and GPT-4o to provide accurate, AI-driven voice responses to customer inquiries about loans and deposits.

## Needed
- Python 3.11 installed
- Docker Desktop installed and running (https://www.docker.com/products/docker-desktop/)
- An OpenAI API key
## Tech Stack
- **Backend:** Python
- **AI Models:** OpenAI GPT-4o, Whisper (STT)
- **Web Scraping:** Crawl4AI
- **Speech:** pyttsx3 (TTS)
- **Importatr libaries** crawl4ai, sounddevice, openai, pyttsx3, numpy, scipy

## Files
- `ameriabank.py`,`IDRAM.py`,`Araratbank.py`: It collects information about credits,deposits and about following banks
- `main.py`: Responsible for AI assistent logic (LLM)
- `voice_bot.py`:Responsible for AI assistent speach
- `info.json`: Data base

## Installation 
clone the repo 
`git clone https://github.com/yourusername/project-name.git
cd project-name`
enter your ARI key 
download necessary liberies `pip install crawl4ai sounddevice openai pyttsx3 numpy scipy`
download  Playwright`python -m playwright install chromium`

## Usage

1. first run scrips to restart `info.json`
   `python Ameria_Crawler.py`
   `python IDRAM.py`
   `python Araratbank.py`
2. run LiveKit server 
    `docker run --rm -it -p 7880:7880 -p 7881:7881 -e "LIVEKIT_KEYS=devkey: secret" livekit/livekit-server --dev`
    if the port is used for other applicaton , change it using 
    `docker run --rm -it -p 7882:7880 -p 7883:7881 -e "LIVEKIT_KEYS=devkey: secret" livekit/livekit-server --dev`
3. check 'http://localhost:7880' on browser if it works 
4. run voice assistant .
   `python voice_bot.py`

## System Architecture
The assistant follows a **Retrieval-Augmented Generation (RAG)** pattern:
1. **Data Acquisition:** `Crawl4AI` performs asynchronous scraping of banking portals.
2. **Knowledge Base:** Extracted Markdown is filtered for keywords (Loans, Deposits, Branches) and stored in `info.json`.
3. **Voice Processing:** 
   - **STT:** `OpenAI Whisper` converts Armenian speech to text.
   - **Reasoning:** `GPT-4o` analyzes the query using the `info.json` context.
   - **TTS:** `pyttsx3` generates the voice response.
4. **Transport:** `LiveKit` manages the real-time audio stream.

## Grounding & Accuracy
To ensure financial accuracy:
- **Strict Context:** The system prompt restricts the AI to *only* use data found in `info.json`.
- **Fallback:** If information is missing or the question is out-of-scope, the bot is programmed to respond with: *"Ես չեմ կարող պատասխանել այդ հարցին"* (I cannot answer that question).

## Troubleshooting
- **Port Conflicts:** If port `7880` is busy, Docker might fail. Use the alternative port mapping provided in the usage section.
- **Audio Devices:** Ensure your microphone is set as the default input device in your OS settings before running `voice_bot.py`.
- **API Limits:** Ensure your OpenAI billing account has a positive balance for GPT-4o and Whisper API calls.
