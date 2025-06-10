import fitz
from PIL import Image
from io import BytesIO

# Открываем PDF-документ
doc = fitz.open("71.pdf")

# Загружаем первую страницу
page = doc.load_page(0)

# Получаем pixmap с заданным разрешением (300 DPI)
pixmap = page.get_pixmap(dpi=300)

# Преобразуем pixmap в байты
img_bytes = pixmap.tobytes()

# Создаем объект изображения с помощью Pillow
image = Image.open(BytesIO(img_bytes))

# Сохраняем изображение в файл (например, в формате PNG)
image.save('output_image.png', format='PNG')

print("Изображение успешно сохранено как 'output_image.png'")
