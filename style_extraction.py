import os
import docx
import csv
from tqdm import tqdm

def extract_text_and_style_docx(file_path, csv_writer, style_list):
    doc = docx.Document(file_path)

    prev_style = None
    for paragraph in doc.paragraphs:
        for run in paragraph.runs:
            text = run.text
            style = run.style.name

            if text.strip():
                if style not in style_list:
                    style_list.append(style)

                if style != prev_style:
                    csv_writer.writerow([str(text), style, style_list.index(style)])

                prev_style = style

def write_style_list_to_text(style_list, output_text_file):
    with open(output_text_file, 'w') as text_file:
        for style in style_list:
            text_file.write(style + '\n')

folder_path = "Journal - Samples"
output_csv_file = "style_data.csv"
output_text_file = "style_list.txt"
style_list = []

docx_files = [file for file in os.listdir(folder_path) if file.lower().endswith("output.docx")]
total_files = len(docx_files)

with open(output_csv_file, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Text', 'Style Name', 'Style Index'])

    for file in tqdm(docx_files, total=total_files, desc="Processing files"):
        file_path = os.path.join(folder_path, file)
        extract_text_and_style_docx(file_path, csv_writer, style_list)

write_style_list_to_text(style_list, output_text_file)
