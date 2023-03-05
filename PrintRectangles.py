import cv2
import math
import numpy as np
import os
import svgutils
from svglib.svglib import svg2rlg
from PIL import Image
from reportlab.graphics import renderPM
import svgwrite

# сreating a return path
def return_path(input_kwargs):
    picture_name = input_kwargs['picture_name']
    folder = input_kwargs['folder']
    if folder is None:
        folder = os.path.abspath(os.getcwd())
    if picture_name is None:
        picture_name = "example.svg"
    result_path = os.path.join(folder, picture_name)
    return result_path


# creating a pattern in jpg format
def circleOfRectangles(width, distance, radius, angle, size_w, size_h, **kwargs):
    r"""
    Args:
        width: rectangle width (the parameter is set in millimeters)
        distance: distance between rectangles (the parameter is set in millimeters)
        radius: the radius of the circle to fit the rectangles into
        angle: the angle of rotation of the pattern
        size_w: image width (the parameter is set in millimeters)
        size_h: image height (the parameter is set in millimeters)
        **kwargs: link to save the image
        image_wigth, image_height: parameters describing the image size
        centerX, centerY: parameters describing the center of the image
        image: canvas for drawing
        quality: the number of rectangles that can be drawn on the image
        centralRectangle: defines the central rectangle
        centerOffsetX: the center of the central rectangle
        start_point, end_point: the starting and ending points of the rectangle
        color, thickness: rectangle border color and thickness
        rotation_matrix, rotated: variables for image rotation
        result_path: link to save the image
    """

    # set image parameters and its center
    image_width = size_w
    image_height = size_h
    centerX = size_w // 2
    centerY = size_h // 2

    # creating a canvas
    image = np.zeros((image_width, image_height, 3), np.uint8)

    # calculation of pattern elements
    quality = math.trunc((((2 * radius) + distance) / (width + distance)) + 2)
    centralRectangle = quality // 2
    for i in range(quality):
        centerOffsetX = centerX - ((centralRectangle - i) * (width + distance))
        if radius + centerX > centerOffsetX > centerX - radius:
            if centralRectangle > i:
                start_point = (
                math.trunc(centerOffsetX - (width / 2)), math.trunc(centerY - ((centerY + radius * math.sin(
                    math.acos(
                        ((centerOffsetX - (width / 2)) - centerX) / radius))) - centerY)))
                end_point = (math.trunc(centerOffsetX + (width / 2)), math.trunc(centerY + radius * math.sin(
                    math.acos(((centerOffsetX - (width / 2)) - centerX) / radius))))
            else:
                start_point = (
                math.trunc(centerOffsetX - (width / 2)), math.trunc(centerY - ((centerY + radius * math.sin(
                    math.acos(
                        ((centerOffsetX + (width / 2)) - centerX) / radius))) - centerY)))
                end_point = (math.trunc(centerOffsetX + (width / 2)), math.trunc(centerY + radius * math.sin(
                    math.acos(((centerOffsetX + (width / 2)) - centerX) / radius))))
            color = (255, 255, 255)
            thickness = -1
            # draw a rectangle
            cv2.rectangle(image, start_point, end_point, color, thickness)
        # image rotation
        rotation_matrix = cv2.getRotationMatrix2D((centerX, centerY), angle, 1)
        rotated = cv2.warpAffine(image, rotation_matrix, (image_width, image_height))
    # saving an image
    result_path = return_path(kwargs)
    cv2.imwrite(result_path, rotated)
    return image

# starting the function
# circleOfRectangles(100, 100, 1000, 0, 2048, 2048, picture_name='PictureTest5.jpg', folder='Pictures')
# circleOfRectangles(10, 10, 200, 143, 400, 400, picture_name=None, folder=None)


# creating a pattern in svg and png format
def vectorCircleOfRectangles(width, distance, radius, angle, size_w, size_h, **kwargs):
    r"""
    Args:
        width: rectangle width (the parameter is set in millimeters)
        distance: distance between rectangles (the parameter is set in millimeters)
        radius: the radius of the circle to fit the rectangles into
        angle: the angle of rotation of the pattern
        size_w: image width (the parameter is set in millimeters)
        size_h: image height (the parameter is set in millimeters)
        **kwargs: link to save the image
        img: canvas for drawing
        centerX, centerY: parameters describing the center of the image
        quality: the number of rectangles that can be drawn on the image
        centralRectangle: defines the central rectangle
        centerOffsetX: the center of the central rectangle
        start_pointX, start_pointY, end_pointY: the starting and ending points of the rectangle
        originalSVG: reading an svg image to rotate it
        figure: making svg shapes
    """

    # creating a canvas
    img = svgwrite.Drawing('example.svg', size=(f'{size_w}mm', f'{size_h}mm'),
                           viewBox=f'{size_w / 2 * -1} {size_h / 2 * -1} {size_w} {size_h}')

    # calculation of pattern elements
    centerX = 0
    centerY = 0
    quality = math.trunc((((2 * radius) + distance) / (width + distance)) + 2)
    centralRectangle = quality // 2
    for i in range(quality):
        centerOffsetX = centerX - ((centralRectangle - i) * (width + distance))
        if radius + centerX > centerOffsetX > centerX - radius:
            if centralRectangle > i:
                start_pointX = math.trunc(centerOffsetX - (width / 2))
                start_pointY = math.trunc(centerY - ((centerY + radius * math.sin(
                    math.acos(((centerOffsetX - (width / 2)) - centerX) / radius))) - centerY))
                end_pointY = math.trunc(
                    centerY + radius * math.sin(math.acos(((centerOffsetX - (width / 2)) - centerX) / radius)))
            else:
                start_pointX = math.trunc(centerOffsetX - (width / 2))
                start_pointY = math.trunc(centerY - ((centerY + radius * math.sin(
                    math.acos(((centerOffsetX + (width / 2)) - centerX) / radius))) - centerY))
                end_pointY = math.trunc(
                    centerY + radius * math.sin(math.acos(((centerOffsetX + (width / 2)) - centerX) / radius)))
            # draw a rectangle
            img.add(img.rect(insert=(start_pointX, start_pointY), size=(width, (end_pointY - start_pointY)),
                                 fill=svgwrite.rgb(255, 255, 255)))
    # saving an image
    img.save()
    # image rotation
    originalSVG = svgutils.compose.SVG('example.svg')
    originalSVG.rotate(angle)
    figure = svgutils.transform.fromstring(
        (svgutils.compose.Figure(f'{size_w}mm', f'{size_h}mm', originalSVG)).tostr().decode('utf-8').replace(
            'viewBox="0 0', f'viewBox="{size_w / 2 * -1} {size_h / 2 * -1}'))
    # saving an image
    figure.save(return_path(kwargs))
    # saving an image in png format
    renderPM.drawToFile(svg2rlg(return_path(kwargs)), return_path(kwargs)[:-3] + 'png', fmt='PNG', bg=0)


# starting the function
vectorCircleOfRectangles(100, 100, 1000, 143, 2048, 2048, picture_name='Test1.svg', folder='SVGandPNG')
# vectorCircleOfRectangles(100, 100, 1000, 143, 2048, 2048, picture_name=None, folder=None)
