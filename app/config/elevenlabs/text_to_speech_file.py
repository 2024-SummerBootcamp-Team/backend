import json
import os
import uuid

from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs

client = ElevenLabs()


def text_to_speech_file(text: str) -> str:
    # Calling the text_to_speech conversion API with detailed parameters
    response = client.text_to_speech.convert(
        # voice_id="pNInz6obpgDQGcFmaJgB",  # Adam pre-made voice
        voice_id="Es5AnE58gKPS9Vffyooe",
        optimize_streaming_latency="0",
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_multilingual_v2",  # use the turbo model for low latency, for other languages use the `eleven_multilingual_v2`
        voice_settings=VoiceSettings(
            stability=0.5,
            similarity_boost=0.75,
            style=0.0,
            use_speaker_boost=True,
        ),
    )

    # Generating a unique file name for the output MP3 file
    save_file_path = f"{uuid.uuid4()}.mp3"
    # Writing the audio stream to the file

    with open(save_file_path, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)

    print(f"A new audio file was saved successfully at {save_file_path}")

    # Return the path of the saved audio file
    return save_file_path


if __name__ == "__main__":
    text_to_speech_file("Hello, world! This is a test of the ElevenLabs API.")