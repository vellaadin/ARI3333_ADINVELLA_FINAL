import time
import requests
from dotenv import load_dotenv
import os

load_dotenv("apis.env")


#api token
API_TOKEN_LLAMA3 = os.getenv("API_TOKEN_LLAMA3")
API_URL_LLAMA3 = os.getenv("API_URL_LLAMA3")


def generate_story(prompt, max_tokens=2000, temperature=0.7, retries=5):
    headers = {"Authorization": f"Bearer {API_TOKEN_LLAMA3}"}
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": max_tokens,
            "temperature": temperature,
        },
    }

    for attempt in range(retries):
        response = requests.post(API_URL_LLAMA3, headers=headers, json=payload)

        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and "generated_text" in data[0]:
                generated_text = data[0]["generated_text"]

                #removing prompt from the outputted generated text
                if generated_text.startswith(prompt):
                    generated_text = generated_text[len(prompt):].strip()

                return generated_text
            else:
                raise Exception("!! ERROR: Unexpected response format: " + str(data))
        elif response.status_code == 503:
            print(f"\n-- CAUTION: Model is loading, retrying in 10 seconds... (Attempt {attempt + 1}/{retries})")
            time.sleep(10)
        else:
            raise Exception(f"!! ERROR: Failed to generate text: {response.status_code}, {response.text}")

    raise Exception("!! ERROR: Failed to generate text following numerous retries !!")
