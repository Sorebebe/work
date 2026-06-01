from typing import Optional
from core.interfaces.vacancy_repository import VacancyRepository


class ListVacanciesUseCase:
    def __init__(self, vacancy_repo: VacancyRepository):
        self.vacancy_repo = vacancy_repo
    
    def execute(self, sphere: Optional[str] = None, page: int = 1, page_size: int = 5) -> dict:
        all_vacancies = self.vacancy_repo.get_all(sphere=sphere)
        total = len(all_vacancies)
        
        start = (page - 1) * page_size
        end = start + page_size
        
        return {
            'items': all_vacancies[start:end],
            'total': total,
            'page': page,
            'total_pages': (total + page_size - 1) // page_size if total > 0 else 1
        }