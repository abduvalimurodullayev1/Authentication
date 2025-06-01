from rest_framework import serializers

from apps.common.models import Something


class SomethingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Something
        fields = ("id", "title", "description")
