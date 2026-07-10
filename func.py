from flask import Flask, session, render_template, request, url_for, redirect
import os
import  dotenv
import secrets
import requests
import openai



import os
from dotenv import load_dotenv
import requests

# Загружаем переменные из .env при старте модуля
load_dotenv()

def weather_f(city):
    key = os.getenv("weatherapi_key")
    if not key:
        return ["Ошибка: не задан ключ weatherapi_key в .env"]

    url = f"http://api.weatherapi.com/v1/current.json?key={key}&q={city}&aqi=no"
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        return [f"Ошибка запроса погоды: {response.status_code}"]

    data = response.json()
    current = data.get("current", {})

    temp = f"Температура: {current.get('temp_c', '?')} °C (ощущается как {current.get('feelslike_c', '?')}°C)"
    humidity = f"Влажность: {current.get('humidity', '?')} %"
    wind_kph = f"Ветер: {current.get('wind_kph', '?')} км/ч"
    chance_of_rain = f"Шанс дождя: {current.get('chance_of_rain', '?')}"
    uv = f"УФ‑индекс: {current.get('uv', '?')}"
    cloud = f"Облачность: {current.get('cloud', '?')}"
    vis_km = f"Видимость: {current.get('vis_km', '?')} км"
    pressure_mb = f"Давление: {current.get('pressure_mb', '?')} мбар"

    return [temp, humidity, wind_kph, chance_of_rain, uv, cloud, vis_km, pressure_mb]


YANDEX_MODEL = "yandexgpt-lite"
YANDEX_API_KEY = os.getenv("YANDEX_API_KEY")
YANDEX_FOLDER_ID = os.getenv("YANDEX_FOLDER_ID")



def answer(data, city, occasion):
    if not YANDEX_API_KEY or not YANDEX_FOLDER_ID:
        return "Ошибка: не заданы YANDEX_API_KEY или YANDEX_FOLDER_ID в .env"

    prompt = f"Ответь, что лучше одеть для ситуации {occasion} в городе {city}, если там такие погодные условия: {'; '.join(data)}"

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Authorization": f"Api-Key {YANDEX_API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "modelUri": f"gpt://{YANDEX_FOLDER_ID}/{YANDEX_MODEL}",
        "completionOptions": {
            "temperature": 0.8,
            "maxTokens": 1500
        },
        "messages": [
            {"role": "user", "text": prompt}
        ]
    }

    resp = requests.post(url, json=body, headers=headers, timeout=30)
    if resp.status_code != 200:
        return f"Ошибка вызова Yandex GPT: {resp.status_code}, {resp.text}"

    result = resp.json()
    candidates = result.get("result", {}).get("alternatives", [])
    if not candidates:
        return "Не удалось получить ответ от модели"

    text = candidates[0].get("message", {}).get("text", "")
    return text.replase("*", "")
