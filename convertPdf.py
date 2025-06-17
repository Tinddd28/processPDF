import PyPDF2

from pdfminer.high_level import extract_pages, extract_text
from pdfminer.layout import LTTextContainer, LTChar, LTRect, LTFigure, LTComponent

import pdfplumber

from PIL import Image
from pdf2image import convert_from_path

import pytesseract

import os

from pathlib import Path


def write_to_file(file_path: str, data: str):
    with open(file_path, "w", encoding="utf-8") as file:  # Открываем файл в режиме записи ('w')
        file.write(data)  # Записываем все данные сразу


def get_pdf_files(directory: str) -> list:
    path = Path(directory)
    return [file for file in path.glob("*.pdf")]

directory_path = "./pdf"
output_directory = "./txt"
keywords = ["Имя", "Фамилия", "Отчество", "ФИО"]

os.makedirs(output_directory, exist_ok=True)

def process_element():
    files = get_pdf_files(directory_path)

    print(files)
    for file in files:
        all_lines = []  # Список для хранения всех строк для текущего файла

        for page_num, page in enumerate(extract_pages(file)):
            for element in page:
                if isinstance(element, LTTextContainer):
                    line_text = text_extraction(element)
                    # Добавляем найденные данные в список
                    all_lines.append(line_text)
                if isinstance(element, LTFigure):
                    pass

                if isinstance(element, LTRect):
                    pass

        # Генерируем путь к текстовому файлу
        txt_file_name = file.stem + ".txt"  # Имя файла без расширения + ".txt"
        txt_file_path = Path(output_directory) / txt_file_name  # Полный путь к файлу

        # Объединяем все строки через '\n' и записываем в файл
        concatenated_data = "\n".join(all_lines)
        write_to_file(txt_file_path, concatenated_data)

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