# misinfo-assistant

# Misinformation Memory Assistant

A memory-driven AI system for detecting recurring misinformation by
retrieving and reasoning over previously observed claims using a
vector database.

---

## Prerequisites

- Python 3.9+
- Qdrant running locally

---

## Setup

### 1. Start Qdrant (Terminal 1)

```powershell
cd D:\qdrant
.\qdrant.exe

Leave this terminal running.

### **2. Create and activate virtual environment (Terminal 2)**

python -m venv venv
.\venv\Scripts\activate

### **3. Install dependencies**

python -m pip install -r requirements.txt

### **4. Seed the memory (one-time)**

python app/ingest.py

### **5. Start the API**

uvicorn app.main:app --reload

The API will be available at: http://127.0.0.1:8000
Swagger UI: http://127.0.0.1:8000/docs

### **Demo**

Send a POST request to /check-claim with JSON:

{
  "claim": "Does bleach cure covid?"
}



