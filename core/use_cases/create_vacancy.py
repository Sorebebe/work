from datetime import datetime
from core.entities.vacancy import Vacancy
from core.interfaces.vacancy_repository import VacancyRepository


class CreateVacancyUseCase:
    def __init__(self, vacancy_repo: VacancyRepository):
        self.vacancy_repo = vacancy_repo
    
    def execute(self, title: str, company: str, sphere: str, employer_id: int) -> Vacancy:
        vacancy = Vacancy(
            id=None,
            title=title,
            company=company,
            sphere=sphere,
            employer_id=employer_id,
            created_at=datetime.now()
        )
        return self.vacancy_repo.save(vacancy)