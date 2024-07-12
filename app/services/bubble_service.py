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
    return db.query(Bubble).filter(Bubble.id == bubble_id,Bubble.is_deleted == False).first()




# 채팅하기: ai 답변 요청
async def create_bubble(chat_id: int, content: str, db: Session):
    db_bubble_human = Bubble(chat_id=chat_id, writer=1, content=content)
    db.add(db_bubble_human)

    ai_message = ""
    message_buffer = ""

    async for chunk in runnable_with_history.astream(
        [HumanMessage(content=content)],
        config={"configurable": {"session_id": str(chat_id)}}
    ):
        ai_message += chunk.content
        message_buffer += chunk.content

        # 문장에 키워드 . ! ?가 있을 경우 음성으로 변환
        if any(keyword in chunk.content for keyword in [".", "!", "?"]):
            async for audio_chunk in tts_stream(message_buffer):
                encoded_audio = base64.b64encode(audio_chunk).decode("utf-8")
                yield f'data: {json.dumps({"audio": encoded_audio})}\n\n'
            message_buffer = ""

        yield f'data: {json.dumps({"message": chunk.content})}\n\n'

    db_bubble_ai = Bubble(chat_id=chat_id, writer=0, content=ai_message)
    db.add(db_bubble_ai)
    db.commit()

