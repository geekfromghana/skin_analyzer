
import random
from typing import Dict, List
from PIL import Image

SKIN_TYPES = ["Oily", "Dry", "Combination", "Normal", "Sensitive"]
ISSUES_POOL = ["Acne", "Hyperpigmentation", "Dark Spots",
               "Wrinkles", "Texture", "Redness", "Pores"]


def analyze_image(image_path: str) -> Dict:
    try:
        img = Image.open(image_path).convert('L')
        pixels = list(img.getdata())
        avg_brightness = sum(pixels) / len(pixels)
    except Exception:
        avg_brightness = 127.0

    seed = int(avg_brightness * 1000) % 2**32
    random.seed(seed)

    skin_type = random.choice(SKIN_TYPES)
    num_issues = 1 if avg_brightness > 170 else 2 if avg_brightness > 90 else 3
    issues: List[str] = random.sample(ISSUES_POOL, k=num_issues)
    confidence = round(
        min(0.95, max(0.5, (avg_brightness / 255) * 0.9 + 0.05)), 2)

    return {
        "skin_type": skin_type,
        "issues": issues,
        "confidence": confidence,
        "metrics": {"avg_brightness": round(avg_brightness, 2)}
    }
