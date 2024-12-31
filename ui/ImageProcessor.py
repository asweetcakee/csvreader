from PIL import Image, ImageDraw, ImageOps

class ImageProcessor:
    @staticmethod
    def make_rounded_corners(image_path, radius):
        """Adds rounded corners to the given image."""
        img = Image.open(image_path).convert("RGBA")
        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle((0, 0, img.size[0], img.size[1]), radius=radius, fill=255)
        rounded_img = ImageOps.fit(img, img.size, centering=(0.5, 0.5))
        rounded_img.putalpha(mask)
        return rounded_img
