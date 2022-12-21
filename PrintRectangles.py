import cv2
import math

def rectangles(quality, width, height, distance, start_pointX, start_pointY):
    path = r'BlackRectangle.png'
    image = cv2.imread(path)
    window_name = 'Image'
    for i in range(quality):
        start_point = (start_pointX + i * (distance + width), start_pointY)
        end_point = ((start_pointX + i * (distance + width)) + width, start_pointY + height)
        color = (255, 255, 255)
        thickness = -1
        cv2.rectangle(image, start_point, end_point, color, thickness)
    cv2.imshow(window_name, image)
    cv2.waitKey(3500)
    pass


# rectangles(5, 100, 500, 50, 290, 100)


def circleOfRectangles(width, distance, centerX, centerY, radius, angle):
    path = r'BlackRectangle.png'
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
        crop_image = rotated[centerY - radius - 10:centerY + radius + 10, centerX - radius - 10:centerX + radius + 10]
    cv2.imshow(window_name, crop_image)
    cv2.waitKey(3500)
    pass


circleOfRectangles(10, 10, 630, 350, 200, 143)
