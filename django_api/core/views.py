from core.models import Counter
from core.serializers import AddCounterSerializer, CounterSerializer
from django.shortcuts import get_object_or_404
from opentelemetry import trace
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

tracer = trace.get_tracer(__name__)


class CounterViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        [counter, created] = Counter.objects.get_or_create(id=pk)
        counter_serializer = CounterSerializer(counter)

        return Response(counter_serializer.data)

    def update(self, request, pk=None):
        add_counter_serializer = AddCounterSerializer(data=request.data)
        add_counter_serializer.is_valid(raise_exception=True)

        counter = get_object_or_404(Counter, pk=pk)

        counter.value += add_counter_serializer.data["value"]
        counter.save()

        counter_serializer = CounterSerializer(counter)

        return Response(counter_serializer.data)
