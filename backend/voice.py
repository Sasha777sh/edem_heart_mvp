import os
import uuid

# Graceful degradation for edge_tts
try:
    import edge_tts
    HAS_TTS = True
except ImportError:
    HAS_TTS = False
    print("⚠️ WARNING: edge_tts not found. Voice generation disabled.")

async def generate_voice(text: str, folder="assets") -> str:
    """
    Generates a voice file from text using Edge TTS.
    Returns absolute path to the .mp3 file.
    If TTS is missing, returns None.
    """
    if not HAS_TTS:
        return None

    if not os.path.exists(folder):
        os.makedirs(folder)
        
    filename = f"{uuid.uuid4()}.mp3"
    output_path = os.path.join(folder, filename)
    
    # Voices:
    # ru-RU-DmitryNeural (Male, Deep)
    # ru-RU-SvetlanaNeural (Female, Soft)
    VOICE = "ru-RU-DmitryNeural"
    
    try:
        communicate = edge_tts.Communicate(text, VOICE)
        await communicate.save(output_path)
    except Exception as e:
        print(f"TTS Error: {e}")
        return None
    
    return output_path
