import os
import docx
import csv

def extract_text_and_style_docx(file_path, csv_writer):
    doc = docx.Document(file_path)

    for paragraph in doc.paragraphs:
        for run in paragraph.runs:
            text = run.text
            style = run.style.name
            font_size = run.style.font.size.pt if run.style.font.size else None
            font_size_str = str(font_size) if font_size is not None else "None"
            font_color = run.style.font.color.rgb

            if text.strip():
                if style not in style_list:
                    style_list.append(style)
                csv_writer.writerow([text, style, style_list.index(style), font_size_str, font_color])

folder_path = "J"
output_csv_file = "output.csv"
style_list = []

with open(output_csv_file, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Text', 'Style Name', 'Style Index', 'Font Size', 'Font Color'])

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(".docx"):
                file_path = os.path.join(root, file)
                extract_text_and_style_docx(file_path, csv_writer)