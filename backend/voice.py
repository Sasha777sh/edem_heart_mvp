import edge_tts
import os
import uuid

async def generate_voice(text: str, folder="assets") -> str:
    """
    Generates a voice file from text using Edge TTS.
    Returns absolute path to the .mp3 file.
    """
    if not os.path.exists(folder):
        os.makedirs(folder)
        
    filename = f"{uuid.uuid4()}.mp3"
    output_path = os.path.join(folder, filename)
    
    # Voices:
    # ru-RU-DmitryNeural (Male, Deep)
    # ru-RU-SvetlanaNeural (Female, Soft)
    VOICE = "ru-RU-DmitryNeural"
    
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(output_path)
    
    return output_path
