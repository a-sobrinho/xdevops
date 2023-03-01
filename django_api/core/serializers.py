from rest_framework import serializers
from core.models import Counter


class CounterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Counter
        fields = ["value"]


class AddCounterSerializer(serializers.Serializer):
    value = serializers.IntegerField()
