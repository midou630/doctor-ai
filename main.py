# main.py
import os
import requests
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

# --------------------------
# إعداد HuggingFace API Key
# --------------------------
HUGGINGFACE_API_KEY = os.environ.get("HUGGINGFACE_API_KEY")
if not HUGGINGFACE_API_KEY:
    raise ValueError("Please set your HUGGINGFACE_API_KEY in environment variables!")

# استخدام Router API الجديد
API_URL = "https://router.huggingface.co/api/models/mistralai/Mistral-7B-Instruct-v0.2"
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

# --------------------------
# إنشاء تطبيق FastAPI
# --------------------------
app = FastAPI(title="Assistant Médical AI")

# --------------------------
# دالة التحليل
# --------------------------
def assistant_medical_fr(case_text):
    prompt = f"""
Vous êtes un assistant médical intelligent destiné aux médecins.
Analysez le cas clinique suivant sans poser de diagnostic définitif.

Veuillez fournir :
- Des hypothèses générales (non concluantes)
- Des questions complémentaires pertinentes
- Des examens médicaux éventuellement recommandés

⚠️ Mentionnez clairement que la décision finale appartient au médecin.

Cas clinique :
{case_text}
"""

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 600,
            "temperature": 0.7,
            "return_full_text": False
        }
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload)

    if response.status_code != 200:
        return f"Erreur API HuggingFace: {response.text}"

    result = response.json()

    # بعض النماذج قد ترجع قائمة أو dict مباشر
    if isinstance(result, list) and "generated_text" in result[0]:
        return result[0]["generated_text"]
    if isinstance(result, dict) and "generated_text" in result:
        return result["generated_text"]

    return str(result)

# --------------------------
# الصفحة الرئيسية
# --------------------------
@app.get("/", response_class=HTMLResponse)
async def home():
    return """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>🧠🩺 Assistant Médical AI</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        body { margin: 0; min-height: 100vh; font-family: 'Poppins', sans-serif; background: radial-gradient(circle at top, #1cb5e0, #000046); color: #fff; display: flex; align-items: center; justify-content: center; }
        .card { background: rgba(255,255,255,0.08); backdrop-filter: blur(20px); border-radius: 25px; padding: 40px; width: 90%; max-width: 850px; box-shadow: 0 20px 60px rgba(0,0,0,0.4); }
        h1 { text-align: center; }
        p { text-align: center; opacity: 0.9; margin-bottom: 30px; }
        textarea { width: 100%; height: 180px; border-radius: 15px; border: none; padding: 18px; font-size: 1em; resize: none; outline: none; }
        button { margin-top: 25px; width: 100%; padding: 16px; font-size: 1.2em; font-weight: 700; border: none; border-radius: 18px; background: linear-gradient(90deg, #ffcc33, #ff9900); cursor: pointer; }
        .loading { display: none; text-align: center; margin-top: 20px; }
        footer { margin-top: 30px; text-align: center; font-size: 0.9em; opacity: 0.8; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🧠🩺 Assistant Médical AI</h1>
        <p>Analyse intelligente des cas cliniques – aide à la décision médicale</p>
        <form action="/analyze/" method="post" onsubmit="showLoading()">
            <textarea name="case_text" placeholder="Ex : Patient de 52 ans avec ictère..." required></textarea>
            <button type="submit">Analyser 🤖🩺</button>
        </form>
        <div class="loading" id="loading">⏳ قيد المعالجة...</div>
        <footer>Développé en Algérie 🇩🇿 – Assistant médical intelligent</footer>
    </div>
    <script>
        function showLoading() { document.getElementById("loading").style.display = "block"; }
    </script>
</body>
</html>
"""

# --------------------------
# صفحة النتيجة
# --------------------------
@app.post("/analyze/", response_class=HTMLResponse)
async def analyze(case_text: str = Form(...)):
    try:
        result = assistant_medical_fr(case_text)
    except Exception as e:
        result = f"Erreur: {str(e)}"

    return f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Résultat 🧠🩺</title>
    <style>
        body {{ margin: 0; min-height: 100vh; font-family: 'Poppins', sans-serif; background: radial-gradient(circle at top, #1cb5e0, #000046); color: #fff; display: flex; align-items: center; justify-content: center; }}
        .box {{ background: rgba(255,255,255,0.08); backdrop-filter: blur(20px); border-radius: 25px; padding: 40px; width: 90%; max-width: 900px; box-shadow: 0 20px 60px rgba(0,0,0,0.4); white-space: pre-wrap; }}
        a {{ display: inline-block; margin-top: 25px; color: #ffcc33; font-weight: 600; text-decoration: none; }}
    </style>
</head>
<body>
    <div class="box">
        <h1>🧠🩺 Résultat de l'analyse</h1>
        <p>{result}</p>
        <a href="/">⬅️ Nouvelle analyse</a>
    </div>
</body>
</html>
"""

# --------------------------
# تشغيل الخادم (Render compatible)
# --------------------------
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)

