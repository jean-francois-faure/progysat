from typing import TypeVar, Type

from django.db import models

from django.utils import translation


T = TypeVar("T", bound=models.Model)


def objects_for_current_language(model: Type[models.Model]):
    current_language = translation.get_language()

    return model.objects.filter(locale__language_code=current_language)
