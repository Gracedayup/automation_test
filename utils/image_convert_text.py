
import cv2 as cv
import ddddocr
from PIL import Image, ImageEnhance
import pytesseract
from pytesseract import image_to_string


class ImageConvertText(object):
    def image_convert_text(self, image):
        """

        :param image: 图片地址
        :return: text 图片中的文本
        """
        text = ""
        ocr = ddddocr.DdddOcr()
        with open(image, "rb") as f:
            img = f.read()
        text = ocr.classification(img)
        return text



