from datetime import datetime
from core.entities.response import Response
from core.interfaces.response_repository import ResponseRepository
from core.interfaces.vacancy_repository import VacancyRepository


class RespondToVacancyUseCase:
    def __init__(self, response_repo: ResponseRepository, vacancy_repo: VacancyRepository):
        self.response_repo = response_repo
        self.vacancy_repo = vacancy_repo
    
    def execute(self, vacancy_id: int, first_name: str, last_name: str, phone: str) -> Response:
        vacancy = self.vacancy_repo.get_by_id(vacancy_id)
        if vacancy is None:
            raise ValueError("Вакансия не найдена")
        
        response = Response(
            id=None,
            vacancy_id=vacancy_id,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            created_at=datetime.now()
        )
        return self.response_repo.create(response)