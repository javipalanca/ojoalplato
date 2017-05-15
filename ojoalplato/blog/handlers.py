import math
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
from redactor.handlers import SimpleUploader, DateDirectoryUploader
from PIL import Image, ImageEnhance

from ojoalplato.blog.watermark import watermark


class WatermarkUploader(SimpleUploader):

    def get_file(self):
        # read image from InMemoryUploadedFile
        self.upload_file.file.seek(0)
        data = self.upload_file.file
        # create PIL Image instance
        image = Image.open(data)
        watermark_img = Image.open("/app/ojoalplato/static/wpfamily/img/logo2_white.png")
        rgba_image = image.convert('RGBA')
        rgba_watermark = watermark_img.convert('RGBA')

        # resize watermark image
        image_x, image_y = rgba_image.size
        watermark_x = watermark_y = max(math.floor(image_x / 10), math.floor(image_y / 10))
        new_size = (watermark_x, watermark_y)
        rgba_watermark = rgba_watermark.resize(new_size, resample=Image.ANTIALIAS)

        # apply watermark
        position = ((image_x - watermark_x - 10), (image_y - watermark_y - 10))
        rgba_image = watermark(rgba_image, rgba_watermark, position=position)

        # save new watermarked image
        cimage = BytesIO()
        rgba_image.save(cimage, format="PNG")
        cimage.seek(0)
        image_file = InMemoryUploadedFile(cimage, self.upload_file.field_name, self.upload_file.name,
                                          self.upload_file.content_type, rgba_image.tell, None)
        image_file.seek(0)
        self.upload_file = image_file
        return image_file


class DateDirectoryWatermarkUploader(WatermarkUploader, DateDirectoryUploader):
    pass
