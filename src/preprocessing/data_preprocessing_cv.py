"""
script to read pdf, extract relevant text and skills to generate a csv and dataframe.

"""


import os
import sys
from pathlib import Path
import re

import pandas as pd
import pypdf

relevant_sections = ["professional summary", "core competencies & technical skills"]

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

def extract_relevant_sections(text:str) -> pd.DataFrame:
    """
    extracts the relevant sections from the text and returns dataframe and produces a csv file.
    """
    if text:
        text = text.lower()
        pattern = rf"(?:^|\n){re.escape(relevant_sections[0])}\b(.*?)(?=(?:^|\n){re.escape(relevant_sections[1])}\b)"
        match = re.search(pattern, text, re.DOTALL)

        

        if match:
            section_text = match.group(1)
            # 5. Convert it to a DataFrame
            # Splitting into individual lines for clean DataFrame rows
            lines = [line.strip() for line in section_text.split("\n") if line.strip()]
            sentance = ' '.join(lines)
            df = pd.DataFrame({relevant_sections[0]: [sentance]})
            
            print(f"--- Extracted Section: {relevant_sections[0]} ---")
            print(df.head())
        else:
            print(f"Heading '{relevant_sections[0]}' not found in the document.")
    return None

if __name__ == "__main__":
    curr_dir = Path.cwd()
    pdf = Path("assets/Jayadeep_Narla.pdf")
    pdf_path = curr_dir/pdf

    if not pdf_path.exists():
        print(f"CV path doesnot exists")
        sys.exit(1)
    contents = read_pdf(pdf_path)
    df = extract_relevant_sections(contents)