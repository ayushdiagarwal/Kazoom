from flask import Flask, request, jsonify
from flask_cors import CORS
from pydub import AudioSegment
from find_match import return_song
import os

app = Flask(__name__)
# CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}})

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def hello():
    return "Hello!"

@app.route("/upload", methods=["POST"])
def upload():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file found"}), 400

    audio_file = request.files["audio"]
    filepath_webm = os.path.join(UPLOAD_FOLDER, audio_file.filename)
    audio_file.save(filepath_webm)

    filepath_mp3 = filepath_webm.rsplit('.', 1)[0] + ".mp3"
    audio = AudioSegment.from_file(filepath_webm, codec="opus")

    audio.export(filepath_mp3, format="mp3")

    song_name, confidence = return_song(filepath_mp3)
    print(song_name)
    
    return jsonify({"message": "Audio received and converted to MP3", "filename": os.path.basename(filepath_mp3), "song_name": song_name, "confidence": confidence})
                   
if __name__ == "__main__":
    app.run(debug=True)