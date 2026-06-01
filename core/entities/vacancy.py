from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class Sphere(Enum):
    IT = "IT"
    MEDICINE = "MEDICINE"
    ARCHITECTURE = "ARCHITECTURE"
    
    @classmethod
    def choices(cls):
        return [(item.value, cls.get_display(item.value)) for item in cls]
    
    @classmethod
    def get_display(cls, value: str) -> str:
        displays = {
            "IT": "Информационные технологии",
            "MEDICINE": "Медицина",
            "ARCHITECTURE": "Архитектура"
        }
        return displays.get(value, value)


@dataclass
class Vacancy:
    id: Optional[int]
    title: str
    company: str
    sphere: str
    employer_id: int
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        if not self.title or len(self.title) < 3:
            raise ValueError("Название вакансии должно содержать минимум 3 символа")
    
    @property
    def sphere_display(self) -> str:
        return Sphere.get_display(self.sphere)
    
    def get_sphere_display(self) -> str:
        return self.sphere_display
    
    def can_be_edited_by(self, user_id: int, is_admin: bool = False) -> bool:
        if is_admin:
            return False
        return self.employer_id == user_id

    def can_be_deleted_by(self, user_id: int, is_admin: bool = False) -> bool:
        return is_admin or self.employer_id == user_id