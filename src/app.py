import os
from file_hash import file_hash
from flask import Flask, request, jsonify, abort, send_file
from auth import auth
from file_path import get_file_path
from config import STORAGE_DIR

from werkzeug.wrappers import Response

app = Flask(__name__)


@app.route('/upload', methods=['POST'])
@auth.login_required
def upload_file() -> tuple[Response, int]:
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    f_hash = file_hash(file)

    subdir = f_hash[:2]
    file_dir = os.path.join(STORAGE_DIR, subdir)
    file_path = os.path.join(file_dir, f_hash)

    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    file.save(file_path)
    return jsonify({"hash": f_hash}), 200


@app.route('/download/<string:file_hash>', methods=['GET'])
@auth.login_required
def download_file(file_hash: str) -> Response:
    file_path = get_file_path(file_hash)

    if not file_path or not os.path.exists(file_path):
        abort(404, description="File not found")

    subdir = file_hash[:2]
    return send_file(os.path.join(STORAGE_DIR, subdir, file_hash), as_attachment=True)


@app.route('/delete/<string:file_hash>', methods=['DELETE'])
@auth.login_required
def delete_file(file_hash: str) -> tuple[Response, int]:
    file_path = get_file_path(file_hash)

    if not file_path or not os.path.exists(file_path):
        abort(404, description="File not found")
    try:
        os.remove(file_path)
        subdir = file_hash[:2]
        subdir_path = os.path.join(STORAGE_DIR, subdir)
        if os.path.exists(subdir_path) and not os.listdir(subdir_path):
            os.rmdir(subdir_path)
        return jsonify({"message": "File deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
