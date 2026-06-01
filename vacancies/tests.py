from django.test import TestCase
from core.entities.vacancy import Vacancy
from core.use_cases.create_vacancy import CreateVacancyUseCase
from core.interfaces.vacancy_repository import VacancyRepository


class MockVacancyRepository(VacancyRepository):
    def __init__(self):
        self.vacancies = []

    def save(self, vacancy: Vacancy) -> Vacancy:
        vacancy.id = len(self.vacancies) + 1
        self.vacancies.append(vacancy)
        return vacancy

    def get_by_id(self, vacancy_id: int): pass
    def get_all(self, sphere=None): return self.vacancies
    def update(self, vacancy: Vacancy): pass
    def delete(self, vacancy_id: int): pass


class CleanArchitectureTestCase(TestCase):
    def test_create_vacancy_success(self):
        """Проверка успешного создания валидной вакансии"""
        repo = MockVacancyRepository()
        use_case = CreateVacancyUseCase(repo)
        
        vacancy = use_case.execute(
            title="Python разработчик",
            company="Яндекс",
            sphere="IT",
            employer_id=1
        )
        
        self.assertEqual(vacancy.id, 1)
        self.assertEqual(vacancy.title, "Python разработчик")
        self.assertEqual(len(repo.get_all()), 1)

    def test_create_vacancy_validation_error(self):
        """Бизнес-логика должна падать, если название слишком короткое"""
        repo = MockVacancyRepository()
        use_case = CreateVacancyUseCase(repo)
        
        with self.assertRaises(ValueError):
            use_case.execute(
                title="IT",
                company="Google",
                sphere="IT",
                employer_id=1
            )