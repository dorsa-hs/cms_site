from rest_framework.serializers import ModelSerializer

from django_jalali.serializers.serializerfield import (
    JDateField, JDateTimeField,
)

from .models import Post


class JDateFieldSerializer(ModelSerializer):
    date = JDateField()

    class Meta:
        model = Post
        exclude = []

