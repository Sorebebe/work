from typing import List, Optional
from core.entities.vacancy import Vacancy
from core.interfaces.vacancy_repository import VacancyRepository
from vacancies.models import Vacancy as DjangoVacancy


class DjangoVacancyRepository(VacancyRepository):
    
    def _to_domain(self, django_vacancy) -> Vacancy:
        return Vacancy(
            id=django_vacancy.id,
            title=django_vacancy.title,
            company=django_vacancy.company,
            sphere=django_vacancy.sphere,
            employer_id=django_vacancy.employer_id,
            created_at=django_vacancy.created_at
        )
    
    def get_by_id(self, vacancy_id: int) -> Optional[Vacancy]:
        try:
            return self._to_domain(DjangoVacancy.objects.get(id=vacancy_id))
        except DjangoVacancy.DoesNotExist:
            return None
    
    def get_all(self, sphere: Optional[str] = None) -> List[Vacancy]:
        queryset = DjangoVacancy.objects.all()
        if sphere:
            queryset = queryset.filter(sphere=sphere)
        return [self._to_domain(v) for v in queryset]
    
    def save(self, vacancy: Vacancy) -> Vacancy:
        django_vacancy = DjangoVacancy.objects.create(
            title=vacancy.title,
            company=vacancy.company,
            sphere=vacancy.sphere,
            employer_id=vacancy.employer_id,
            created_at=vacancy.created_at
        )
        return self._to_domain(django_vacancy)
    
    def update(self, vacancy: Vacancy) -> Vacancy:
        django_vacancy = DjangoVacancy.objects.get(id=vacancy.id)
        django_vacancy.title = vacancy.title
        django_vacancy.sphere = vacancy.sphere
        django_vacancy.save()
        return self._to_domain(django_vacancy)
    
    def delete(self, vacancy_id: int) -> bool:
        deleted, _ = DjangoVacancy.objects.filter(id=vacancy_id).delete()
        return deleted > 0