from flask import Flask, render_template, request, send_file
import psycopg2
import io
from fpdf import FPDF

app = Flask(__name__)

# PostgreSQL connection details
conn = psycopg2.connect(
    "postgres://default:SA57KMxEhzwb@ep-holy-firefly-a1hm97ya.ap-southeast-1.aws.neon.tech:5432/verceldb?sslmode=require")
cur = conn.cursor()

# Ensure the table exists
cur.execute('''
    CREATE TABLE IF NOT EXISTS names (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL
    );
''')
conn.commit()

# Certificate template image path
certificate_template_path = 'static/certificate.png'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    name = request.form.get('name').lower()

    # Check if the name is in the database
    cur.execute("SELECT name FROM names WHERE LOWER(name) = %s", (name,))
    result = cur.fetchone()

    if result:
        # Create a PDF object
        pdf = FPDF('L', 'mm', 'A4')  # Landscape orientation, A4 size
        pdf.add_page()

        # Set the certificate template as the background
        pdf.image(certificate_template_path, x=0, y=0, w=297, h=210)  # A4 size in mm (297x210)

        # Customize text on top of the template
        pdf.set_font("Arial", 'B', 24)
        pdf.set_text_color(0, 0, 0)  # Set text color to black
        pdf.set_xy(0, 128)  # Set position (adjust based on your template)
        pdf.cell(297, 10, txt=f"{name.title()}", ln=True, align='C')

        # Save the PDF as a string in memory
        pdf_output = io.BytesIO()
        pdf_output.write(pdf.output(dest='S').encode('latin1'))
        pdf_output.seek(0)

        # Send the PDF as a downloadable file
        return send_file(pdf_output, download_name="certificate.pdf", as_attachment=True)
    else:
        return "Sorry, your name is not on the list.", 403


if __name__ == '__main__':
    app.run(debug=True)
