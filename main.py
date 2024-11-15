from flask import Flask, request, render_template, jsonify
import evaluation_functions
# evaluation_functions.py contains the translation and comparision functions

app = Flask(__name__)

# Edit the API key in evaluation_functions.py

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

# Home page
@app.route("/")  # home.html
def home_page():
    context1 = SOURCE_LANGUAGES
    context2 = TARGET_LANGUAGES
    return render_template("home.html", result1=context1, result2=context2)

# Processing the translations and getting the output
@app.route("/scores", methods=['POST', 'GET']) # scores.html
def translate():
    if request.method == "POST":
        try:
            source_text = request.form.get("source_text") # A
            source_language = request.form.get("source_language")

            target_text = request.form.get("target_text") # B
            target_language = request.form.get("target_language")

            text_a = evaluation_functions.fetch_translation(source_text, target_language) # A prime
            
            if source_language == "EN":
                source_language = "EN-US"
            
            text_b = evaluation_functions.fetch_translation(target_text, source_language) # B prime

            # A v B prime
            # B v A prime
            
            scores = evaluation_functions.calc_score(source_text, target_text, text_a, text_b)

            # conditional statements to decide on the final evaluation
            if(scores["aggregate_quality_score"] > 0.75):
                result = "Good Translation"
            elif(scores["aggregate_quality_score"] > 0.50 and scores["aggregate_quality_score"] < 0.75):
                result = "Ok but can be improved"
            else:
                result = "Bad translation"
            return render_template("scores.html", scores_data=scores, final_result = result)
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)