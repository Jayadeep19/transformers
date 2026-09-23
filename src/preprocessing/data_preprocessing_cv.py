"""
script to read pdf, extract relevant text and skills to generate a csv and dataframe.

"""


import os
import sys
from pathlib import Path
import re
import csv

import pandas as pd
import pypdf

sections = ["PERSONAL INFO","PROFESSIONAL SUMMARY", 
            "CORE COMPETENCIES  TECHNICAL SKILLS", 
            "WORK EXPERIENCE  RESEARCH", 
            "KEY PROJECTS  PORTFOLIO", 
            "EDUCATION  CERTIFICATIONS", 
            "LANGUAGES"]

def read_pdf(path:Path):
    """
    Reads the pdf file in assets folder and returns the relevant contents of the pdf file
    """
    try:
        reader = pypdf.PdfReader(path)
        text1 = ""
        for page in reader.pages:
            text = page.extract_text()
            text1 += text
        
    except Exception as e:
        print(f"error occurred while reading the pdf file: {e}")

    return text1

def clean_raw_text(text:str) -> str:
    """
    Clean the raw cv text. (white spaces, symbols)
    """
    # normalizing white spaces or tabs
    text = re.sub(r'\s+', ' ', text)
    # broken words across lines
    text = re.sub(r'(\w+)-\s+(\w+)', r'\1-\2', text)

    text = re.sub(r'[^a-zA-Z0-9\+\#\.\,\:\;\-\s]', '', text)
    return text.strip()

def save_csv(raw_text, op_path: Path, output_csv_name: str = 'cv_csv.csv'):
    """
    To save the extracted text into csv file.
    """
    grouped_data = {sec: [] for sec in sections}

    lines = [line.strip() for line in raw_text.split('\n') if line.strip()]

    curr_section = "PERSONAL INFO"

    for line in lines:
        #clean each line before checking for the section heading
        cleaned_line = clean_raw_text(line)
        if not cleaned_line:
            continue
        
        # loop through the line and check if there is any section heading
        matched_section = None 
        for sec in sections:
            #sec_kw = [kw.split() for kw in sec.split() if len(kw)>3]
            if sec == "PERSONAL INFO":
                continue
            if (sec.lower() in cleaned_line.lower()) and len(cleaned_line)<50:
                matched_section = sec
                break
        
        if matched_section:
            curr_section = matched_section
        else:
            if curr_section in grouped_data:
                grouped_data[curr_section].append(cleaned_line)
        
    #write the populated dict into csv file.
    with open(op_path/output_csv_name, mode = 'w', newline = '', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['section', 'cleaned_content'])

        for sec_name, sec_lines in grouped_data.items():
            combined_text = ' '.join(sec_lines)
            writer.writerow([sec_name, combined_text])

    return grouped_data

if __name__ == "__main__":
    curr_dir = Path.cwd()
    pdf = Path("assets/Jayadeep_Narla.pdf")
    pdf_path = curr_dir/pdf

    csv_output_path = curr_dir/Path("csv")
    csv_output_path.mkdir(exist_ok = True)


    if not pdf_path.exists():
        print(f"CV path doesnot exists")
        sys.exit(1)
    contents = read_pdf(pdf_path)
    cleaned_string = clean_raw_text(contents)

    save_csv(contents, csv_output_path)
