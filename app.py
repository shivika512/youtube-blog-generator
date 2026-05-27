from flask import send_file
from fpdf import FPDF
from flask import Flask, render_template, request
from youtube_transcript_api import YouTubeTranscriptApi
import mysql.connector
from summarizer import generate_summary

app = Flask(__name__)
latest_summary = ""

# MySQL Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Patanahi#4631",
    database="yt_blog"
)

cursor = db.cursor()

@app.route('/', methods=['GET', 'POST'])
def home():

    transcript_text = ""
    blog_summary = ""
    thumbnail_url = ""

    if request.method == 'POST':

        try:

            youtube_url = request.form['youtube_url']

            # Extract Video ID
            video_id = youtube_url.split("v=")[1]
            video_id = video_id.split("&")[0]

            print("Video ID:", video_id)

            # Thumbnail URL
            thumbnail_url = f"https://img.youtube.com/vi/{video_id}/0.jpg"

            # Fetch Transcript
            ytt_api = YouTubeTranscriptApi()

            transcript = ytt_api.fetch(video_id)

            # Convert transcript into text
            for item in transcript:
                transcript_text += item.text + " "

            # Generate Summary
            blog_summary = generate_summary(transcript_text)
            global latest_summary

            latest_summary = blog_summary

            print("\nSUMMARY:\n")
            print(blog_summary)

            # Save into MySQL
            sql = """
            INSERT INTO transcripts
            (youtube_url, transcript, summary)
            VALUES (%s, %s, %s)
            """

            values = (
                youtube_url,
                transcript_text,
                blog_summary
            )

            cursor.execute(sql, values)

            db.commit()

            print("Saved to database!")

        except Exception as e:

            transcript_text = "Error fetching transcript."
            blog_summary = ""

            print("ERROR:", e)

    return render_template(
        'index.html',
        transcript=transcript_text,
        summary=blog_summary,
        thumbnail=thumbnail_url
    )

@app.route('/download')
def download_pdf():

    pdf = FPDF()

    pdf.add_page()

    pdf.set_font("Arial", size=12)

    pdf.multi_cell(0, 10, latest_summary)

    pdf.output("blog_summary.pdf")

    return send_file(
        "blog_summary.pdf",
        as_attachment=True
    )

if __name__ == '__main__':
    app.run(debug=True)