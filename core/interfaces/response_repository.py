from abc import ABC, abstractmethod
from typing import List
from core.entities.response import Response


class ResponseRepository(ABC):
    @abstractmethod
    def create(self, response: Response) -> Response:
        pass