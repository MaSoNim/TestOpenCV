import cv2
import math
from PIL import Image

def some_kwargs(picture_name, folder):
    if picture_name is None and folder is None:
        result = "Rectangles.jpg"
    else:
        result = '"' + folder + '/' + picture_name + '"'
    return result

def circleOfRectangles(width, distance, centerX, centerY, radius, angle, **save_picture):
    image_width = centerX + radius
    image_height = centerY + radius
    clear_image = Image.new("RGB", (image_width, image_height), (0, 0, 0))
    filename = "Rectangles.jpg"
    clear_image.save(filename)

    path = r"Rectangles.jpg"
    image = cv2.imread(path)
    window_name = 'Image'
    quality = math.trunc((((2 * radius) + distance) / (width + distance)) + 2)
    centralRectangle = quality // 2
    for i in range(quality):
        centerOffsetX = centerX - ((centralRectangle - i) * (width + distance))
        if radius + centerX > centerOffsetX > centerX - radius:
            if centralRectangle > i:
                start_point = (math.trunc(centerOffsetX - (width / 2)), math.trunc(centerY - ((centerY + radius * math.sin(
                    math.acos(
                        ((centerOffsetX - (width / 2)) - centerX) / radius))) - centerY)))
                end_point = (math.trunc(centerOffsetX + (width / 2)), math.trunc(centerY + radius * math.sin(
                    math.acos(((centerOffsetX - (width / 2)) - centerX) / radius))))
            else:
                start_point = (math.trunc(centerOffsetX - (width / 2)), math.trunc(centerY - ((centerY + radius * math.sin(
                    math.acos(
                        ((centerOffsetX + (width / 2)) - centerX) / radius))) - centerY)))
                end_point = (math.trunc(centerOffsetX + (width / 2)), math.trunc(centerY + radius * math.sin(
                    math.acos(((centerOffsetX + (width / 2)) - centerX) / radius))))
            color = (255, 255, 255)
            thickness = -1
            cv2.rectangle(image, start_point, end_point, color, thickness)
        (h, w) = image.shape[:2]
        rotation_matrix = cv2.getRotationMatrix2D((centerX, centerY), angle, 1)
        rotated = cv2.warpAffine(image, rotation_matrix, (w, h))
        crop_image = rotated[centerY - radius:centerY + radius, centerX - radius:centerX + radius]
    cv2.imshow(window_name, crop_image)
    print(some_kwargs(**save_picture))
    cv2.imwrite(some_kwargs(**save_picture), crop_image)
    cv2.waitKey(3500)
    pass


circleOfRectangles(10, 10, 500, 500, 200, 143, picture_name="PictureTest5.jpg", folder="Pictures")
# circleOfRectangles(10, 10, 500, 500, 200, 143, picture_name=None, folder=None)
