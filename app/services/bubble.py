from sqlalchemy.orm import Session
from app.models.chat import Chat as ChatModel
from app.models.bubble import ChatBubble as ChatBubbleModel
from app.models.voice import Voice as TTSModel
from app.models.image import Image as ImageModel
from app.schemas.chat import ChatRoomBase

# 내가 원하는것은 get_chats 이함수는 특정한 채팅방 id를 받고 그 아이디가 데이터 베이스에 있는 아이디랑 같으면 그 망풍선들마다의 정보를 가져오는 것
def get_bubbles(db: Session, chat_id: int): # 클라이언트가 알고싶어하는 채팅방 id가 chat_id임

     #chat =  db.query(ChatModel).filter(ChatModel.id == chat_id) #Chat 클래스의 id가  chat_id: int애랑 같으면 특정한 채팅방에 대한 정보를 조회
     bubbles = db.query(ChatBubbleModel).filter(ChatBubbleModel.chat_id == chat_id).all()     # 특정방의 말풍선들정보를 가지고 옴

     result = []
     for bubble in bubbles:
          tts_count = db.query(TTSModel).filter(TTSModel.chatbubble_id == bubble.id).count()
          image_count = db.query(ImageModel).filter(ImageModel.chatbubble_id == bubble.id).count()

          bubble_form = ChatRoomBase(
               id=bubble.id,
               writer=bubble.writer,
               category=bubble.category,
               content=bubble.content,
               created_at=bubble.created_at,
               tts_count=tts_count,
               image_count=image_count,
          )
          result.append(bubble_form)

     # 특정방의 말풍선 정보 + TTs랑 이미지 값을 한번에 보여줘야함 그떄 알기위해선 bubbles를 반복문으로 돌면서 각 bubble의 아이디를 통해서tts와 이미지의 갯수를 조회해옴 bubbletts와 이미지의 외래키인 chatbubble_id 이
     return result
