import PyPDF2

from pdfminer.high_level import extract_pages, extract_text
from pdfminer.layout import LTTextContainer, LTChar, LTRect, LTFigure, LTComponent

import pdfplumber

from PIL import Image
from pdf2image import convert_from_path

import pytesseract

import os

from pathlib import Path

def get_pdf_files(directory: str) -> list:
    path = Path(directory)
    return [file for file in path.glob("*.pdf")]

directory_path = "./pdf"

keywords = ["Имя", "Фамилия", "Отчество", "ФИО"]


def process_element():
    files = get_pdf_files(directory_path)
    print(files)
    for file in files:
        for _, page in enumerate(extract_pages(file)):
            for element in page:
                if isinstance(element, LTTextContainer):
                    line_text = text_extraction(element)
                    print(line_text)
                if isinstance(element, LTFigure):
                    pass

                if isinstance(element, LTRect):
                    pass

def text_extraction(element: LTTextContainer):
    line_text = element.get_text()
    
    # line_formats = []
    
    for text_line in element:
       if isinstance(text_line, LTTextContainer):
           for character in text_line:
               if isinstance(character, LTChar):
                #    line_formats.append(character.size)
                    pass
                   
    # format_per_line = list(set(line_formats))
    
    return line_text

    

def main():
    process_element()

if __name__ == "__main__":
    main()