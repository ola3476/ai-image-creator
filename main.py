import requests
import os
from utils import save_image_from_url

# List of all image APIs to try (fallback order)
IMAGE_APIS = [
    "https://api.giftedtech.co.ke/api/ai/text2img",
    "https://api.giftedtech.co.ke/api/ai/text2ghibli",
    "https://api.giftedtech.co.ke/api/ai/fluximg",
    "https://api.giftedtech.co.ke/api/ai/sd",
    "https://api.giftedtech.co.ke/api/ai/deepimg",
    "https://api.giftedtech.co.ke/api/ai/vision"
]

def try_api(api_url, params):
    try:
        response = requests.get(api_url, params=params, timeout=10)
        response.raise_for_status()
        try:
            data = response.json()
        except Exception:
            print(f"Invalid JSON from {api_url}: {response.text}")
            return None
        image_url = data.get("image") or data.get("url")
        if image_url:
            return image_url
    except Exception as e:
        print(f"API {api_url} failed: {e}")
    return None

def generate_image(prompt):
    apikey = "gifted"  # Replace with your valid API key if you have one
    safe_prompt = prompt.replace(" ", "_")
    output_path = f"static/images/{safe_prompt}.png"
    params = {"apikey": apikey, "prompt": prompt}

    for api_url in IMAGE_APIS:
        image_url = try_api(api_url, params)
        if image_url:
            try:
                save_image_from_url(image_url, output_path)
                return output_path, None
            except Exception as e:
                print(f"Failed to save image: {e}")
                return "static/images/placeholder.png", "Error downloading image."
    return "static/images/placeholder.png", "AI image APIs all failed. Showing placeholder."
