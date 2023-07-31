import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import io
from PyPDF2 import PdfReader


class PDF_DOCX:

    def extract_text_from_file(self, file_path):
        text = ""
        if file_path.lower().endswith(('.pdf')):
            text = self.extract_text_from_pdf(file_path)
        elif file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            text = self.extract_text_from_image(file_path)
        return text

    def extract_text_from_pdf(self, pdf_path):
        with open(pdf_path, 'rb') as file:
            reader = PdfReader(file)
            text = ""

            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()

                # Check if the page contains images
                try:
                    if '/XObject' in page.Resources:
                        xObject = page.Resources['/XObject']
                        for obj in xObject:
                            if xObject[obj]['/Subtype'] == '/Image':
                                # Convert image to PIL Image
                                image_stream = io.BytesIO(xObject[obj].get_object().get_object())
                                img = Image.open(image_stream)

                                # Perform OCR on the image and append the extracted text
                                image_text = pytesseract.image_to_string(img)
                                text += image_text
                except AttributeError:
                    pass  # Skip this page if it doesn't have the expected attribute

            return text

    def extract_text_from_image(self, image_path):
        pytesseract.pytesseract.tesseract_cmd = r'C:\Users\divin\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'  # Set the path to the tesseract executable
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text

    def runner(self, file_path):
        text_content = self.extract_text_from_file(file_path)
        return text_content
