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
        span = trace.get_current_span()

        span.set_attribute("operation.counter_id", pk)

        [counter, created] = Counter.objects.get_or_create(id=pk)
        span.set_attribute("operation.counter_value", counter.value)
        span.set_attribute("operation.counter_created", created)

        counter_serializer = CounterSerializer(counter)

        return Response(counter_serializer.data)

    def update(self, request, pk=None):
        span = trace.get_current_span()

        span.set_attribute("operation.counter_id", pk)

        counter = get_object_or_404(Counter, pk=pk)
        span.set_attribute("operation.counter_value_before", counter.value)

        span.set_attribute("operation.request_data", request.data)
        add_counter_serializer = AddCounterSerializer(data=request.data)
        add_counter_serializer.is_valid(raise_exception=True)
        span.set_attribute("operation.serialized_data", add_counter_serializer.data)

        counter.value += add_counter_serializer.data["value"]
        counter.save()
        span.set_attribute("operation.counter_value_after", counter.value)

        counter_serializer = CounterSerializer(counter)

        return Response(counter_serializer.data)
