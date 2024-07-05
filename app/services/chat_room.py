
from sqlalchemy.orm import Session
from ..models.chat import Chat as ChatModel # ..models.chat에서 Chat 클래스를  ChatModel로 씀
from ..models.chatBubble import ChatBubble as ChatBubbleModel
from ..models.TTS import TTS as TTSModel
from ..models.Image import Image as ImageModel

#내가 원하는것은 get_chats 이함수는 특정한 채팅방 id를 받고 그 아이디가 데이터 베이스에 있는 아이디랑 같으면 그 망풍선들마다의 정보를 가져오는 것
def get_chats(db: Session, chat_id: int): #클라이언트가 알고싶어하는 채팅방 id가 chat_id임

     chat=  db.query(ChatModel).filter(ChatModel.id == chat_id, ChatModel.is_deleted == False) #Chat 클래스의 id가  chat_id: int애랑 같으면 특정한 채팅방에 대한 정보를 조회
     bubbles=db.query(ChatBubbleModel).filter(ChatBubbleModel.is_deleted == False,ChatBubbleModel.chat_id == chat_id).all()     ## 특정방의 말풍선들정보를 가지고 옴

     for bubble in bubbles:
          tts_count = db.query(TTSModel).filter(TTSModel.chat_bubble_id == bubble.id).count()
          image_count = db.query(ImageModel).filter(ImageModel.chat_bubble_id == bubble.id).count()
          bubble.tts_count = tts_count
          bubble.image_count = image_count

    ##특정방의 말풍선 정보 + TTs랑 이미지 값을 한번에 보여줘야함 그떄 알기위해선 bubbles를 반복문으로 돌면서 각 bubble의 아이디를 통해서tts와 이미지의 갯수를 조회해옴 bubbletts와 이미지의 외래키인 chatbubble_id 이
     return {
          "chat": chat,
          "bubbles": bubbles
     }
