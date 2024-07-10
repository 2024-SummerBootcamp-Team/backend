from langchain_core.messages import HumanMessage
from sqlalchemy.orm import Session

from app.config.langChain.langChainSetting import runnable_with_history
from app.models import Bubble


def get_bubble(db: Session, bubble_id: int):
    return db.query(Bubble).filter(Bubble.id == bubble_id,Bubble.is_deleted == False).first()


async def create_bubble(chat_id: int, content: str, db: Session):
    db_bubble = Bubble(chat_id=chat_id, content=f'{chat_id}')
    db.add(db_bubble)
    db.commit()
    db.refresh(db_bubble)

    async for chunk in runnable_with_history.astream(
        [HumanMessage(content=content)],
        config={"configurable": {"session_id": str(chat_id)}}
    ):
        yield f'data: {chunk.content}\n\n'

