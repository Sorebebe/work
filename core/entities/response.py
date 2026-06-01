from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import re


@dataclass
class Response:
    id: Optional[int]
    vacancy_id: int
    first_name: str
    last_name: str
    phone: str
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        if not self.first_name or len(self.first_name) < 2:
            raise ValueError("Имя должно содержать минимум 2 символа")