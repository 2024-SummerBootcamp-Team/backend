from sqlalchemy import Column, Integer, String,DateTime,Boolean,ForeignKey
from ..database.session import Base



class Chat(Base):
    #클래스 명은 대문자
    __tablename__ = "chat"

    id = Column(Integer, primary_key=True, autoincrement=True)
    character_id = Column(Integer, ForeignKey('character.id'), nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    name = Column(String(45), nullable=False)

    # character = relationship("Character", back_populates="chats")
    # bubbles = relationship("ChatBubble", back_populates="chat")

    # 1= relationship("2", back_populates="3") 이라고 가정하면
    # 1 여기서 "1"은 클래스 내에서 사용할 변수 이름을 의미합니다. 이 변수는 관계된 객체를 참조하는 데 사용됩니다.예를 들어, ChatModel 클래스에서 bubbles라는 변수를 사용하면 ChatBubble 객체들의 목록을 참조할 수 있습니다
    # 2 여기서 "2"는 관계를 설정할 대상 클래스의 이름입니다. 이 클래스는 문자열로 작성되며, 관계를 맺을 테이블을 정의합니다.예를 들어, ChatBubble 클래스와 관계를 맺고 싶다면 "ChatBubble"이라고 작성합니다.
    # 3 여기서 "3"는 반대쪽 클래스에서 이 관계를 역참조하는 변수 이름입니다. back_populates를 사용하여 양방향 관계를 정의합니다. 예를 들어, ChatBubble 클래스에서 chat이라는 변수로 ChatModel을 역참조한다면, back_populates="chat"이라고 작성합니다.