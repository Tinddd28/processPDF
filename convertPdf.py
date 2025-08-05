import PyPDF2

from pdfminer.high_level import extract_pages, extract_text
from pdfminer.layout import LTTextContainer, LTChar, LTRect, LTFigure, LTComponent

import pdfplumber

from PIL import Image
from pdf2image import convert_from_path

import pytesseract

import os
import time
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
                    # Вырезаем изображение из PDF
                    crop_image(element, pageObj)
                    # Преобразуем обрезанный pdf в изображение
                    convert_to_images('cropped_image.pdf')
                    # Извлекаем текст из изображения
                    image_text = image_to_text('PDF_image.png')
                    text_from_images.append(image_text)
                    page_content.append(image_text)
                    # Добавляем условное обозначение в списки текста и формата
                    page_text.append('image')
                    line_format.append('image')

                # Проверяем элементы на наличие таблиц
                if isinstance(element, LTRect):
                    # Если первый прямоугольный элемент
                    if first_element == True and (table_num+1) <= len(tables):
                        # Находим ограничивающий прямоугольник таблицы
                        lower_side = page.bbox[3] - tables[table_num].bbox[3]
                        upper_side = element.y1 
                        # Извлекаем информацию из таблицы
                        table = extract_table(pdf_path, pagenum, table_num)
                        # Преобразуем информацию таблицы в формат структурированной строки
                        table_string = table_converter(table)
                        # Добавляем строку таблицы в список
                        text_from_tables.append(table_string)
                        page_content.append(table_string)
                        # Устанавливаем флаг True, чтобы избежать повторения содержимого
                        table_extraction_flag = True
                        # Преобразуем в другой элемент
                        first_element = False
                        # Добавляем условное обозначение в списки текста и формата
                        page_text.append('table')
                        line_format.append('table')

                    # Проверяем, извлекли ли мы уже таблицы из этой страницы
                    if element.y0 >= lower_side and element.y1 <= upper_side:
                        pass
                    elif not isinstance(page_elements[i+1][1], LTRect):
                        table_extraction_flag = False
                        first_element = True
                        table_num+=1


            # Создаём ключ для словаря
            dctkey = 'Page_'+str(pagenum)
            # Добавляем список списков как значение ключа страницы
            text_per_page[dctkey]= [page_text, line_format, text_from_images,text_from_tables, page_content]

        # Закрываем объект файла pdf
        pdfFileObj.close()

        # Удаляем созданные дополнительные файлы
        os.remove('cropped_image.pdf')
        os.remove('PDF_image.png')

        # Удаляем содержимое страницы
        result = ''.join(text_per_page['Page_0'][4])
        result = result.replace("None", "")
        splitStr = result.split("|")
        resStr = ""
        # for s in splitStr:
        #     if s == "":
        #         continue
        #     resStr += s
        # print(resStr)
        print(result)

        time.sleep(10)


process_element()
