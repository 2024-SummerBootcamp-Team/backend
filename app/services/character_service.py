from sqlalchemy import func
from sqlalchemy.orm import Session

from ..models import Chat
from ..models.character import Character
from ..schemas.character import CharacterDetail
from ..schemas.dashboard import SpicyFrequency, TopicFrequency, DashboardTotal, CharacterStats


def get_character(db: Session, character_id: int):
    return db.query(Character).filter(Character.id == character_id).first()


def get_character_by_name(db: Session, character_name: str):
    return db.query(Character).filter(Character.name == character_name).first()


def get_characters(db: Session, skip: int = 0, limit: int = 100):
    characters = db.query(Character).filter(Character.is_deleted == False).offset(skip).limit(limit).all()
    character_list = [CharacterDetail(id=character.id, name=character.name, image_url=character.image_url) for character in characters]
    return character_list


# 대시보드 관련
def get_topic_count(db: Session, character_id: int, topic: str) -> int:
    """주어진 topic의 채팅 수를 반환하는 함수"""
    return db.query(func.count(Chat.id)).filter(Chat.character_id == character_id, Chat.topic == topic).scalar()

def get_dashboard_total(db: Session):
    characters = get_characters(db)
    print("characters: ", characters)
    return DashboardTotal(
        characters=[
            CharacterStats(
                name=character.name,
                topic_frequency=TopicFrequency(
                    취업=get_topic_count(db, character.id, "취업"),
                    학업=get_topic_count(db, character.id, "학업"),
                    인간관계=get_topic_count(db, character.id, "인간관계"),
                    연애=get_topic_count(db, character.id, "연애")
                ),
                spicy_frequency=SpicyFrequency(
                    level_1_2=7,
                    level_2_4=15,
                    level_5_6=10,
                    level_7_8=10,
                    level_9_10=8
                )
            )
            for character in characters
        ]
    )
