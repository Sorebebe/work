from core.entities.vacancy import Vacancy
from core.interfaces.vacancy_repository import VacancyRepository


class UpdateVacancyUseCase:
    def __init__(self, vacancy_repo: VacancyRepository):
        self.vacancy_repo = vacancy_repo
    
    def execute(self, vacancy_id: int, title: str, sphere: str, user_id: int, is_admin: bool = False) -> Vacancy:
        vacancy = self.vacancy_repo.get_by_id(vacancy_id)
        if vacancy is None:
            raise ValueError("Вакансия не найдена")
        
        if not vacancy.can_be_edited_by(user_id, is_admin):
            raise PermissionError("Нет прав для редактирования")
        
        updated = Vacancy(
            id=vacancy.id,
            title=title,
            company=vacancy.company,
            sphere=sphere,
            employer_id=vacancy.employer_id,
            created_at=vacancy.created_at
        )
        return self.vacancy_repo.update(updated)


class DeleteVacancyUseCase:
    def __init__(self, vacancy_repo: VacancyRepository):
        self.vacancy_repo = vacancy_repo
    
    def execute(self, vacancy_id: int, user_id: int, is_admin: bool = False) -> bool:
        vacancy = self.vacancy_repo.get_by_id(vacancy_id)
        if vacancy is None:
            raise ValueError("Вакансия не найдена")
        
        if not vacancy.can_be_edited_by(user_id, is_admin):
            raise PermissionError("Нет прав для удаления")
        
        return self.vacancy_repo.delete(vacancy_id)