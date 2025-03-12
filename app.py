from flask import Flask, render_template, request, send_file, redirect, url_for, flash
import yt_dlp
import os
import uuid

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure secret key

# Ensure downloads folder exists
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

def download_instagram_audio(url, download_folder=DOWNLOAD_FOLDER):
    # Create a unique filename using uuid
    unique_id = str(uuid.uuid4())
    outtmpl = os.path.join(download_folder, unique_id + '.%(ext)s')
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': outtmpl,
        # Note: No postprocessor is set up here so no FFmpeg is needed.
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        # The file is saved with its native extension (e.g., .m4a or .webm)
        filename = ydl.prepare_filename(info_dict)
    return filename

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        if not url:
            flash("Please provide a valid URL.", "error")
            return redirect(url_for('index'))
        try:
            audio_file = download_instagram_audio(url)
            return send_file(audio_file, as_attachment=True)
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            return render_template("index.html", error=error_message)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
