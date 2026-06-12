import asyncio
import io
import os
from tkinter import Tk, filedialog # Added for file selector interface
import edge_tts
import pandas as pd
import pygame

# ==========================================
# PART 1: Voice Management
# ==========================================

# This function fetches available voices and filters them based on locale and gender. 
# It uses pandas for easier data manipulation and presentation. 
async def get_filtered_voices(locale_prefix="en", gender="Female"):
    """Fetches and filters available voices using a pandas DataFrame."""
    voices_manager = await edge_tts.VoicesManager.create()
    voices = voices_manager.voices
    
    # edge_tts provides 'ShortName' directly in its voice dictionary
    voices_list = [
        [voice['ShortName'], voice['Locale'], voice['Gender']] 
        for voice in voices
    ]
    
    # Create a DataFrame for easier filtering
    headers = ["ShortName", "Locale", "Gender"]
    df_voices = pd.DataFrame(voices_list, columns=headers)
    
    # Filter by language and gender
    filtered_df = df_voices[
        (df_voices['Locale'].str.startswith(locale_prefix)) & 
        (df_voices['Gender'] == gender)
    ]

    # Reset index for cleaner output
    filtered_df.reset_index(drop=True, inplace=True)
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

# This function opens a native Windows file explorer dialog to allow the user to select a text file.
def prompt_for_text_file():
    """Opens a native Windows file explorer to select a text file."""
    # Initialize tkinter and immediately hide the blank background window
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True) # Brings the file explorer window to the front
    
    print("Opening file selector... Please choose a text file.")
    
    # Open the dialog window restricted to Text Files
    file_path = filedialog.askopenfilename(
        title="Select a Text File to Read Aloud",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    
    # Close the hidden window track cleanly
    root.destroy()
    return file_path

# This function reads the content of the selected text file, generates TTS audio, 
# and plays it through the speakers using pygame.
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

# The main function orchestrates the workflow: it can optionally display available voices,
# prompts the user to select a text file, and then reads it aloud using the specified 
# voice and speed settings.
async def main():
    # Optional: View available voices if you want to swap the voice name below
    # available_voices = await get_filtered_voices(locale_prefix="en", gender="Female")
    # print(available_voices)

    # 1. Ask the user to select a file using the new prompt function
    selected_file = prompt_for_text_file()
    
    # Handle user canceling the file browser screen
    if not selected_file:
        print("No file selected. Exiting script.")
        return
        
    # 2. Configuration Settings
    voice_choice = "en-US-JennyNeural"
    speed_rate = "-5%"
    
    # 3. Run the audio engine using the selected path
    await read_text_file_aloud(selected_file, rate=speed_rate, voice=voice_choice)

# Run the main application workflow
if __name__ == "__main__":
    # If running inside a Jupyter notebook or interactive panel, use:
    # await main()
    # If running as a standard standalone script, use:
    asyncio.run(main())