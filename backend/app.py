from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import PyPDF2
import docx2txt
from fpdf import FPDF
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer  # You can change to LexRank, Luhn, etc.

# -------------------------
# Flask app configuration
# -------------------------
app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10 MB limit

ALLOWED_EXTENSIONS = {"pdf", "docx", "doc", "txt"}


# -------------------------
# Helper functions
# -------------------------
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text(file_path):
    ext = file_path.rsplit(".", 1)[1].lower()
    if ext == "pdf":
        text = ""
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text
    elif ext in ["docx", "doc"]:
        return docx2txt.process(file_path)
    elif ext == "txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        return ""


def summarize_text(text, sentences_count=5):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentences_count)
    return " ".join([str(sentence) for sentence in summary])


# -------------------------
# Routes
# -------------------------
@app.route("/summarize", methods=["POST"])
def summarize_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    sentences_count = int(request.form.get("sentences", 5))

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        text = extract_text(filepath)
        if not text.strip():
            return jsonify({"error": "No text found in file"}), 400
        summary = summarize_text(text, sentences_count)
        return jsonify({"summary": summary})
    else:
        return jsonify({"error": "File type not allowed"}), 400


# Optional: simple home route
@app.route("/")
def home():
    return "Smart Notes Summarizer (Offline) is running!"


# -------------------------
# Run app
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
