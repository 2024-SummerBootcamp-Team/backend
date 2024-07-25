from typing import List

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from . import image_service, voice_service, chat_service
from ..models import Chat
from ..models.character import Character
from ..schemas.character import CharacterDetail
from ..schemas.dashboard import SpicyFrequency, TopicFrequency, DashboardTotal, CharacterStats, DashboardCharacter, \
    CharacterInfo, ImageInfo, VoiceInfo


def get_character(db: Session, character_id: int):
    return db.query(Character).filter(Character.id == character_id).first()


def get_character_by_name(db: Session, character_name: str):
    return db.query(Character).filter(Character.name == character_name).first()


def get_characters(db: Session, skip: int = 0, limit: int = 100):
    characters = db.query(Character).filter(Character.is_deleted == False).offset(skip).limit(limit).all()
    character_list = [CharacterDetail(id=character.id, name=character.name, image_url=character.image_url) for character
                      in characters]
    return character_list


# 대시보드 관련
def get_topic_count(db: Session, character_id: int, topic: str) -> int:
    return db.query(func.count(Chat.id)).filter(Chat.character_id == character_id, Chat.topic == topic).scalar()


# 매운맛 점수 구간 개수 구하기
def get_spicy_frequency(db: Session, character_id: int) -> SpicyFrequency:
    chats = db.query(Chat).filter(Chat.character_id == character_id).all()
    spicy_count = get_spicy_count(chats)
    return SpicyFrequency(
        level_0_20=spicy_count["0-20"],
        level_20_40=spicy_count["20-40"],
        level_40_60=spicy_count["40-60"],
        level_60_80=spicy_count["60-80"],
        level_80_100=spicy_count["80-100"]
    )


def get_spicy_count(chats) -> dict:
    spicy_count = {
        "0-20": 0,
        "20-40": 0,
        "40-60": 0,
        "60-80": 0,
        "80-100": 0
    }
    for chat in chats:
        spicy = chat.spicy
        if spicy is None:
            continue  # spicy가 None인 경우 해당 chat을 건너뜁니다.
        if 0 <= spicy < 20:
            spicy_count["0-20"] += 1
        elif 20 <= spicy < 40:
            spicy_count["20-40"] += 1
        elif 40 <= spicy < 60:
            spicy_count["40-60"] += 1
        elif 60 <= spicy < 80:
            spicy_count["60-80"] += 1
        elif 80 <= spicy <= 100:
            spicy_count["80-100"] += 1
    return spicy_count


# 매운맛 점수 평균 구하기
def get_spicy_average(db: Session, character_id: int):
    chats = chat_service.get_chat_by_character_id(db, character_id)
    if not chats:  # chats가 비어있으면 0.0을 반환합니다.
        return 0.0
    total_spicy = sum(chat.spicy if chat.spicy is not None else 0 for chat in chats)
    return round((total_spicy / len(chats)), 1) # 소수점 첫째자리까지 반올림


# 전체 통계
def get_dashboard_total(db: Session):
    characters = get_characters(db)
    return DashboardTotal(
        characters=[
            CharacterStats(
                name=character.name,
                chat_count=chat_service.get_chat_count(db, character.id),
                topic_frequency=TopicFrequency(
                    취업=get_topic_count(db, character.id, "취업"),
                    학업=get_topic_count(db, character.id, "학업"),
                    인간관계=get_topic_count(db, character.id, "인간관계"),
                    연애=get_topic_count(db, character.id, "연애")
                ),
                spicy_frequency=get_spicy_frequency(db, character.id)
            )
            for character in characters
        ]
    )


# 캐릭터 별 통계
def get_dashboard_character(db: Session, character_name: str):
    character = get_character_by_name(db, character_name)
    if not character:
        raise HTTPException(status_code=404, detail="캐릭터를 찾을 수 없습니다.")
    images = image_service.get_top_images_by_character(db, character.id)
    voices = voice_service.get_top_voices_by_character(db, character.id)
    return DashboardCharacter(
        info=CharacterInfo(
            id=character.id,
            name=character.name,
            description="설명"
        ),
        top_images=[
            ImageInfo(
                id=image.id,
                url=image.image_url,
                download=image.i_count
            )
            for image in images
        ],
        top_voices=[
            VoiceInfo(
                id=voice.id,
                content=voice.content,
                url=voice.audio_url,
                download=voice.v_count
            )
            for voice in voices
        ],
        topic_frequency=TopicFrequency(
            취업=get_topic_count(db, character.id, "취업"),
            학업=get_topic_count(db, character.id, "학업"),
            인간관계=get_topic_count(db, character.id, "인간관계"),
            연애=get_topic_count(db, character.id, "연애")
        ),
        average_spice_level=get_spicy_average(db, character.id)
    )
