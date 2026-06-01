from dataclasses import dataclass
from typing import Optional


@dataclass
class EmployerProfile:
    id: Optional[int]
    user_id: int
    company_name: str
    email: str
    address: str
    
    def __post_init__(self):
        if not self.company_name or len(self.company_name) < 2:
            raise ValueError("Название компании должно содержать минимум 2 символа")