from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from converterArquivoAPI import converter_arquivo_para_json

app = Flask(__name__)
CORS(app, origins=["https://classup-web.netlify.app", "http://localhost:5173"])


UPLOAD_FOLDER = "./uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/converterJson", methods=["POST"])
def converter():
    if "file" not in request.files:
        return jsonify({"erro": "Arquivo não encontrado"}), 400

    file = request.files["file"]
    caminho = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(caminho)

    try:
        usuarios = converter_arquivo_para_json(caminho) 
        return jsonify(usuarios), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000)
