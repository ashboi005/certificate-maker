from flask import Flask, render_template, request, send_file
from fpdf import FPDF
import io

app = Flask(__name__)

allowed_names = ['ashwath soni', 'parth kapoor', 'navkirat singh', 'harnoor singh bhatia', 'tushar dhingra']

certificate_template_path = 'static/certificate.png'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    name = request.form.get('name')
    if name.lower() in allowed_names:
        # Create a PDF object
        pdf = FPDF('L', 'mm', 'A4')
        pdf.add_page()

        # Set the certificate template as the background
        pdf.image(certificate_template_path, x=0, y=0, w=297, h=210)

        # Customize text on top of the template
        pdf.set_font("Arial", 'B', 24)
        pdf.set_text_color(0, 0, 0)
        pdf.set_xy(0, 128)
        pdf.cell(297, 10, txt=f"{name}", ln=True, align='C')

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
