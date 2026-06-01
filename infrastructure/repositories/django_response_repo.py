from typing import List
from core.entities.response import Response
from core.interfaces.response_repository import ResponseRepository
from vacancies.models import Response as DjangoResponse


class DjangoResponseRepository(ResponseRepository):
    
    def _to_domain(self, django_response) -> Response:
        return Response(
            id=django_response.id,
            vacancy_id=django_response.vacancy_id,
            first_name=django_response.first_name,
            last_name=django_response.last_name,
            phone=django_response.phone,
            created_at=django_response.created_at
        )
    
    def create(self, response: Response) -> Response:
        django_response = DjangoResponse.objects.create(
            vacancy_id=response.vacancy_id,
            first_name=response.first_name,
            last_name=response.last_name,
            phone=response.phone
        )
        return self._to_domain(django_response)