
# Mobile Image Analysis API

A lightweight backend service for mobile apps to **upload images** and receive **structured analysis results**. Built with **Python** and **FastAPI**; uses the **local filesystem** for storage.

---

## ✅ Features
- RESTful API with FastAPI
- Image upload (JPEG/PNG), validated file type and size (≤ 5 MB)
- Mocked analysis logic with deterministic outputs based on image brightness
- Local storage under `data/uploads`
- Optional API key authentication (`x-api-key`)
- Basic logging to `logs/app.log`
- Postman collection as `face analyser.json`

---

## 📂 Project Structure

```
SKIN-ANALYZER/
├── README.md
├── requirements.txt
├── Dockerfile
├── .env
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── upload.py
│   │   └── analyze.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── storage.py
│   │   └── analysis.py
│   └── utils/
│       ├── __init__.py
│       ├── validators.py
│       └── auth.py
├── data/
│   └── uploads/
└── logs/
    └── app.log
```

> If imports fail, ensure `__init__.py` exists in `app/`, `routes/`, `services/`, and `utils/` (empty files are fine).

---

## ⚙️ Requirements

Use Python 3.11+ and the following pinned dependencies:

```txt
fastapi==0.115.2
uvicorn[standard]==0.30.0
python-multipart==0.0.9
pydantic==2.8.2
pydantic-settings==2.4.1
Pillow==10.4.0
```

> If you hit dependency conflicts, upgrade `pip`, clear cache, and reinstall:
>
> ```bash
> pip install --upgrade pip
> pip cache purge
> pip install -r requirements.txt
> ```

---

## 🚀 Getting Started

### 1) Clone the repository
```bash
git clone https://github.com/<your-username>/mobile-ai-backend.git
cd skin-analyzer
```

### 2) Configure environment
Create `.env` from `.env` and adjust if needed:
```env
API_KEY=your_api_key_here   # optional
LOG_LEVEL=INFO
STORAGE_DIR=data/uploads
MAX_FILE_MB=5
```

- If `API_KEY` is set, requests must include the header: `x-api-key: <your_api_key_here>`.
- If `API_KEY` is not set, auth is disabled and endpoints are public.

### 3) Run locally (Python)
```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell
. .\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload
```

Service will be available at:
- Base: `http://127.0.0.1:8001`
- Docs: `http://127.0.0.1:8001/docs`
- Redoc: `http://127.0.0.1:8001/redoc`

> On Windows (especially under OneDrive paths), if `--reload` causes issues:
> - Restrict watcher: `--reload-dir app`
> - Or run without reload: `uvicorn app.main:app --host 127.0.0.1 --port 8001`
> - Or move the project to a non-OneDrive path (e.g., `C:\Dev\skin-analyzer`)

### 4) Run with Docker (optional)
```bash
docker build -t skin-analyzer .
docker run -p 8000:8000 --env-file .env skin-analyzer
```

Service will be available at `http://localhost:8000`.

> If Docker is not installed or restricted, use the Python method above.

---

## 🔌 API Endpoints

### POST `/upload`
Upload a JPEG/PNG image (≤ 5 MB). Returns a generated `image_id`.

**Request (multipart/form-data):**
- `file`: image file (jpeg/png)

**Response:**
```json
{ "image_id": "<uuid-hex>" }
```

**Errors:**
- `400 Bad Request` — unsupported extension/content-type; empty file
- `413 Payload Too Large` — file exceeds size limit
- `401 Unauthorized` — missing/invalid API key (if enabled)

**Examples**

- **PowerShell using curl.exe** (recommended on Windows):
```powershell
curl.exe -X POST "http://127.0.0.1:8001/upload" `
  -H "x-api-key: your_api_key_here" `
  -F "file=@"C:\path\to\image.jpg";type=image/jpeg"
```

- **PowerShell 7 (Invoke-RestMethod)**:
```powershell
$headers = @{ "x-api-key" = "your_api_key_here" }
$form = @{ file = Get-Item "C:\path\to\image.jpg" }
Invoke-RestMethod -Uri "http://127.0.0.1:8001/upload" -Method Post -Headers $headers -Form $form
```

---

### POST `/analyze`
Submit an `image_id` to receive mocked analysis.

**Request (JSON):**
```json
{ "image_id": "<uuid-hex>" }
```

**Response (JSON):**
```json
{
  "image_id": "<uuid-hex>",
  "skin_type": "Oily",
  "issues": ["Hyperpigmentation"],
  "confidence": 0.87,
  "metrics": { "avg_brightness": 123.45 }
}
```

**Examples**

- **PowerShell using curl.exe**:
```powershell
curl.exe -X POST "http://127.0.0.1:8001/analyze" `
  -H "Content-Type: application/json" `
  -H "x-api-key: your_api_key_here" `
  -d "{"image_id":"<uuid-from-upload>"}"
```

- **PowerShell (Invoke-RestMethod)**:
```powershell
$headers = @{ "x-api-key" = "your_api_key_here"; "Content-Type" = "application/json" }
$body = @{ image_id = "<uuid-from-upload>" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://127.0.0.1:8001/analyze" -Method Post -Headers $headers -Body $body
```

---

## 🧪 Analysis Logic (Mock)
- Converts the image to grayscale and calculates **average brightness**
- Seeds a random generator with brightness to produce **deterministic-like** results per image
- Chooses `skin_type` from: `Oily`, `Dry`, `Combination`, `Normal`, `Sensitive`
- Selects 1–3 `issues` from: `Acne`, `Hyperpigmentation`, `Dark Spots`, `Wrinkles`, `Texture`, `Redness`, `Pores`
- Computes a bounded `confidence` score influenced by brightness

> This is intentionally simple (no ML libraries). The aim is to demonstrate backend flow and integration.

---

## 🧰 Postman Collection

A ready-to-import Postman collection is included in the project:
```
face analyzer.json
```

**Usage:**
1. Open Postman → **File → Import** → select the JSON file.
2. Set collection variables:
   - `host` → `http://127.0.0.1:8001`
   - `api_key` → your key (if enabled) or blank
   - `image_path` → e.g., `C:\path\to\image.jpg`
3. Run **Upload image** then **Analyze image** (the collection saves `image_id` automatically in collection variables).

---

## ⚡ PowerShell Test Script

A ready-to-run Windows script is included:
```
scripts/test_api.ps1
```

**Usage:**
```powershell
.\scripts	est_api.ps1 -Host "http://127.0.0.1:8001" -ApiKey "your_api_key_here" -ImagePath "C:\path\to\image.jpg"
```

What it does:
1. Uploads the image using `curl.exe`
2. Captures the `image_id`
3. Calls `/analyze` with that `image_id`
4. Prints the analysis result as formatted JSON

---

## ✅ Assumptions
- Local storage only (no cloud integration)
- Simple deterministic mock analysis; no real AI/ML
- CORS is permissive for development convenience

---

## 🚀 Future Improvements
- Database for image metadata (timestamps, user association)
- Cloud object storage integration
- JWT-based authentication & role-based access
- Background task queue for analysis
- CI/CD pipeline, automated tests (pytest), and code quality checks

---

## 📜 License
MIT

---

## 🧪 Quick Self-Test (Windows)

```powershell
# Start server (PowerShell)
uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload

# Upload
curl.exe -X POST "http://127.0.0.1:8001/upload" `
  -F "file=@"C:\path\to\image.jpg";type=image/jpeg"

# Analyze (replace uuid)
curl.exe -X POST "http://127.0.0.1:8001/analyze" `
  -H "Content-Type: application/json" `
  -d "{"image_id":"<uuid-from-upload>"}"
```
