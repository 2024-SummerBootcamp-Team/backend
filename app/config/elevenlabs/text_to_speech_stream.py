import os
from io import BytesIO
from typing import IO, Generator

from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs

client = ElevenLabs()


def text_to_speech_stream(text: str) -> IO[bytes]:
# async def text_to_speech_stream(text: str) -> Generator[bytes, None, None]:
    """
    Converts text to speech and returns the audio data as a byte stream.

    This function invokes a text-to-speech conversion API with specified parameters, including
    voice ID and various voice settings, to generate speech from the provided text. Instead of
    saving the output to a file, it streams the audio data into a BytesIO object.

    Args:
        text (str): The text content to be converted into speech.

    Returns:
        IO[bytes]: A BytesIO stream containing the audio data.
    """
    # Perform the text-to-speech conversion
    response = client.text_to_speech.convert(
        # voice_id="pNInz6obpgDQGcFmaJgB",  # Adam pre-made voice
        voice_id="Es5AnE58gKPS9Vffyooe",
        optimize_streaming_latency="0",
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_multilingual_v2",
        # use the turbo model for low latency, for other languages use the `eleven_multilingual_v2`
        voice_settings=VoiceSettings(
            stability=0.5,
            similarity_boost=0.75,
            style=0.0,
            use_speaker_boost=True,
        ),
    )

    print("Streaming audio data...")

    # Create a BytesIO object to hold audio data
    audio_stream = BytesIO()

    # Write each chunk of audio data to the stream
    for chunk in response:
        if chunk:
            audio_stream.write(chunk)

    # Reset stream position to the beginning
    audio_stream.seek(0)

    # Return the stream for further use
    return audio_stream


    # # Yield each chunk of audio data 웹소켓 연결을 위한
    # for chunk in response:
    #     yield chunk


if __name__ == "__main__":
    text_to_speech_stream("Hello, world! This is using the streaming API.")