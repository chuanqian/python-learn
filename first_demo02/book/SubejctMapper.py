from bpmappers.djangomodel import ModelMapper
from bpmappers import RawField

from .models import Subject


class SubjectMapper(ModelMapper):
    isHost = RawField("is_host")

    class Meta:
        model = Subject
        exclude = ("is_host")
