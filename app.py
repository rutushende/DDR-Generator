from flask import Flask, request, jsonify, render_template, send_file
import os
from datetime import datetime

from src.parser.pdf_parser import extract_text_from_pdf
from src.parser.image_extractor import extract_images
from src.processing.ddr_generator import generate_ddr
from src.report.pdf_builder import build_pdf

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs/reports"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/upload', methods=['POST'])
def upload():
    try:
        inspection = request.files.get('inspection')
        thermal = request.files.get('thermal')

        if not inspection or not thermal:
            return jsonify({"error": "Both files required"}), 400

        insp_path = os.path.join(UPLOAD_FOLDER, "inspection.pdf")
        therm_path = os.path.join(UPLOAD_FOLDER, "thermal.pdf")

        inspection.save(insp_path)
        thermal.save(therm_path)

        # Extract text
        insp_text = extract_text_from_pdf(insp_path)
        therm_text = extract_text_from_pdf(therm_path)

        # Extract images
        images_data = extract_images(insp_path)

        # Generate DDR
        report = generate_ddr(insp_text, therm_text, images_data)

        # Attach images
        for obs in report.get("area_wise_observations", []):
            obs["images"] = images_data.get("images", [])[:1] if images_data else ["Image Not Available"]

        # Generate PDF
        filename = f"DDR_{datetime.now().strftime('%H%M%S')}.pdf"
        filepath = os.path.join(OUTPUT_FOLDER, filename)

        build_pdf(report, filepath)

        print("✅ REPORT GENERATED")

        return jsonify({
            "success": True,
            "report": report,
            "file": filename
        })

    except Exception as e:
        print("❌ ERROR:", str(e))
        return jsonify({"error": str(e)}), 500


@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join(OUTPUT_FOLDER, filename), as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True, port=8080)