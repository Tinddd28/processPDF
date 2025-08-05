import fitz
from PIL import Image
from io import BytesIO
from pathlib import Path


def get_pdf_files(dir: str) -> list:
    path = Path(dir)
    return [file for file in path.glob("*.pdf")]

def write_to_file(file_path, img_bytes):
    file_path.parent.mkdir(parents=True, exist_ok=True)
    image = Image.open(BytesIO(img_bytes))
    image.save(file_path, format="JPEG")

DIR_PATH = "./pdf"
SAVE_PATH = "./images"

def process():
    files = get_pdf_files(DIR_PATH)
    for file in files:
        doc = fitz.open(file)

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pixmap = page.get_pixmap(dpi=300)
            img_bytes = pixmap.tobytes()

            output_path = Path(SAVE_PATH)  / f"{file.stem}_{page_num}.jpeg"
            write_to_file(output_path, img_bytes)

            print(f"Image {file.stem}_{page_num}.png has been saved")
        
        doc.close()


def main():
    process()


if __name__ == "__main__":
    main()
# # Открываем PDF-документ
# doc = fitz.open("71.pdf")

# # Загружаем первую страницу
# page = doc.load_page(0)

# # Получаем pixmap с заданным разрешением (300 DPI)
# pixmap = page.get_pixmap(dpi=300)

# # Преобразуем pixmap в байты
# img_bytes = pixmap.tobytes()

# # Создаем объект изображения с помощью Pillow
# image = Image.open(BytesIO(img_bytes))

# # Сохраняем изображение в файл (например, в формате PNG)
# image.save('output_image.png', format='PNG')

# print("Изображение успешно сохранено как 'output_image.png'")
