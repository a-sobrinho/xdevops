import json

from core.serializers import OperationSerializer
from opentelemetry import trace
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


# Create your views here.
class CalculatorViewSet(viewsets.ViewSet):
    @action(detail=False, methods=["post"])
    def sum(self, request):
        span = trace.get_current_span()

        span.set_attribute("operation.request_data", json.dumps(request.data))
        serializer = OperationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        span.set_attribute("operation.serialized_data", json.dumps(serializer.data))

        num1 = serializer.data["num1"]
        num2 = serializer.data["num2"]
        total = num1 + num2
        span.set_attribute("operation.total", total)

        return Response({"total": total})
