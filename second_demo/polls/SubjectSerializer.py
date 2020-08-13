from rest_framework.serializers import ModelSerializer
from .views import Subject


class SubjectSerializer(ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"
