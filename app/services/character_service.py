from sqlalchemy.orm import Session
from ..models.character import Character as CharacterModel


def get_character(db: Session, character_id: int):
    return db.query(CharacterModel).filter(CharacterModel.id == character_id).first()


def get_character_by_name(db: Session, character_name: str):
    return db.query(CharacterModel).filter(CharacterModel.name == character_name).first()