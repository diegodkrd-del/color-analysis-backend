import re
import cv2
import numpy as np

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return '#{:02X}{:02X}{:02X}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))

def hex_to_lab(hex_str):
    rgb = np.uint8([[list(hex_to_rgb(hex_str))]])
    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB)
    return lab[0][0]

def lab_to_hex(lab):
    lab_pixel = np.uint8([[lab]])
    rgb = cv2.cvtColor(lab_pixel, cv2.COLOR_LAB2RGB)
    return rgb_to_hex(rgb[0][0])

def get_intermediate_color(hex1, hex2):
    """Calculates the exact CIELAB perceptual midpoint between hex1 and hex2."""
    lab1 = hex_to_lab(hex1).astype(float)
    lab2 = hex_to_lab(hex2).astype(float)
    mid_lab = (lab1 + lab2) / 2.0
    return lab_to_hex(mid_lab.astype(np.uint8))

print("Testing intermediate color interpolation:")
print("Midpoint between #FF4500 and #FFB300 ->", get_intermediate_color('#FF4500', '#FFB300'))
print("Midpoint between #002366 and #D50000 ->", get_intermediate_color('#002366', '#D50000'))
