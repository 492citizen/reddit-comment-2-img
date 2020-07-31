from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw


def add_height_to_img(image_object, new_height, width):
    new = Image.new('RGB', (width, new_height), '#FFFFFF')
    new.paste(image_object, (0, 0))
    return new


def add_text_to_img(image_object, x_coord, y_coord, text, font_size):
    draw = ImageDraw.Draw(image_object)
    font = ImageFont.truetype("arial.ttf", font_size)
    draw.text((x_coord, y_coord), text,(0, 0, 0),font=font)
    return image_object


def wrap_text(text, font_size, width):
    _font_title = ImageFont.truetype("arial.ttf", font_size)

    lines = text.splitlines()
    for line in lines:
        line_length = _font_title.getsize(line)[0]
        if line_length > width:

            lines = ['']
            line_words = []
            words = text.split()

            for word in words:
                line_words.append(word)
                lines[-1] = ' '.join(line_words)

                line_length = _font_title.getsize(lines[-1])[0]
                if line_length > width:
                    lines[-1] = lines[-1][:-len(word)].strip()
                    lines.append(word)
                    line_words = [word]

    text = '\n'.join(lines)
    return text

def image_edit(img_path, text, out_path, font_size=50):
    img = Image.open(img_path)
    width, height = img.size

    text = wrap_text(text, font_size, width)
    new_height = height + len(text.splitlines()) * font_size + int(font_size * 0.5)

    resized_image = add_height_to_img(img, new_height, width)

    resized_image = add_text_to_img(resized_image, 10, height, text, font_size)

    resized_image.save(out_path)


if __name__ == "__main__":
    image_edit('image.webp', "In dis country, you gotta make da money first. Den when you get da money, you get da power. Den when you get da power, den you get da hard drive.", "out.png", 50)