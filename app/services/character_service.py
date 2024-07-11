from sqlalchemy.orm import Session
from ..models.character import Character as CharacterModel


def get_character_id_by_name(db: Session, character_name: str):
    return db.query(CharacterModel).filter(CharacterModel.name == character_name).first()