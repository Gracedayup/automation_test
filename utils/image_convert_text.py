
import cv2 as cv
import ddddocr
from PIL import Image, ImageEnhance
import pytesseract
from pytesseract import image_to_string


class ImageConvertText(object):
    """
    三种识别图片文字方式，image_convert_text3方法准确度最高，推荐使用
    """

    def image_convert_text(self, image):
        """

        :param image: 图片地址
        :return: text 图片中的文本
        """
        text = ""
        # 边缘保留滤波，去噪
        dst = cv.pyrMeanShiftFiltering(image, sp=10, sr=150)
        # 灰度图像
        gray = cv.cvtColor(dst, cv.COLOR_BGR2GRAY)
        # 二值化
        ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
        # 形态学操作 腐蚀，膨胀
        erode = cv.erode(binary, None, iterations=2)
        dilate = cv.dilate(erode, None, iterations=1)
        cv.imshow('dilate', dilate)
        # 逻辑运算 让背景白色 字体黑色，便于识别
        cv.bitwise_not(dilate, dilate)
        cv.imshow('binary-image', dilate)
        # 识别
        test_massage = Image.fromarray(dilate)
        text = pytesseract.image_to_string(test_massage)
        print(text)
        print('识别结果：{0}'.format(text))
        return text

    def image_convert_text2(self, image):
        """

        :param image: 图片地址
        :return: text 图片中的文本
        """
        text = ""
        im = Image.open(image)
        im = im.convert("L")
        sharpness = ImageEnhance.Contrast(im)
        sharp_img = sharpness.enhance(2.0)
        sharp_img.save(image)
        text = image_to_string(image).strip()
        return text

    def image_convert_text3(self, image):
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



