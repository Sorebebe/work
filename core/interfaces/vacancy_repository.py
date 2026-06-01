from abc import ABC, abstractmethod
from typing import List, Optional
from core.entities.vacancy import Vacancy


class VacancyRepository(ABC):
    @abstractmethod
    def get_by_id(self, vacancy_id: int) -> Optional[Vacancy]:
        pass
    
    @abstractmethod
    def get_all(self, sphere: Optional[str] = None) -> List[Vacancy]:
        pass
    
    @abstractmethod
    def save(self, vacancy: Vacancy) -> Vacancy:
        pass

    @abstractmethod
    def update(self, vacancy: Vacancy) -> Vacancy:
        pass

    @abstractmethod
    def delete(self, vacancy_id: int) -> bool:
        pass