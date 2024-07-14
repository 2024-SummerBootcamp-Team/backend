import asyncio
import base64
import json
from io import BytesIO

from langchain_core.messages import HumanMessage
from sqlalchemy.orm import Session

from app.config.langChain.langChainSetting import runnable_with_history
from app.models import Bubble

from app.config.elevenlabs.text_to_speech_stream import tts_stream


# 채팅 내용 조회
def get_bubble(db: Session, bubble_id: int):
    return db.query(Bubble).filter(Bubble.id == bubble_id, Bubble.is_deleted == False).first()


# This is a placeholder for the actual GPT stream generator.
async def async_gpt_stream(text: str, message_queue: asyncio.Queue, chat_id: int):
    ai_message = ""
    message_buffer = ""
    tts_queue = asyncio.Queue()
    loop = asyncio.get_event_loop()
    tts_task = loop.create_task(async_tts_stream(message_queue, tts_queue))

    try:
        async for chunk in runnable_with_history.astream(
                [HumanMessage(content=text)],
                config={"configurable": {"session_id": str(chat_id)}}
        ):
            ai_message += chunk.content
            message_buffer += chunk.content
            await message_queue.put(json.dumps({"message": chunk.content}))

            if any(keyword in chunk.content for keyword in [".", "!", "?"]) or (
                    chunk.response_metadata and message_buffer.isalpha()):
                # 테스크를 생성하고
                await tts_queue.put(message_buffer)
                message_buffer = ""

        await tts_queue.put(None)

        # 생성한 테스크가 모두 종료되길 기다립니다.
        await tts_task

        await message_queue.put(None)

    except Exception as e:
        await message_queue.put(json.dumps({"error": str(e)}))
        await tts_queue.put(None)
        ai_message = "에러가 발생했습니다."

    return ai_message


# This is a placeholder for the actual TTS stream generator.
async def async_tts_stream(message_queue: asyncio.Queue, tts_queue: asyncio.Queue):
    while True:
        text = await tts_queue.get()
        if text is None:
            break
        try:
            async for audio_chunk in tts_stream(text):
                encoded_audio = audio_chunk.hex()
                await message_queue.put(json.dumps({"audio": encoded_audio}))
        except Exception as e:
            await message_queue.put(json.dumps({"error": str(e)}))


# 채팅하기: ai 답변 요청
async def create_bubble(chat_id: int, content: str, db: Session):
    response_queue = asyncio.Queue()
    loop = asyncio.get_event_loop()
    gpt_task = loop.create_task(async_gpt_stream(text=content, message_queue=response_queue, chat_id=chat_id))

    while not gpt_task.done():
        message = await response_queue.get()
        if message is None:
            break
        if message.startswith('{"error":'):
            yield f"data: {message}\n\n"
            raise Exception(message)
        yield f"data: {message}\n\n"

    # Save the final AI message to the database
    ai_message = await gpt_task
    db_bubble_ai = Bubble(chat_id=chat_id, writer=0, content=ai_message)
    db.add(db_bubble_ai)
    db.commit()
