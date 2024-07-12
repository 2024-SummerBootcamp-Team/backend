from io import BytesIO
from typing import IO, Generator, Iterator, AsyncIterator

from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs, AsyncElevenLabs

client = ElevenLabs()

async_client = AsyncElevenLabs()

def text_to_speech_stream(text: str) -> IO[bytes]:
# async def text_to_speech_stream(text: str) -> Generator[bytes, None, None]:
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
            # time.sleep(1)  # 각 청크 전송 전에 1초 대기

    # Reset stream position to the beginning
    audio_stream.seek(0)

    # Return the stream for further use
    return audio_stream


    # # Yield each chunk of audio data - 웹소켓 연결
    # for chunk in response:
    #     # await asyncio.sleep(1)
    #     yield chunk


def tts_stream(text: str) -> AsyncIterator[bytes]:
    response = async_client.text_to_speech.convert(
        voice_id="Es5AnE58gKPS9Vffyooe",
        optimize_streaming_latency="0",
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_multilingual_v2",
        voice_settings=VoiceSettings(
            stability=0.5,
            similarity_boost=0.75,
            style=0.0,
            use_speaker_boost=True,
        ),
    )
    return response



if __name__ == "__main__":
    text_to_speech_stream("Hello, world! This is using the streaming API.")