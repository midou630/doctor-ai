# main.py
import os
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from openai import OpenAI

# --------------------------
# إعداد API Key
# --------------------------
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Please set your OPENAI_API_KEY in environment variables!")

client = OpenAI(api_key=OPENAI_API_KEY)

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
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Assistant médical expérimental. Ne remplace pas un avis médical professionnel."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return response.choices[0].message.content

# --------------------------
# الصفحة الرئيسية (تصميم خيالي عصري)
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
        body {
            margin: 0;
            min-height: 100vh;
            font-family: 'Poppins', sans-serif;
            background: radial-gradient(circle at top, #1cb5e0, #000046);
            color: #fff;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .card {
            background: rgba(255,255,255,0.08);
            backdrop-filter: blur(20px);
            border-radius: 25px;
            padding: 40px;
            width: 90%;
            max-width: 850px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.4);
            animation: fadeUp 1s ease;
        }
        h1 {
            text-align: center;
            font-size: 2.8em;
            margin-bottom: 10px;
        }
        p {
            text-align: center;
            opacity: 0.9;
            margin-bottom: 30px;
        }
        textarea {
            width: 100%;
            height: 180px;
            border-radius: 15px;
            border: none;
            padding: 18px;
            font-size: 1em;
            resize: none;
            outline: none;
        }
        button {
            margin-top: 25px;
            width: 100%;
            padding: 16px;
            font-size: 1.2em;
            font-weight: 700;
            border: none;
            border-radius: 18px;
            background: linear-gradient(90deg, #ffcc33, #ff9900);
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        }
        button:hover {
            transform: scale(1.03);
            box-shadow: 0 15px 35px rgba(0,0,0,0.4);
        }
        .loading {
            display: none;
            text-align: center;
            margin-top: 20px;
            font-size: 1.2em;
            animation: pulse 1.2s infinite;
        }
        footer {
            margin-top: 30px;
            text-align: center;
            font-size: 0.9em;
            opacity: 0.8;
        }
        @keyframes fadeUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes pulse {
            0% { opacity: 0.4; }
            50% { opacity: 1; }
            100% { opacity: 0.4; }
        }
    </style>
</head>
<body>
    <div class="card">
        <h1>🧠🩺 Assistant Médical AI</h1>
        <p>Analyse intelligente des cas cliniques – aide à la décision médicale</p>

        <form action="/analyze/" method="post" onsubmit="showLoading()">
            <textarea name="case_text" placeholder="Ex : Patient de 52 ans avec ictère, douleurs hépatiques..." required></textarea>
            <button type="submit">Analyser 🤖🩺</button>
        </form>

        <div class="loading" id="loading">
            ⏳ قيد المعالجة... <br> 🤖🩺
        </div>

        <footer>
            Développé en Algérie 🇩🇿 – Assistant médical intelligent
        </footer>
    </div>

    <script>
        function showLoading() {
            document.getElementById("loading").style.display = "block";
        }
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
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        body {{
            margin: 0;
            min-height: 100vh;
            font-family: 'Poppins', sans-serif;
            background: radial-gradient(circle at top, #1cb5e0, #000046);
            color: #fff;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .box {{
            background: rgba(255,255,255,0.08);
            backdrop-filter: blur(20px);
            border-radius: 25px;
            padding: 40px;
            width: 90%;
            max-width: 900px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.4);
            white-space: pre-wrap;
        }}
        a {{
            display: inline-block;
            margin-top: 25px;
            color: #ffcc33;
            font-weight: 600;
            text-decoration: none;
        }}
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
