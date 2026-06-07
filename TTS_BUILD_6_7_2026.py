import asyncio
import io
import edge_tts
import pandas as pd
import pygame

# ==========================================
# PART 1: Voice Management
# ==========================================
async def get_filtered_voices(locale_prefix="en", gender="Female"):
    """Fetches and filters available voices using a pandas DataFrame."""
    voices_manager = await edge_tts.VoicesManager.create()
    voices = voices_manager.voices
    
    # edge_tts provides 'ShortName' directly in its voice dictionary
    voices_list = [
        [voice['ShortName'], voice['Locale'], voice['Gender']] 
        for voice in voices
    ]
    
    headers = ["ShortName", "Locale", "Gender"]
    df_voices = pd.DataFrame(voices_list, columns=headers)
    
    # Filter by language and gender
    filtered_df = df_voices[
        (df_voices['Locale'].str.startswith(locale_prefix)) & 
        (df_voices['Gender'] == gender)
    ]
    return filtered_df

# ==========================================
# PART 2: TTS and Audio Playback
# ==========================================
async def text_to_speech(text, rate="0%", voice="en-US-AnaNeural"):
    """Streams TTS audio into an in-memory buffer."""
    communicate = edge_tts.Communicate(text=text, rate=rate, voice=voice)
    audio_buffer = io.BytesIO()

    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_buffer.write(chunk["data"])

    audio_buffer.seek(0)
    return audio_buffer

async def read_text_file_aloud(file_path, rate="-7%", voice="en-US-JennyNeural"):
    """Reads content from a text file and streams it to the speakers."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text_content = file.read().strip()
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    if not text_content:
        print("The file is empty.")
        return

    print(f"Generating audio using voice: {voice} at speed rate: {rate}")
    audio_buffer = await text_to_speech(text_content, rate, voice)

    # Initialize pygame mixer
    pygame.mixer.init()

    try:
        # Load audio data from the buffer and play it
        pygame.mixer.music.load(io.BytesIO(audio_buffer.getvalue()))
        pygame.mixer.music.play()

        # Keep the loop alive while audio plays
        while pygame.mixer.music.get_busy():
            await asyncio.sleep(0.5)
    except Exception as e:
        print(f"Error playing audio: {e}")
    finally:
        pygame.mixer.quit()

# ==========================================
# PART 3: Execution Control
# ==========================================
async def main():
    # Optional: View available voices if you want to swap the voice name below
    # available_voices = await get_filtered_voices(locale_prefix="en", gender="Female")
    # print(available_voices)

    # Path to your text file
    file_to_read = r"C:\Users\khang\Desktop\Projects\DS_Work\tts\Short stories\A small bird.txt"
    
    # Configuration
    voice_choice = "en-US-JennyNeural"
    speed_rate = "-5%"
    
    print(f"Starting playback for: {file_to_read}")
    await read_text_file_aloud(file_to_read, rate=speed_rate, voice=voice_choice)

# Run the main application workflow
if __name__ == "__main__":
    # If running inside a Jupyter notebook or interactive panel, use:
    # await main()
    # If running as a standard standalone script, use:
    asyncio.run(main())