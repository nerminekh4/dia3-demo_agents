import base64


class ImageEncoder:
    @staticmethod
    def to_data_url(image_file):
        image_base64 = base64.b64encode(image_file.getvalue()).decode("utf-8")
        return f"data:{image_file.type};base64,{image_base64}"


    @staticmethod
    def to_bytes(data_url):
        image_base64 = data_url.split(",", 1)[1]
        return base64.b64decode(image_base64)