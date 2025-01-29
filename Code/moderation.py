import requests
import streamlit as st
import time
from dotenv import load_dotenv
import os

load_dotenv("apis.env")

#API URL for BART Large MNLI
MODERATION_API_URL = os.getenv("MODERATION_API_URL")
MODERATION_API_TOKEN = os.getenv("MODERATION_API_TOKEN")
MODERATION_HEADERS = {"Authorization": MODERATION_API_TOKEN}

#classification candidate labels
CANDIDATE_LABELS = [
    "weapons",
    "violence",
    "erotica",
    "hate-speech",
    "racism",
    "politics",
    "child abuse",
    "drug use",
    "self-harm",
    "animal abuse",
]

#query api
def query_moderation(payload):
    response = requests.post(MODERATION_API_URL, headers=MODERATION_HEADERS, json=payload)
    return response.json()

def classify_prompt(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {
            "candidate_labels": CANDIDATE_LABELS
        }
    }
    result = query_moderation(payload)

    #response structure validation
    if "labels" not in result or "scores" not in result:
        st.error(f"Unexpected API response structure: {result}")
        return {}

    #label and score extraction
    scores = {label: score for label, score in zip(result["labels"], result["scores"])}
    return scores

def is_prompt_appropriate(prompt, threshold=0.5):
    classification_scores = classify_prompt(prompt)

    #categories that were flagged for
    flagged_categories = [
        (category, classification_scores[category])
        for category in CANDIDATE_LABELS
        if classification_scores[category] > threshold
    ]
    
    is_appropriate = len(flagged_categories) == 0

    return is_appropriate, flagged_categories
