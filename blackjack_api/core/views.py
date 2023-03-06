import random

import requests
from core.models import Blackjack
from opentelemetry import trace
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


def get_deal():
    return random.randint(1, 13)


def get_cheat_deal() -> int:
    raise RuntimeError("You are trying to cheat")


class BlackjackViewSet(viewsets.ViewSet):
    @action(detail=False, methods=["get"])
    def deal(self, _):
        span = trace.get_current_span()

        [blackjack, created] = Blackjack.objects.get_or_create(id=1)
        span.set_attribute("operation.new_round", created)
        initial_value = blackjack.value
        span.set_attribute("operation.initial_value", initial_value)

        deal = get_deal()
        span.set_attribute("operation.deal", deal)

        response = requests.post(
            "http://calculator-api:8002/api/calculator/sum/",
            json={"num1": blackjack.value, "num2": deal},
        )

        json_response = response.json()

        blackjack.value = int(json_response["total"])
        blackjack.save()

        final_value = blackjack.value
        span.set_attribute("operation.final_value", final_value)

        return Response(
            dict(
                initial_value=initial_value,
                deal=deal,
                final_value=final_value,
            )
        )

    @action(detail=False, methods=["get"])
    def new(self, _):
        blackjack = Blackjack.objects.get(pk=1)
        blackjack.delete()

        return Response()

    @action(detail=False, methods=["get"])
    def cheat(self, _):
        span = trace.get_current_span()

        [blackjack, created] = Blackjack.objects.get_or_create(id=1)
        span.set_attribute("operation.new_round", created)
        initial_value = blackjack.value
        span.set_attribute("operation.initial_value", initial_value)

        deal = get_cheat_deal()
        span.set_attribute("operation.deal", deal)

        response = requests.post(
            "http://calculator-api:8002/api/calculator/sum/",
            json={"num1": blackjack.value, "num2": deal},
        )

        json_response = response.json()

        blackjack.value = int(json_response["total"])
        blackjack.save()

        final_value = blackjack.value
        span.set_attribute("operation.final_value", final_value)

        return Response(
            dict(
                initial_value=initial_value,
                deal=deal,
                final_value=final_value,
            )
        )
