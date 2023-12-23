import azure.functions as func  # type: ignore
from azure.core.credentials import AzureKeyCredential  # type: ignore
from azure.ai.textanalytics import TextAnalyticsClient  # type: ignore
import datetime
import json
import logging
import os

app = func.FunctionApp()

endpoint = os.environ["AZURE_LANGUAGE_ENDPOINT"]
key = os.environ["AZURE_LANGUAGE_KEY"]


@app.route(route="HttpExample", auth_level=func.AuthLevel.ANONYMOUS)
def HttpExample(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    name = req.params.get("name")
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get("name")

    if name:
        return func.HttpResponse(
            f"Hello, {name}. This HTTP triggered function executed successfully."
        )
    else:
        return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
            status_code=200,
        )


@app.route(route="detect_language", auth_level=func.AuthLevel.ANONYMOUS)
def detect_language(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    sentence = req.params.get("sentence")
    if not sentence:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            sentence = req_body.get("sentence")

    text_analytics_client = TextAnalyticsClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )
    detected_language = text_analytics_client.detect_language(
        [
            sentence,
        ]
    )
    result = detected_language[0]

    if result.primary_language:
        return func.HttpResponse(
            f"detected language of sentence '{sentence}': {result.primary_language.name} with confidence score {result.primary_language.confidence_score}",
            status_code=200,
        )
    else:
        return func.HttpResponse(
            "The HTTP Trigger Function is running but received either no or no useful input. Pass a query string like /?sentence=i+like+clouds",
            status_code=200,
        )


@app.route(route="detect_sentiment", auth_level=func.AuthLevel.ANONYMOUS)
def detect_sentiment(req: func.HttpRequest) -> func.HttpResponse:
    sentence = req.params.get("sentence")
    if not sentence:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            sentence = req_body.get("sentence")

    text_analytics_client = TextAnalyticsClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )
    sentiment = text_analytics_client.analyze_sentiment(
        [
            sentence,
        ]
    )
    result = sentiment[0]

    if result.sentiment:
        return func.HttpResponse(
            f"detected sentiment of sentence {sentence}: {result.sentiment}",
            status_code=200,
        )
    else:
        return func.HttpResponse(
            "The HTTP Trigger Function is running but received either no or no useful input. Pass a query string like /?sentence=i+like+clouds",
            status_code=500,
        )
    return sentence
