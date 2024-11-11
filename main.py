from flask import Flask, request, render_template, redirect, jsonify
import vishlex

app = Flask(__name__)

SOURCE_LANGUAGES = {
    "AR": "Arabic",
    "BG": "Bulgarian",
    "CS": "Czech",
    "DA": "Danish",
    "DE": "German",
    "EL": "Greek",
    "EN": "English",
    "ES": "Spanish",
    "ET": "Estonian",
    "FI": "Finnish",
    "FR": "French",
    "HU": "Hungarian",
    "ID": "Indonesian",
    "IT": "Italian",
    "JA": "Japanese",
    "KO": "Korean",
    "LT": "Lithuanian",
    "LV": "Latvian",
    "NB": "Norwegian Bokmål",
    "NL": "Dutch",
    "PL": "Polish",
    "PT": "Portuguese",
    "RO": "Romanian",
    "RU": "Russian",
    "SK": "Slovak",
    "SL": "Slovenian",
    "SV": "Swedish",
    "TR": "Turkish",
    "UK": "Ukrainian",
    "ZH": "Chinese"
}

TARGET_LANGUAGES = {
    "AR": "Arabic",
    "BG": "Bulgarian",
    "CS": "Czech",
    "DA": "Danish",
    "DE": "German",
    "EL": "Greek",
    "EN-GB": "English (British)",
    "EN-US": "English (American)",
    "ES": "Spanish",
    "ET": "Estonian",
    "FI": "Finnish",
    "FR": "French",
    "HU": "Hungarian",
    "ID": "Indonesian",
    "IT": "Italian",
    "JA": "Japanese",
    "KO": "Korean",
    "LT": "Lithuanian",
    "LV": "Latvian",
    "NB": "Norwegian Bokmål",
    "NL": "Dutch",
    "PL": "Polish",
    "PT-BR": "Portuguese (Brazilian)",
    "PT-PT": "Portuguese (all Portuguese variants excluding Brazilian Portuguese)",
    "RO": "Romanian",
    "RU": "Russian",
    "SK": "Slovak",
    "SL": "Slovenian",
    "SV": "Swedish",
    "TR": "Turkish",
    "UK": "Ukrainian",
    "ZH-HANS": "Chinese (simplified)",
    "ZH-HANT": "Chinese (traditional)"
}

@app.route("/")
def home_page():
    context1 = SOURCE_LANGUAGES
    context2 = TARGET_LANGUAGES
    return render_template("home.html", result1=context1, result2=context2)

@app.route("/translate", methods=['POST', 'GET'])
def translate():
    if request.method == "POST":
        try:
            source_text = request.form.get("source_text")
            source_language = request.form.get("source_language")

            target_text = request.form.get("target_text")
            target_language = request.form.get("target_language")

            text_a = vishlex.fetch_translation(source_text, target_language)
            
            if source_language == "EN":
                source_language = "EN-US"
            
            text_b = vishlex.fetch_translation(target_text, source_language)
            
            scores = vishlex.calc_score(source_text, target_text, text_a, text_b)
            scores = jsonify(scores)
            return scores
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)