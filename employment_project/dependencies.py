from infrastructure.repositories.django_vacancy_repo import DjangoVacancyRepository
from infrastructure.repositories.django_response_repo import DjangoResponseRepository
from core.use_cases.list_vacancies import ListVacanciesUseCase
from core.use_cases.create_vacancy import CreateVacancyUseCase
from core.use_cases.respond_to_vacancy import RespondToVacancyUseCase
from core.use_cases.manage_vacancy import UpdateVacancyUseCase, DeleteVacancyUseCase

_vacancy_repo = DjangoVacancyRepository()
_response_repo = DjangoResponseRepository()

def get_list_vacancies_use_case() -> ListVacanciesUseCase:
    return ListVacanciesUseCase(_vacancy_repo)

def get_create_vacancy_use_case() -> CreateVacancyUseCase:
    return CreateVacancyUseCase(_vacancy_repo)

def get_respond_to_vacancy_use_case() -> RespondToVacancyUseCase:
    return RespondToVacancyUseCase(_response_repo, _vacancy_repo)

def get_update_vacancy_use_case() -> UpdateVacancyUseCase:
    return UpdateVacancyUseCase(_vacancy_repo)

def get_delete_vacancy_use_case() -> DeleteVacancyUseCase:
    return DeleteVacancyUseCase(_vacancy_repo)