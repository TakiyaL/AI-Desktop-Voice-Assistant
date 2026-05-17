import asyncio
import os
import edge_tts
import pygame
import time

VOICE = "en-US-AndrewNeural" 

# Initialize pygame once
pygame.mixer.init()

# ---------------- REMOVE FILE ----------------
def remove_file(file_path):

    for _ in range(5):

        try:
            if os.path.exists(file_path):

                os.remove(file_path)

            break

        except PermissionError:

            time.sleep(0.2)

# ---------------- PLAY AUDIO ----------------
def play_audio(file_path):

    try:

        pygame.mixer.music.load(file_path)

        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():

            pygame.time.Clock().tick(10)

    except Exception as e:

        print(f"Audio Error: {e}")

# ---------------- TEXT TO SPEECH ----------------
async def amain(text, output_file):

    try:

        communicate = edge_tts.Communicate(text, VOICE)

        await communicate.save(output_file)

        play_audio(output_file)

    except Exception as e:

        print(f"TTS Error: {e}")

    finally:

        pygame.mixer.music.unload()

        remove_file(output_file)

# ---------------- MAIN SPEAK FUNCTION ----------------
def speak(text, output_file="speak.mp3"):

    print(f"\n==> Jarvis AI: {text}\n")

    try:

        asyncio.run(amain(text, output_file))

    except RuntimeError:
        # Fix for Jupyter/Streamlit running loop

        loop = asyncio.get_event_loop()

        loop.run_until_complete(
            amain(text, output_file)
        )
speak("Initializing Jarvis AI...")
