from flask import Flask, render_template, request, send_file
import pandas as pd
import os
from fpdf import FPDF

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

excel_path = os.path.join(UPLOAD_FOLDER, 'data.xlsx')
pdf_path = os.path.join(UPLOAD_FOLDER, 'data.pdf')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        email = request.form.get('email')

        if name and age and email:
            new_entry = pd.DataFrame([[name, age, email]], columns=['Name', 'Age', 'Email'])

            # If Excel file exists, append new data
            if os.path.exists(excel_path):
                existing_data = pd.read_excel(excel_path)
                combined_data = pd.concat([existing_data, new_entry], ignore_index=True)
            else:
                combined_data = new_entry

            # Save updated data
            combined_data.to_excel(excel_path, index=False)

            # Generate PDF from all data
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            for i, row in combined_data.iterrows():
                pdf.cell(200, 10, txt=f"{i+1}. Name: {row['Name']}, Age: {row['Age']}, Email: {row['Email']}", ln=True)
            pdf.output(pdf_path)

            return render_template('index.html', success=True)

    return render_template('index.html', success=False)

@app.route('/download')
def download_pdf():
    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
