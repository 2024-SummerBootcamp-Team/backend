
# # app/models/__init__.py
# from sqlalchemy.orm import relationship
#
# from .character import Character
# from .chat import Chat
# from .chatBubble import ChatBubble
#
# # 관계 설정
# Character.chats = relationship("Chat", back_populates="character")
# Chat.character = relationship("Character", back_populates="chats")
# Chat.bubbles = relationship("ChatBubble", back_populates="chat")
# ChatBubble.chat = relationship("Chat", back_populates="bubbles")

