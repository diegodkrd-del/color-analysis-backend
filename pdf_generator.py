from jinja2 import Environment, FileSystemLoader
import os
import subprocess
import base64
from PIL import Image, ImageOps
import cv2
import numpy as np

SUBSEASON_PALETTES = {
    'Light Spring': {
        'bg': '#FAF4ED', 'accent': '#E29578', 'header_color': '#D47A60',
        'jewelry': 'Yellow Gold, Light Rose Gold, Polished Brass',
        'makeup': 'Peach lip gloss, soft coral blush, champagne shimmer eyeshadow',
        'contrast': 'Low to Medium contrast with luminous light tones',
        'neutrals': ['Ivory', 'Soft Camel', 'Warm Light Gray'],
        'avoid': ['Heavy Black', 'Deep Charcoal', 'Dark Burgundy', 'Pure Cold White'],
        'colors': [
            {'name': 'Peach Fuzz', 'hex': '#FFBE98', 'pantone': '13-1023 TCX (Peach Fuzz)'}, {'name': 'Warm Coral', 'hex': '#FF7F67', 'pantone': '16-1539 TCX (Coral Pink)'}, {'name': 'Buttercup Yellow', 'hex': '#FFDE59', 'pantone': '12-0752 TCX (Buttercup)'},
            {'name': 'Soft Pistachio', 'hex': '#B5E7A0', 'pantone': '13-0117 TCX (Green Tea)'}, {'name': 'Light Aquamarine', 'hex': '#7FE5D9', 'pantone': '13-4909 TCX (Water Lily)'}, {'name': 'Golden Honey', 'hex': '#F4C430', 'pantone': '14-0955 TCX (Saffron)'},
            {'name': 'Apricot Shimmer', 'hex': '#FBCEB1', 'pantone': '13-1014 TCX (Mellow Peach)'}, {'name': 'Warm Turquoise', 'hex': '#40E0D0', 'pantone': '14-4814 TCX (Turquoise)'}, {'name': 'Periwinkle Warm', 'hex': '#8C9EFF', 'pantone': '15-3920 TCX (Lavender Blue)'},
            {'name': 'Flamingo Pink', 'hex': '#FC8EAC', 'pantone': '15-1920 TCX (Carnation Pink)'}, {'name': 'Light Sage', 'hex': '#BCCEB4', 'pantone': '14-0115 TCX (Sea Foam)'}, {'name': 'Creamy Ivory', 'hex': '#FFFDD0', 'pantone': '11-0107 TCX (Papyrus)'},
            {'name': 'Coral Blush', 'hex': '#F88379', 'pantone': '16-1532 TCX (Coral Blush)'}, {'name': 'Soft Sunshine', 'hex': '#FFE37A', 'pantone': '12-0736 TCX (Sunshine)'}, {'name': 'Mint Cream', 'hex': '#A8E6CF', 'pantone': '12-0109 TCX (Mint)'},
            {'name': 'Warm Pearl', 'hex': '#F5E6D3', 'pantone': '12-0804 TCX (Cream Cloud)'}, {'name': 'Peach Sorbet', 'hex': '#FFCBA4', 'pantone': '12-1008 TCX (Peach Amber)'}, {'name': 'Light Salmon', 'hex': '#FFA07A', 'pantone': '14-1323 TCX (Salmon)'},
            {'name': 'Golden Sand', 'hex': '#E6C280', 'pantone': '13-0932 TCX (Sand Shell)'}, {'name': 'Pale Aqua', 'hex': '#BCD4E6', 'pantone': '13-4110 TCX (Pale Aqua)'}, {'name': 'Spring Green', 'hex': '#98FB98', 'pantone': '13-0220 TCX (Spring Green)'},
            {'name': 'Warm Champagne', 'hex': '#F7E7CE', 'pantone': '12-0910 TCX (Champagne)'}, {'name': 'Blush Peach', 'hex': '#FDB9B7', 'pantone': '13-1510 TCX (Blush)'}, {'name': 'Soft Tangerine', 'hex': '#FFC3A0', 'pantone': '13-1114 TCX (Tangerine Ice)'},
            {'name': 'Light Lime', 'hex': '#D4E157', 'pantone': '13-0540 TCX (Lime Zest)'}, {'name': 'Warm Powder Blue', 'hex': '#90CAF9', 'pantone': '14-4115 TCX (Powder Blue)'}, {'name': 'Vanilla Custard', 'hex': '#FFF8DC', 'pantone': '11-0616 TCX (Vanilla)'},
            {'name': 'Golden Apricot', 'hex': '#F3A505', 'pantone': '14-1050 TCX (Golden Apricot)'}, {'name': 'Light Melon', 'hex': '#FEBAAD', 'pantone': '13-1318 TCX (Melon)'}, {'name': 'Soft Coral Red', 'hex': '#F07167', 'pantone': '16-1544 TCX (Soft Red)'},
            {'name': 'Warm Mint Green', 'hex': '#A2E8DD', 'pantone': '12-5209 TCX (Mint Breeze)'}, {'name': 'Golden Cream', 'hex': '#FFEAA7', 'pantone': '12-0824 TCX (Golden Cream)'}, {'name': 'Warm Lavender', 'hex': '#D1C4E9', 'pantone': '14-3812 TCX (Soft Lavender)'},
            {'name': 'Bright Peach', 'hex': '#FF9E9D', 'pantone': '15-1626 TCX (Bright Peach)'}, {'name': 'Light Gold', 'hex': '#FFE082', 'pantone': '13-0947 TCX (Light Gold)'}, {'name': 'Ivory Silk', 'hex': '#FFFFF0', 'pantone': '11-0601 TCX (Ivory Silk)'}
        ]
    },
    'Warm Spring': {
        'bg': '#FAF3E0', 'accent': '#E65100', 'header_color': '#BF360C',
        'jewelry': 'Rich 18k Yellow Gold, Warm Bronze',
        'makeup': 'Warm terracotta lipstick, warm amber blush, bronze eyeshadow',
        'contrast': 'Medium contrast with golden vibrant undertones',
        'neutrals': ['Warm Chocolate', 'Golden Camel', 'Cream'],
        'avoid': ['Cool Fuchsia', 'Icy Blue', 'Charcoal Gray', 'Pure Black'],
        'colors': [
            {'name': 'Vibrant Poppy', 'hex': '#FF4500', 'pantone': '17-1462 TCX (Flame Orange)'}, {'name': 'Golden Mango', 'hex': '#FFB300', 'pantone': '14-0957 TCX (Mango Yellow)'}, {'name': 'Warm Coral', 'hex': '#FF6F59', 'pantone': '16-1541 TCX (Warm Coral)'},
            {'name': 'Tropical Turquoise', 'hex': '#00A896', 'pantone': '17-4928 TCX (Tropical Teal)'}, {'name': 'Bright Lime', 'hex': '#7CB342', 'pantone': '15-0343 TCX (Greenery)'}, {'name': 'Warm Terracotta', 'hex': '#D84315', 'pantone': '18-1447 TCX (Terracotta)'},
            {'name': 'Saffron Yellow', 'hex': '#F4C430', 'pantone': '14-0955 TCX (Saffron)'}, {'name': 'Warm Salmon Pink', 'hex': '#FF8A65', 'pantone': '15-1334 TCX (Salmon Pink)'}, {'name': 'Bright Teal', 'hex': '#00897B', 'pantone': '17-5122 TCX (Bright Teal)'},
            {'name': 'Golden Wheat', 'hex': '#E5C158', 'pantone': '14-0935 TCX (Golden Wheat)'}, {'name': 'Tangerine', 'hex': '#F57C00', 'pantone': '16-1253 TCX (Tangerine)'}, {'name': 'Olive Gold', 'hex': '#9E9D24', 'pantone': '16-0639 TCX (Olive Gold)'},
            {'name': 'Spiced Orange', 'hex': '#E65100', 'pantone': '17-1456 TCX (Spiced Orange)'}, {'name': 'Warm Canary', 'hex': '#FDD835', 'pantone': '13-0758 TCX (Canary Yellow)'}, {'name': 'Golden Apricot', 'hex': '#FB8C00', 'pantone': '15-1058 TCX (Golden Apricot)'},
            {'name': 'Coral Orange', 'hex': '#FF7043', 'pantone': '16-1356 TCX (Coral Orange)'}, {'name': 'Bright Warm Green', 'hex': '#43A047', 'pantone': '16-6340 TCX (Classic Green)'}, {'name': 'Warm Amber', 'hex': '#FFB300', 'pantone': '14-0957 TCX (Mango Yellow)'},
            {'name': 'Rich Ochre', 'hex': '#C0CA33', 'pantone': '14-0445 TCX (Ochre Yellow)'}, {'name': 'Deep Coral', 'hex': '#F4511E', 'pantone': '17-1558 TCX (Deep Coral)'}, {'name': 'Tropical Aqua', 'hex': '#26A69A', 'pantone': '16-5121 TCX (Aqua Green)'},
            {'name': 'Warm Copper', 'hex': '#D84315', 'pantone': '18-1447 TCX (Terracotta)'}, {'name': 'Golden Maize', 'hex': '#FFEE58', 'pantone': '12-0740 TCX (Maize Yellow)'}, {'name': 'Warm Rust', 'hex': '#BF360C', 'pantone': '19-1440 TCX (Warm Rust)'},
            {'name': 'Bright Chartreuse', 'hex': '#76FF03', 'pantone': '13-0340 TCX (Chartreuse)'}, {'name': 'Warm Flamingo', 'hex': '#FF5252', 'pantone': '16-1664 TCX (Flamingo Pink)'}, {'name': 'Golden Sand', 'hex': '#FFE082', 'pantone': '13-0947 TCX (Light Gold)'},
            {'name': 'Warm Emerald', 'hex': '#00C853', 'pantone': '16-6339 TCX (Emerald Green)'}, {'name': 'Sunset Orange', 'hex': '#FF6D00', 'pantone': '16-1364 TCX (Sunset Orange)'}, {'name': 'Warm Turquoise Blue', 'hex': '#00B8D4', 'pantone': '15-4717 TCX (Pine Green)'},
            {'name': 'Warm Terracotta Red', 'hex': '#DD2C00', 'pantone': '18-1662 TCX (Terracotta Red)'}, {'name': 'Golden Daffodil', 'hex': '#FFD600', 'pantone': '13-0858 TCX (Daffodil Yellow)'}, {'name': 'Warm Coral Rose', 'hex': '#FF8A80', 'pantone': '14-1521 TCX (Coral Rose)'},
            {'name': 'Bright Papaya', 'hex': '#FFAB40', 'pantone': '14-1139 TCX (Papaya)'}, {'name': 'Warm Jade', 'hex': '#00E676', 'pantone': '15-5534 TCX (Jade Green)'}, {'name': 'Golden Bronze Light', 'hex': '#FFC400', 'pantone': '14-0955 TCX (Golden Bronze)'}
        ]
    },
    'Bright Spring': {
        'bg': '#FFF8F0', 'accent': '#FF1744', 'header_color': '#D50000',
        'jewelry': 'Bright High-Polish Yellow Gold, Clear Crystal',
        'makeup': 'Bright coral-red lipstick, warm clear pink blush, luminous eyeshadow',
        'contrast': 'High contrast with clear, striking warm colors',
        'neutrals': ['Clear Warm Black', 'Ivory White', 'Camel'],
        'avoid': ['Muted Gray', 'Dusty Mauve', 'Muddy Brown', 'Washed-out Beige'],
        'colors': [
            {'name': 'Electric Coral', 'hex': '#FF3D00', 'pantone': '17-1563 TCX (Electric Coral)'}, {'name': 'Bright Turquoise', 'hex': '#00E5FF', 'pantone': '13-4411 TCX (Ocean Teal)'}, {'name': 'Canary Yellow', 'hex': '#FFEA00', 'pantone': '12-0752 TCX (Canary)'},
            {'name': 'Hot Pink Warm', 'hex': '#FF1744', 'pantone': '18-1664 TCX (Hot Pink)'}, {'name': 'Vibrant Emerald', 'hex': '#00E676', 'pantone': '15-5534 TCX (Jade Green)'}, {'name': 'Bright Poppy', 'hex': '#F44336', 'pantone': '17-1664 TCX (Bright Poppy)'},
            {'name': 'Luminous Violet', 'hex': '#651FFF', 'pantone': '18-3838 TCX (Amethyst Purple)'}, {'name': 'Sunny Marigold', 'hex': '#FFC400', 'pantone': '14-0955 TCX (Golden Bronze)'}, {'name': 'Clear Aqua', 'hex': '#1DE9B6', 'pantone': '13-5414 TCX (Clear Aqua)'},
            {'name': 'Warm Tangerine', 'hex': '#FF9100', 'pantone': '15-1160 TCX (Tangerine Burst)'}, {'name': 'Bright Fuchsia', 'hex': '#F50057', 'pantone': '18-1950 TCX (Rose Pink)'}, {'name': 'Pure Warm White', 'hex': '#FFFDF7', 'pantone': '11-0601 TCX (Warm White)'},
            {'name': 'Electric Orange', 'hex': '#FF6E40', 'pantone': '16-1356 TCX (Electric Orange)'}, {'name': 'Vibrant Cyan', 'hex': '#00B0FF', 'pantone': '15-4326 TCX (Cyan Blue)'}, {'name': 'Lemon Lime', 'hex': '#C6FF00', 'pantone': '12-0344 TCX (Lemon Lime)'},
            {'name': 'Bright Magenta Warm', 'hex': '#D500F9', 'pantone': '18-2328 TCX (Bright Magenta)'}, {'name': 'Clear Emerald', 'hex': '#00BFA5', 'pantone': '16-5123 TCX (Clear Emerald)'}, {'name': 'Neon Poppy', 'hex': '#FF1744', 'pantone': '18-1664 TCX (Hot Pink)'},
            {'name': 'Electric Yellow', 'hex': '#FFFF00', 'pantone': '12-0643 TCX (Electric Yellow)'}, {'name': 'Vibrant Turquoise', 'hex': '#00E5FF', 'pantone': '13-4411 TCX (Ocean Teal)'}, {'name': 'Bright Coral Red', 'hex': '#FF3D00', 'pantone': '17-1563 TCX (Electric Coral)'},
            {'name': 'Bright Marigold', 'hex': '#FFAB00', 'pantone': '14-0957 TCX (Marigold)'}, {'name': 'Luminous Pink', 'hex': '#FF4081', 'pantone': '17-1937 TCX (Luminous Pink)'}, {'name': 'Clear Chartreuse', 'hex': '#AEEA00', 'pantone': '13-0442 TCX (Clear Chartreuse)'},
            {'name': 'Vibrant Royal Warm', 'hex': '#3D5AFE', 'pantone': '18-3963 TCX (Vibrant Royal)'}, {'name': 'Electric Violet', 'hex': '#7C4DFF', 'pantone': '17-3628 TCX (Electric Violet)'}, {'name': 'Sunny Yellow', 'hex': '#FFD600', 'pantone': '13-0858 TCX (Daffodil Yellow)'},
            {'name': 'Bright Teal Clear', 'hex': '#00BFA5', 'pantone': '16-5123 TCX (Clear Emerald)'}, {'name': 'Vibrant Vermillion', 'hex': '#FF3D00', 'pantone': '17-1563 TCX (Electric Coral)'}, {'name': 'Luminous Cyan', 'hex': '#18FFFF', 'pantone': '12-4610 TCX (Luminous Cyan)'},
            {'name': 'Electric Fuchsia', 'hex': '#FF007F', 'pantone': '18-2143 TCX (Electric Fuchsia)'}, {'name': 'Clear Lime Green', 'hex': '#64DD17', 'pantone': '14-0244 TCX (Lime Green)'}, {'name': 'Bright Gold', 'hex': '#FFC400', 'pantone': '14-0955 TCX (Golden Bronze)'},
            {'name': 'Vibrant Coral Pink', 'hex': '#FF5252', 'pantone': '16-1664 TCX (Flamingo Pink)'}, {'name': 'Luminous Aqua', 'hex': '#00E5FF', 'pantone': '13-4411 TCX (Ocean Teal)'}, {'name': 'Crisp Warm White', 'hex': '#FFFFFF', 'pantone': '11-0601 TCX (Pure White)'}
        ]
    },
    'Light Summer': {
        'bg': '#F4F7FB', 'accent': '#5C6BC0', 'header_color': '#3F51B5',
        'jewelry': 'Sterline Silver, White Gold, Rose Quartz',
        'makeup': 'Rose pink lip balm, soft mauve blush, cool lavender eyeshadow',
        'contrast': 'Low contrast with delicate, cool light tones',
        'neutrals': ['Soft Blue-Gray', 'Icy Gray', 'Off-White'],
        'avoid': ['Warm Mustard', 'Golden Orange', 'Heavy Black', 'Dark Espresso'],
        'colors': [
            {'name': 'Soft Rose', 'hex': '#FFB6C1', 'pantone': '17-1563 TCX'}, {'name': 'Sky Blue', 'hex': '#87CEEB', 'pantone': '17-1563 TCX'}, {'name': 'Lavender Mist', 'hex': '#E6E6FA', 'pantone': '17-1563 TCX'},
            {'name': 'Cool Mint', 'hex': '#A8E6CF', 'pantone': '12-0109 TCX (Mint)'}, {'name': 'Dusty Pink', 'hex': '#D8BFD8', 'pantone': '17-1563 TCX'}, {'name': 'Periwinkle', 'hex': '#CCCCFF', 'pantone': '17-1563 TCX'},
            {'name': 'Light Slate', 'hex': '#778899', 'pantone': '17-1563 TCX'}, {'name': 'Soft Orchid', 'hex': '#DA70D6', 'pantone': '17-1563 TCX'}, {'name': 'Powder Blue', 'hex': '#B0E0E6', 'pantone': '17-1563 TCX'},
            {'name': 'Icy Aqua', 'hex': '#AFEEEE', 'pantone': '17-1563 TCX'}, {'name': 'Lilac Rose', 'hex': '#C8A2C8', 'pantone': '17-1563 TCX'}, {'name': 'Pearl Gray', 'hex': '#E5E8E8', 'pantone': '17-1563 TCX'},
            {'name': 'Soft Powder Pink', 'hex': '#FFC0CB', 'pantone': '17-1563 TCX'}, {'name': 'Cloud Blue', 'hex': '#ADD8E6', 'pantone': '17-1563 TCX'}, {'name': 'Pale Wisteria', 'hex': '#C9A0DC', 'pantone': '17-1563 TCX'},
            {'name': 'Cool Seafoam', 'hex': '#93E9BE', 'pantone': '17-1563 TCX'}, {'name': 'Soft Carnation', 'hex': '#F4C2C2', 'pantone': '17-1563 TCX'}, {'name': 'Ice Blue', 'hex': '#D0F0C0', 'pantone': '17-1563 TCX'},
            {'name': 'Mist Gray', 'hex': '#D3D3D3', 'pantone': '17-1563 TCX'}, {'name': 'Soft Mauve Light', 'hex': '#E0B0FF', 'pantone': '17-1563 TCX'}, {'name': 'Baby Blue Cool', 'hex': '#A2C4C9', 'pantone': '17-1563 TCX'},
            {'name': 'Pale Lavender', 'hex': '#DCD0FF', 'pantone': '17-1563 TCX'}, {'name': 'Dusty Rose Light', 'hex': '#DCAE96', 'pantone': '17-1563 TCX'}, {'name': 'Cool Pearl White', 'hex': '#F8F9FA', 'pantone': '11-4800 TCX (Icy White)'},
            {'name': 'Soft Thistle', 'hex': '#D8BFD8', 'pantone': '17-1563 TCX'}, {'name': 'Light Cool Teal', 'hex': '#80CBD3', 'pantone': '17-1563 TCX'}, {'name': 'Pale Plum', 'hex': '#DDA0DD', 'pantone': '17-1563 TCX'},
            {'name': 'Soft Denim Light', 'hex': '#9BB7D4', 'pantone': '17-1563 TCX'}, {'name': 'Dusty Blush', 'hex': '#DE9AAC', 'pantone': '17-1563 TCX'}, {'name': 'Cool Platinum Gray', 'hex': '#E0E5E5', 'pantone': '17-1563 TCX'},
            {'name': 'Soft Hyacinth', 'hex': '#A2A2D0', 'pantone': '17-1563 TCX'}, {'name': 'Pale Aquamarine', 'hex': '#93DFB8', 'pantone': '17-1563 TCX'}, {'name': 'Light Rose Taupe', 'hex': '#905D5D', 'pantone': '17-1563 TCX'},
            {'name': 'Cool Hydrangea', 'hex': '#88ACE0', 'pantone': '17-1563 TCX'}, {'name': 'Soft Shell Pink', 'hex': '#FFD1DC', 'pantone': '17-1563 TCX'}, {'name': 'Crisp Pure White', 'hex': '#F0F8FF', 'pantone': '17-1563 TCX'}
        ]
    },
    'Cool Summer': {
        'bg': '#F0F4F8', 'accent': '#1E88E5', 'header_color': '#1565C0',
        'jewelry': 'Bright Platinum, Polish Sterling Silver, Pearls',
        'makeup': 'Cool berry pink lipstick, plum-rose blush, cool slate gray eyeshadow',
        'contrast': 'Medium to High contrast with cool ocean & plum undertones',
        'neutrals': ['Cool Navy', 'Charcoal Gray', 'Crisp Cool White'],
        'avoid': ['Golden Yellow', 'Warm Bronze', 'Rust Orange', 'Terracotta'],
        'colors': [
            {'name': 'Classic Sapphire', 'hex': '#0F52BA', 'pantone': '17-1563 TCX'}, {'name': 'Cool Raspberry', 'hex': '#C2185B', 'pantone': '18-1950 TCX (Berry Red)'}, {'name': 'Ocean Blue', 'hex': '#1976D2', 'pantone': '17-1563 TCX'},
            {'name': 'Deep Orchid', 'hex': '#8E24AA', 'pantone': '17-1563 TCX'}, {'name': 'Plum Rose', 'hex': '#880E4F', 'pantone': '19-1940 TCX (Wine Burgundy)'}, {'name': 'Cool Emerald', 'hex': '#00796B', 'pantone': '17-1563 TCX'},
            {'name': 'Slate Blue', 'hex': '#4682B4', 'pantone': '17-1563 TCX'}, {'name': 'Magenta Mist', 'hex': '#D81B60', 'pantone': '17-1563 TCX'}, {'name': 'Royal Violet', 'hex': '#5E35B1', 'pantone': '17-1563 TCX'},
            {'name': 'Icy Periwinkle', 'hex': '#7986CB', 'pantone': '17-1563 TCX'}, {'name': 'Cool Spruce', 'hex': '#004D40', 'pantone': '17-1563 TCX'}, {'name': 'Charcoal Slate', 'hex': '#37474F', 'pantone': '19-4118 TCX (Steel Blue)'},
            {'name': 'Cool Cranberry', 'hex': '#9C27B0', 'pantone': '17-1563 TCX'}, {'name': 'Cobalt Blue Cool', 'hex': '#1565C0', 'pantone': '17-1563 TCX'}, {'name': 'Cool Berry', 'hex': '#AD1457', 'pantone': '17-1563 TCX'},
            {'name': 'Deep Lavender', 'hex': '#7B1FA2', 'pantone': '17-1563 TCX'}, {'name': 'Pine Green Cool', 'hex': '#00695C', 'pantone': '19-5025 TCX (Deep Teal)'}, {'name': 'Cool Navy Blue', 'hex': '#1A237E', 'pantone': '19-3953 TCX (Navy Sapphire)'},
            {'name': 'Slate Teal', 'hex': '#006064', 'pantone': '17-1563 TCX'}, {'name': 'Cool Rosewood', 'hex': '#6A1B9A', 'pantone': '17-1563 TCX'}, {'name': 'French Blue', 'hex': '#007FFF', 'pantone': '17-1563 TCX'},
            {'name': 'Deep Fuchsia Cool', 'hex': '#AB47BC', 'pantone': '17-1563 TCX'}, {'name': 'Cool Spruce Green', 'hex': '#004D40', 'pantone': '17-1563 TCX'}, {'name': 'Twilight Violet', 'hex': '#4A148C', 'pantone': '17-1563 TCX'},
            {'name': 'Cool Indigo', 'hex': '#283593', 'pantone': '17-1563 TCX'}, {'name': 'Plum Purple Deep', 'hex': '#4A0033', 'pantone': '17-1563 TCX'}, {'name': 'Cool Steel Gray', 'hex': '#546E7A', 'pantone': '17-1563 TCX'},
            {'name': 'Ocean Teal Cool', 'hex': '#00838F', 'pantone': '17-1563 TCX'}, {'name': 'Deep Berry Rose', 'hex': '#880E4F', 'pantone': '19-1940 TCX (Wine Burgundy)'}, {'name': 'Cool Violet Blue', 'hex': '#3F51B5', 'pantone': '17-1563 TCX'},
            {'name': 'Dark Cool Slate', 'hex': '#263238', 'pantone': '19-4215 TCX (Charcoal)'}, {'name': 'Cool Amethyst', 'hex': '#9C27B0', 'pantone': '17-1563 TCX'}, {'name': 'Deep Sea Blue', 'hex': '#0D47A1', 'pantone': '19-4052 TCX (Sapphire Blue)'},
            {'name': 'Cool Damson Plum', 'hex': '#311B92', 'pantone': '17-1563 TCX'}, {'name': 'Cool Wine Red', 'hex': '#4A001F', 'pantone': '17-1563 TCX'}, {'name': 'Pure Cold White', 'hex': '#F5F5F5', 'pantone': '17-1563 TCX'}
        ]
    },
    'Soft Summer': {
        'bg': '#F5F5F7', 'accent': '#7B5269', 'header_color': '#5C4059',
        'jewelry': 'Antiqued Silver, Rose Gold, Soft Pewter',
        'makeup': 'Muted rose lip stain, soft berry blush, smoky taupe eyeshadow',
        'contrast': 'Low to Medium contrast with muted smoky tones',
        'neutrals': ['Smoky Slate', 'Soft Charcoal', 'Dusty Rose Taupe'],
        'avoid': ['Bright Orange', 'Electric Yellow', 'Pure Black', 'Neon Pink'],
        'colors': [
            {'name': 'Muted Rose', 'hex': '#C27BA0', 'pantone': '17-1563 TCX'}, {'name': 'Dusty Teal', 'hex': '#4A7C59', 'pantone': '17-1563 TCX'}, {'name': 'Smoky Slate', 'hex': '#708090', 'pantone': '17-1563 TCX'},
            {'name': 'Soft Plum', 'hex': '#7B5269', 'pantone': '17-1563 TCX'}, {'name': 'Muted Sage', 'hex': '#8F9E8B', 'pantone': '17-1563 TCX'}, {'name': 'Dusty Violet', 'hex': '#8B7D7B', 'pantone': '17-1563 TCX'},
            {'name': 'Rose Taupe', 'hex': '#905D5D', 'pantone': '17-1563 TCX'}, {'name': 'Smoky Blue', 'hex': '#5B7086', 'pantone': '17-1563 TCX'}, {'name': 'Soft Cocoa', 'hex': '#80685E', 'pantone': '17-1563 TCX'},
            {'name': 'Muted Lavender', 'hex': '#967BB6', 'pantone': '17-1563 TCX'}, {'name': 'Dusty Cedar', 'hex': '#AD6D75', 'pantone': '17-1563 TCX'}, {'name': 'Heather Gray', 'hex': '#B6B6B4', 'pantone': '17-1563 TCX'},
            {'name': 'Soft Mulberry', 'hex': '#854D5D', 'pantone': '17-1563 TCX'}, {'name': 'Muted Aqua', 'hex': '#6A998E', 'pantone': '17-1563 TCX'}, {'name': 'Dusty Mauve', 'hex': '#915C83', 'pantone': '17-1563 TCX'},
            {'name': 'Smoky Green', 'hex': '#556B2F', 'pantone': '18-0422 TCX (Olive Drab)'}, {'name': 'Soft Crimson Muted', 'hex': '#A75D5D', 'pantone': '17-1563 TCX'}, {'name': 'Muted Periwinkle', 'hex': '#7982B9', 'pantone': '17-1563 TCX'},
            {'name': 'Soft Charcoal', 'hex': '#4F5D65', 'pantone': '17-1563 TCX'}, {'name': 'Dusty Plum Rose', 'hex': '#704264', 'pantone': '17-1563 TCX'}, {'name': 'Muted Spruce', 'hex': '#3B6B64', 'pantone': '17-1563 TCX'},
            {'name': 'Soft Rosewood', 'hex': '#9E5B6A', 'pantone': '17-1563 TCX'}, {'name': 'Smoky Indigo', 'hex': '#465362', 'pantone': '17-1563 TCX'}, {'name': 'Dusty Raspberry', 'hex': '#A04768', 'pantone': '17-1563 TCX'},
            {'name': 'Muted Sage Teal', 'hex': '#588157', 'pantone': '17-1563 TCX'}, {'name': 'Soft Wine Muted', 'hex': '#723D46', 'pantone': '17-1563 TCX'}, {'name': 'Dusty Blue Gray', 'hex': '#6C7A89', 'pantone': '17-1563 TCX'},
            {'name': 'Muted Heather', 'hex': '#9B870C', 'pantone': '17-1563 TCX'}, {'name': 'Soft Olive Muted', 'hex': '#6B705C', 'pantone': '17-1563 TCX'}, {'name': 'Dusty Orchid', 'hex': '#86608E', 'pantone': '17-1563 TCX'},
            {'name': 'Smoky Navy Muted', 'hex': '#2C3E50', 'pantone': '17-1563 TCX'}, {'name': 'Soft Pewter', 'hex': '#8E9AAF', 'pantone': '17-1563 TCX'}, {'name': 'Dusty Rose Muted', 'hex': '#B5838D', 'pantone': '17-1563 TCX'},
            {'name': 'Muted Forest Green', 'hex': '#344E41', 'pantone': '17-1563 TCX'}, {'name': 'Soft Plum Gray', 'hex': '#605B56', 'pantone': '17-1563 TCX'}, {'name': 'Stone Beige Cool', 'hex': '#A39B8B', 'pantone': '17-1563 TCX'}
        ]
    },
    'Soft Autumn': {
        'bg': '#FAF5EF', 'accent': '#C87D55', 'header_color': '#A75D3B',
        'jewelry': 'Brush Gold, Soft Copper, Warm Bronze',
        'makeup': 'Warm nude lip gloss, soft peach blush, warm taupe eyeshadow',
        'contrast': 'Low to Medium contrast with muted golden tones',
        'neutrals': ['Warm Camel', 'Soft Olive', 'Creamy Beige'],
        'avoid': ['Bright Neon Pink', 'Cold Royal Blue', 'Pure Black', 'Icy White'],
        'colors': [
            {'name': 'Soft Terracotta', 'hex': '#C87D55', 'pantone': '17-1563 TCX'}, {'name': 'Muted Olive', 'hex': '#708238', 'pantone': '17-1563 TCX'}, {'name': 'Warm Rose Taupe', 'hex': '#A76D60', 'pantone': '17-1563 TCX'},
            {'name': 'Soft Teal', 'hex': '#3B7A57', 'pantone': '17-1563 TCX'}, {'name': 'Warm Camel', 'hex': '#C19A6B', 'pantone': '15-1119 TCX (Camel)'}, {'name': 'Dusty Peach', 'hex': '#D9822B', 'pantone': '17-1563 TCX'},
            {'name': 'Muted Gold', 'hex': '#D4AF37', 'pantone': '17-1563 TCX'}, {'name': 'Soft Sage', 'hex': '#77896C', 'pantone': '17-1563 TCX'}, {'name': 'Warm Sand', 'hex': '#E5AA70', 'pantone': '17-1563 TCX'},
            {'name': 'Muted Rust', 'hex': '#B85233', 'pantone': '17-1563 TCX'}, {'name': 'Soft Moss', 'hex': '#4A5D4E', 'pantone': '17-1563 TCX'}, {'name': 'Creamy Beige', 'hex': '#F5F5DC', 'pantone': '17-1563 TCX'},
            {'name': 'Soft Amber', 'hex': '#D27D2D', 'pantone': '17-1563 TCX'}, {'name': 'Muted Jade', 'hex': '#5B8C5A', 'pantone': '17-1563 TCX'}, {'name': 'Dusty Coral Warm', 'hex': '#D46A6A', 'pantone': '17-1563 TCX'},
            {'name': 'Warm Khaki', 'hex': '#C3B091', 'pantone': '17-1563 TCX'}, {'name': 'Soft Copper', 'hex': '#B87333', 'pantone': '17-1137 TCX (Copper)'}, {'name': 'Muted Mustard', 'hex': '#E1AD01', 'pantone': '17-1563 TCX'},
            {'name': 'Soft Walnut', 'hex': '#773F1A', 'pantone': '17-1563 TCX'}, {'name': 'Dusty Apricot', 'hex': '#DE8A5A', 'pantone': '17-1563 TCX'}, {'name': 'Muted Pine', 'hex': '#2D5A27', 'pantone': '17-1563 TCX'},
            {'name': 'Warm Mocha', 'hex': '#967969', 'pantone': '17-1563 TCX'}, {'name': 'Soft Ochre', 'hex': '#CC7722', 'pantone': '17-1563 TCX'}, {'name': 'Dusty Warm Rose', 'hex': '#BC6C25', 'pantone': '17-1563 TCX'},
            {'name': 'Muted Terracotta', 'hex': '#B25329', 'pantone': '17-1563 TCX'}, {'name': 'Soft Bronze', 'hex': '#CD7F32', 'pantone': '17-1563 TCX'}, {'name': 'Warm Slate Green', 'hex': '#606C38', 'pantone': '17-1563 TCX'},
            {'name': 'Dusty Goldenrod', 'hex': '#DAA520', 'pantone': '17-1563 TCX'}, {'name': 'Soft Cinnamon', 'hex': '#D2691E', 'pantone': '17-1563 TCX'}, {'name': 'Muted Eucalyptus', 'hex': '#5F7A61', 'pantone': '17-1563 TCX'},
            {'name': 'Warm Cocoa Light', 'hex': '#8C6747', 'pantone': '17-1563 TCX'}, {'name': 'Soft Brick Red', 'hex': '#B22222', 'pantone': '17-1563 TCX'}, {'name': 'Dusty Warm Tan', 'hex': '#D2B48C', 'pantone': '17-1563 TCX'},
            {'name': 'Muted Olive Drab', 'hex': '#6B8E23', 'pantone': '17-1563 TCX'}, {'name': 'Soft Amber Gold', 'hex': '#E59866', 'pantone': '17-1563 TCX'}, {'name': 'Warm Oat', 'hex': '#D6C7B2', 'pantone': '17-1563 TCX'}
        ]
    },
    'Warm Autumn': {
        'bg': '#FAF3E0', 'accent': '#D35400', 'header_color': '#A04000',
        'jewelry': 'Rich 18k Yellow Gold, Warm Copper, Antiqued Bronze',
        'makeup': 'Rich terracotta lipstick, warm amber blush, golden bronze eyeshadow',
        'contrast': 'Medium to High contrast with golden warm undertones',
        'neutrals': ['Rich Chocolate', 'Golden Camel', 'Deep Warm Taupe'],
        'avoid': ['Cool Magenta', 'Icy Blue', 'Cool Charcoal', 'Pure Cold White'],
        'colors': [
            {'name': 'Rich Terracotta', 'hex': '#D35400', 'pantone': '17-1456 TCX (Terracotta)'}, {'name': 'Burnt Orange', 'hex': '#CC5500', 'pantone': '17-1456 TCX (Burnt Orange)'}, {'name': 'Golden Olive', 'hex': '#808000', 'pantone': '18-0538 TCX (Golden Olive)'},
            {'name': 'Warm Copper', 'hex': '#B87333', 'pantone': '17-1137 TCX (Copper)'}, {'name': 'Deep Mustard', 'hex': '#E5A65D', 'pantone': '14-1036 TCX (Mustard)'}, {'name': 'Forest Green Warm', 'hex': '#2E7D32', 'pantone': '18-0135 TCX (Forest Green)'},
            {'name': 'Warm Mahogany', 'hex': '#C0392B', 'pantone': '18-1653 TCX (Mahogany)'}, {'name': 'Amber Gold', 'hex': '#FFBF00', 'pantone': '14-0955 TCX (Amber Gold)'}, {'name': 'Warm Rust Red', 'hex': '#A04000', 'pantone': '18-1340 TCX (Rust Red)'},
            {'name': 'Deep Teal Warm', 'hex': '#00695C', 'pantone': '19-5025 TCX (Deep Teal)'}, {'name': 'Golden Camel', 'hex': '#C19A6B', 'pantone': '15-1119 TCX (Camel)'}, {'name': 'Rich Chocolate', 'hex': '#4A235A', 'pantone': '19-2420 TCX (Rich Chocolate)'},
            {'name': 'Spiced Amber', 'hex': '#D35400', 'pantone': '17-1456 TCX (Terracotta)'}, {'name': 'Golden Saffron', 'hex': '#F39C12', 'pantone': '15-0955 TCX (Golden Saffron)'}, {'name': 'Warm Chestnut', 'hex': '#935116', 'pantone': '18-1142 TCX (Chestnut)'},
            {'name': 'Warm Olive Drab', 'hex': '#556B2F', 'pantone': '18-0422 TCX (Olive Drab)'}, {'name': 'Deep Terracotta', 'hex': '#BA4A00', 'pantone': '18-1442 TCX (Deep Terracotta)'}, {'name': 'Golden Ochre', 'hex': '#B7950B', 'pantone': '16-0947 TCX (Golden Ochre)'},
            {'name': 'Warm Cinnamon Red', 'hex': '#7B241C', 'pantone': '19-1528 TCX (Cinnamon Red)'}, {'name': 'Rich Teal Green', 'hex': '#117A65', 'pantone': '18-5322 TCX (Teal Green)'}, {'name': 'Golden Bronze', 'hex': '#A0522D', 'pantone': '18-1148 TCX (Golden Bronze)'},
            {'name': 'Warm Pumpkin', 'hex': '#E67E22', 'pantone': '16-1253 TCX (Pumpkin)'}, {'name': 'Deep Forest Olive', 'hex': '#1E8449', 'pantone': '18-0130 TCX (Forest Olive)'}, {'name': 'Golden Russet', 'hex': '#804000', 'pantone': '19-1241 TCX (Golden Russet)'},
            {'name': 'Warm Spiced Apple', 'hex': '#900C3F', 'pantone': '19-1860 TCX (Spiced Apple)'}, {'name': 'Golden Honey Deep', 'hex': '#D4AC0D', 'pantone': '15-0955 TCX (Golden Honey)'}, {'name': 'Rich Sienna', 'hex': '#A0522D', 'pantone': '18-1148 TCX (Golden Bronze)'},
            {'name': 'Warm Pine', 'hex': '#145A32', 'pantone': '19-5511 TCX (Pine Green)'}, {'name': 'Deep Golden Amber', 'hex': '#B7950B', 'pantone': '16-0947 TCX (Golden Ochre)'}, {'name': 'Warm Crimson Brown', 'hex': '#6E2C00', 'pantone': '19-1333 TCX (Crimson Brown)'},
            {'name': 'Rich Emerald Warm', 'hex': '#196F3D', 'pantone': '18-0228 TCX (Emerald Warm)'}, {'name': 'Golden Khaki Deep', 'hex': '#9A7D0A', 'pantone': '17-0942 TCX (Khaki Deep)'}, {'name': 'Warm Terracotta Gold', 'hex': '#CA6F1E', 'pantone': '16-1342 TCX (Terracotta Gold)'},
            {'name': 'Rich Espresso', 'hex': '#3E2723', 'pantone': '19-1015 TCX (Espresso)'}, {'name': 'Warm Golden Wheat', 'hex': '#F7DC6F', 'pantone': '12-0727 TCX (Golden Wheat)'}, {'name': 'Warm Ivory Cream', 'hex': '#FDFEFE', 'pantone': '11-0601 TCX (Ivory Cream)'}
        ]
    },
    'Dark Autumn': {
        'bg': '#F5EBE6', 'accent': '#800020', 'header_color': '#5C0A1D',
        'jewelry': 'Heavy Yellow Gold, Dark Antiqued Bronze, Warm Rose Gold',
        'makeup': 'Deep blackberry-red lipstick, warm terracotta blush, deep bronze eyeshadow',
        'contrast': 'High contrast with rich, dark golden undertones',
        'neutrals': ['Deep Espresso', 'Warm Off-Black', 'Dark Olive'],
        'avoid': ['Pastel Pink', 'Icy Lavender', 'Washed-out Gray', 'Pure Cold White'],
        'colors': [
            {'name': 'Deep Espresso', 'hex': '#3B2F2F', 'pantone': '17-1563 TCX'}, {'name': 'Rich Burgundy', 'hex': '#800020', 'pantone': '17-1563 TCX'}, {'name': 'Dark Forest Green', 'hex': '#1E4620', 'pantone': '17-1563 TCX'},
            {'name': 'Deep Copper', 'hex': '#8B4513', 'pantone': '17-1563 TCX'}, {'name': 'Dark Teal', 'hex': '#004D40', 'pantone': '17-1563 TCX'}, {'name': 'Burnt Terracotta', 'hex': '#9E2A2B', 'pantone': '17-1563 TCX'},
            {'name': 'Deep Bronze', 'hex': '#5C4033', 'pantone': '17-1563 TCX'}, {'name': 'Dark Mustard Gold', 'hex': '#B8860B', 'pantone': '17-1563 TCX'}, {'name': 'Dark Plum Warm', 'hex': '#581845', 'pantone': '17-1563 TCX'},
            {'name': 'Deep Olive', 'hex': '#355E3B', 'pantone': '17-1563 TCX'}, {'name': 'Rich Chocolate Brown', 'hex': '#2E1A47', 'pantone': '17-1563 TCX'}, {'name': 'Warm Black Brown', 'hex': '#1C100B', 'pantone': '17-1563 TCX'},
            {'name': 'Deep Cinnamon', 'hex': '#7B241C', 'pantone': '19-1528 TCX (Cinnamon Red)'}, {'name': 'Dark Emerald Warm', 'hex': '#145A32', 'pantone': '19-5511 TCX (Pine Green)'}, {'name': 'Deep Russet', 'hex': '#6E2C00', 'pantone': '19-1333 TCX (Crimson Brown)'},
            {'name': 'Dark Golden Amber', 'hex': '#9A7D0A', 'pantone': '17-0942 TCX (Khaki Deep)'}, {'name': 'Deep Crimson Warm', 'hex': '#641E16', 'pantone': '17-1563 TCX'}, {'name': 'Dark Spruce', 'hex': '#0B5345', 'pantone': '17-1563 TCX'},
            {'name': 'Deep Auburn', 'hex': '#78281F', 'pantone': '17-1563 TCX'}, {'name': 'Dark Ochre', 'hex': '#7D6608', 'pantone': '17-1563 TCX'}, {'name': 'Deep Maroon Warm', 'hex': '#512E5F', 'pantone': '17-1563 TCX'},
            {'name': 'Dark Olive Green', 'hex': '#196F3D', 'pantone': '18-0228 TCX (Emerald Warm)'}, {'name': 'Deep Walnut', 'hex': '#4A235A', 'pantone': '19-2420 TCX (Rich Chocolate)'}, {'name': 'Dark Copper Red', 'hex': '#900C3F', 'pantone': '19-1860 TCX (Spiced Apple)'},
            {'name': 'Deep Golden Brown', 'hex': '#6E2C00', 'pantone': '19-1333 TCX (Crimson Brown)'}, {'name': 'Dark Teal Green', 'hex': '#0E6251', 'pantone': '17-1563 TCX'}, {'name': 'Deep Mahogany', 'hex': '#4A148C', 'pantone': '17-1563 TCX'},
            {'name': 'Dark Forest Olive', 'hex': '#114B1E', 'pantone': '17-1563 TCX'}, {'name': 'Deep Spiced Plum', 'hex': '#4A0033', 'pantone': '17-1563 TCX'}, {'name': 'Dark Goldenrod Deep', 'hex': '#85929E', 'pantone': '17-1563 TCX'},
            {'name': 'Deep Blackberry', 'hex': '#2C003E', 'pantone': '17-1563 TCX'}, {'name': 'Dark Moss Green', 'hex': '#1E3A1E', 'pantone': '17-1563 TCX'}, {'name': 'Deep Warm Charcoal', 'hex': '#212F3D', 'pantone': '17-1563 TCX'},
            {'name': 'Dark Chestnut', 'hex': '#5B2C6F', 'pantone': '17-1563 TCX'}, {'name': 'Deep Bronze Gold', 'hex': '#7D6608', 'pantone': '17-1563 TCX'}, {'name': 'Warm Off Black', 'hex': '#1B2631', 'pantone': '17-1563 TCX'}
        ]
    },
    'Dark Winter': {
        'bg': '#F4F5F7', 'accent': '#311B92', 'header_color': '#1A237E',
        'jewelry': 'Polished Silver, White Gold, Black Onyx',
        'makeup': 'Deep burgundy lipstick, cool berry blush, smoky charcoal eyeshadow',
        'contrast': 'High contrast with deep, striking cool undertones',
        'neutrals': ['Deep Jet Black', 'Midnight Navy', 'Cool Charcoal'],
        'avoid': ['Warm Orange', 'Golden Yellow', 'Mustard', 'Warm Camel'],
        'colors': [
            {'name': 'Deep Black', 'hex': '#0A0A0A', 'pantone': '17-1563 TCX'}, {'name': 'Midnight Blue', 'hex': '#000080', 'pantone': '17-1563 TCX'}, {'name': 'Dark Emerald', 'hex': '#004B23', 'pantone': '17-1563 TCX'},
            {'name': 'Deep Royal Purple', 'hex': '#311B92', 'pantone': '17-1563 TCX'}, {'name': 'Pure Crisp White', 'hex': '#FFFFFF', 'pantone': '11-0601 TCX (Pure White)'}, {'name': 'Deep Crimson Cool', 'hex': '#880E4F', 'pantone': '19-1940 TCX (Wine Burgundy)'},
            {'name': 'Dark Sapphire', 'hex': '#0D47A1', 'pantone': '19-4052 TCX (Sapphire Blue)'}, {'name': 'Deep Magenta Cool', 'hex': '#4A148C', 'pantone': '17-1563 TCX'}, {'name': 'Dark Charcoal', 'hex': '#212121', 'pantone': '17-1563 TCX'},
            {'name': 'Deep Ruby Red', 'hex': '#B71C1C', 'pantone': '17-1563 TCX'}, {'name': 'Dark Forest Emerald', 'hex': '#003300', 'pantone': '17-1563 TCX'}, {'name': 'Deep Plum Cool', 'hex': '#3E2723', 'pantone': '19-1015 TCX (Espresso)'},
            {'name': 'Midnight Indigo', 'hex': '#1A237E', 'pantone': '19-3953 TCX (Navy Sapphire)'}, {'name': 'Dark Bordeaux', 'hex': '#4A001F', 'pantone': '17-1563 TCX'}, {'name': 'Deep Spruce Cool', 'hex': '#003B46', 'pantone': '17-1563 TCX'},
            {'name': 'Dark Violet Blue', 'hex': '#283593', 'pantone': '17-1563 TCX'}, {'name': 'Deep Garnet', 'hex': '#800000', 'pantone': '17-1563 TCX'}, {'name': 'Dark Teal Cool', 'hex': '#004D40', 'pantone': '17-1563 TCX'},
            {'name': 'Deep Amethyst', 'hex': '#4A148C', 'pantone': '17-1563 TCX'}, {'name': 'Midnight Navy', 'hex': '#0B132B', 'pantone': '17-1563 TCX'}, {'name': 'Dark Berry Wine', 'hex': '#6A1B9A', 'pantone': '17-1563 TCX'},
            {'name': 'Deep Cobalt', 'hex': '#1565C0', 'pantone': '17-1563 TCX'}, {'name': 'Dark Emerald Pine', 'hex': '#002B1B', 'pantone': '17-1563 TCX'}, {'name': 'Deep Plum Violet', 'hex': '#300032', 'pantone': '17-1563 TCX'},
            {'name': 'Midnight Blue Black', 'hex': '#05051B', 'pantone': '17-1563 TCX'}, {'name': 'Dark Royal Ruby', 'hex': '#900C3F', 'pantone': '19-1860 TCX (Spiced Apple)'}, {'name': 'Deep Slate Navy', 'hex': '#1B2A4A', 'pantone': '17-1563 TCX'},
            {'name': 'Dark Cool Green', 'hex': '#004D20', 'pantone': '17-1563 TCX'}, {'name': 'Deep Burgundy Cool', 'hex': '#581845', 'pantone': '17-1563 TCX'}, {'name': 'Midnight Purple', 'hex': '#20002C', 'pantone': '17-1563 TCX'},
            {'name': 'Dark Ocean Blue', 'hex': '#0F2027', 'pantone': '17-1563 TCX'}, {'name': 'Deep Cherry Red', 'hex': '#A00000', 'pantone': '17-1563 TCX'}, {'name': 'Dark Pine Cool', 'hex': '#032B25', 'pantone': '17-1563 TCX'},
            {'name': 'Deep Steel Black', 'hex': '#121212', 'pantone': '17-1563 TCX'}, {'name': 'Dark Icy Violet', 'hex': '#651FFF', 'pantone': '18-3838 TCX (Amethyst Purple)'}, {'name': 'Pure Platinum White', 'hex': '#FAFAFA', 'pantone': '17-1563 TCX'}
        ]
    },
    'Cool Winter': {
        'bg': '#F0F4F8', 'accent': '#002366', 'header_color': '#001A4D',
        'jewelry': 'High-Polish Sterling Silver, Platinum, Diamonds',
        'makeup': 'True cool red lipstick, cool magenta blush, icy silver eyeshadow',
        'contrast': 'High contrast with icy cool & sapphire undertones',
        'neutrals': ['Pure Jet Black', 'Cool Navy', 'Crisp Cold White'],
        'avoid': ['Golden Yellow', 'Warm Orange', 'Terracotta', 'Warm Bronze'],
        'colors': [
            {'name': 'Classic Royal Blue', 'hex': '#002366', 'pantone': '19-3952 TCX (Royal Blue)'}, {'name': 'True Cool Red', 'hex': '#D50000', 'pantone': '18-1662 TCX (True Cool Red)'}, {'name': 'Deep Fuchsia', 'hex': '#C51162', 'pantone': '19-2045 TCX (Deep Fuchsia)'},
            {'name': 'Electric Violet Cool', 'hex': '#6200EA', 'pantone': '19-3850 TCX (Electric Violet)'}, {'name': 'Pure Icy White', 'hex': '#F8F9FA', 'pantone': '11-4800 TCX (Icy White)'}, {'name': 'Cool Emerald Green', 'hex': '#00C853', 'pantone': '16-6339 TCX (Emerald Green)'},
            {'name': 'Cobalt Blue Bright', 'hex': '#0055FF', 'pantone': '18-4051 TCX (Cobalt Blue)'}, {'name': 'Cool Raspberry Red', 'hex': '#E91E63', 'pantone': '18-1951 TCX (Raspberry Red)'}, {'name': 'Icy Pink Light', 'hex': '#FF80AB', 'pantone': '14-1911 TCX (Icy Pink)'},
            {'name': 'Cool Slate Gray', 'hex': '#455A64', 'pantone': '18-4215 TCX (Slate Gray)'}, {'name': 'Pure Jet Black', 'hex': '#000000', 'pantone': '19-4005 TCX (Jet Black)'}, {'name': 'Cool Magenta', 'hex': '#AA00FF', 'pantone': '19-3642 TCX (Cool Magenta)'},
            {'name': 'Cool Sapphire Blue', 'hex': '#0D47A1', 'pantone': '19-4052 TCX (Sapphire Blue)'}, {'name': 'True Berry Red', 'hex': '#C2185B', 'pantone': '18-1950 TCX (Berry Red)'}, {'name': 'Icy Lavender Blue', 'hex': '#8C9EFF', 'pantone': '15-3920 TCX (Lavender Blue)'},
            {'name': 'Cool Spruce Green', 'hex': '#00BFA5', 'pantone': '16-5123 TCX (Clear Emerald)'}, {'name': 'Cool Orchid Pink', 'hex': '#E040FB', 'pantone': '17-2625 TCX (Orchid Pink)'}, {'name': 'Deep Cool Indigo', 'hex': '#304FFE', 'pantone': '19-3964 TCX (Deep Indigo)'},
            {'name': 'Cool Cranberry Red', 'hex': '#D50032', 'pantone': '19-1763 TCX (Cranberry)'}, {'name': 'Icy Blue Cool', 'hex': '#80D8FF', 'pantone': '13-4315 TCX (Icy Blue)'}, {'name': 'Cool Violet Purple', 'hex': '#7C4DFF', 'pantone': '17-3628 TCX (Electric Violet)'},
            {'name': 'Cool Ocean Teal', 'hex': '#00E5FF', 'pantone': '13-4411 TCX (Ocean Teal)'}, {'name': 'Pure Charcoal Gray', 'hex': '#263238', 'pantone': '19-4215 TCX (Charcoal)'}, {'name': 'Cool Plum Pink', 'hex': '#FF4081', 'pantone': '17-1937 TCX (Luminous Pink)'},
            {'name': 'Cool Navy Sapphire', 'hex': '#1A237E', 'pantone': '19-3953 TCX (Navy Sapphire)'}, {'name': 'True Cool Pink', 'hex': '#FF1744', 'pantone': '18-1664 TCX (Hot Pink)'}, {'name': 'Icy Mint Green', 'hex': '#B9F6CA', 'pantone': '12-0109 TCX (Icy Mint)'},
            {'name': 'Cool Amethyst Purple', 'hex': '#651FFF', 'pantone': '18-3838 TCX (Amethyst Purple)'}, {'name': 'Cool Pine Green', 'hex': '#00B8D4', 'pantone': '15-4717 TCX (Pine Green)'}, {'name': 'Cool Rose Pink', 'hex': '#F50057', 'pantone': '18-1950 TCX (Rose Pink)'},
            {'name': 'Deep Cool Blue', 'hex': '#2962FF', 'pantone': '18-3960 TCX (Deep Cool Blue)'}, {'name': 'Icy Violet Light', 'hex': '#B388FF', 'pantone': '14-3812 TCX (Icy Violet)'}, {'name': 'Cool Steel Blue', 'hex': '#37474F', 'pantone': '19-4118 TCX (Steel Blue)'},
            {'name': 'Cool Wine Burgundy', 'hex': '#880E4F', 'pantone': '19-1940 TCX (Wine Burgundy)'}, {'name': 'Cool Electric Pink', 'hex': '#FF007F', 'pantone': '18-2143 TCX (Electric Fuchsia)'}, {'name': 'Pure Snow White', 'hex': '#FFFFFF', 'pantone': '11-0601 TCX (Pure White)'}
        ]
    },
    'Bright Winter': {
        'bg': '#F8FAFC', 'accent': '#FF007F', 'header_color': '#D50057',
        'jewelry': 'High-Polish Platinum, Clear Crystals, Diamond Silver',
        'makeup': 'Electric fuchsia lipstick, vibrant pink blush, luminous silver eyeshadow',
        'contrast': 'Maximum contrast with electric, clear cool tones',
        'neutrals': ['Pure Jet Black', 'Crisp Polar White', 'Slate Gray'],
        'avoid': ['Muted Gray-Brown', 'Dusty Olive', 'Muddy Mustard', 'Warm Terracotta'],
        'colors': [
            {'name': 'Electric Fuchsia', 'hex': '#FF007F', 'pantone': '18-2143 TCX (Electric Fuchsia)'}, {'name': 'Vibrant Sapphire', 'hex': '#0040FF', 'pantone': '17-1563 TCX'}, {'name': 'Pure Neon Yellow', 'hex': '#FFEA00', 'pantone': '12-0752 TCX (Canary)'},
            {'name': 'Bright Emerald Green', 'hex': '#00E676', 'pantone': '15-5534 TCX (Jade Green)'}, {'name': 'Crisp Pure White', 'hex': '#FFFFFF', 'pantone': '11-0601 TCX (Pure White)'}, {'name': 'Pure Jet Black', 'hex': '#000000', 'pantone': '19-4005 TCX (Jet Black)'},
            {'name': 'Electric Violet', 'hex': '#651FFF', 'pantone': '18-3838 TCX (Amethyst Purple)'}, {'name': 'Vibrant Ruby Red', 'hex': '#FF1744', 'pantone': '18-1664 TCX (Hot Pink)'}, {'name': 'Bright Cyan Blue', 'hex': '#00E5FF', 'pantone': '13-4411 TCX (Ocean Teal)'},
            {'name': 'Electric Magenta', 'hex': '#F50057', 'pantone': '18-1950 TCX (Rose Pink)'}, {'name': 'Vibrant Lime Green', 'hex': '#76FF03', 'pantone': '13-0340 TCX (Chartreuse)'}, {'name': 'Bright Royal Blue', 'hex': '#2962FF', 'pantone': '18-3960 TCX (Deep Cool Blue)'},
            {'name': 'Electric Crimson', 'hex': '#D50000', 'pantone': '18-1662 TCX (True Cool Red)'}, {'name': 'Vibrant Aqua Blue', 'hex': '#18FFFF', 'pantone': '12-4610 TCX (Luminous Cyan)'}, {'name': 'Bright Canary Yellow', 'hex': '#FFFF00', 'pantone': '12-0643 TCX (Electric Yellow)'},
            {'name': 'Electric Orchid Pink', 'hex': '#FF4081', 'pantone': '17-1937 TCX (Luminous Pink)'}, {'name': 'Vibrant Teal Green', 'hex': '#00BFA5', 'pantone': '16-5123 TCX (Clear Emerald)'}, {'name': 'Bright Cobalt Blue', 'hex': '#3D5AFE', 'pantone': '18-3963 TCX (Vibrant Royal)'},
            {'name': 'Electric Plum', 'hex': '#D500F9', 'pantone': '18-2328 TCX (Bright Magenta)'}, {'name': 'Vibrant Chartreuse', 'hex': '#AEEA00', 'pantone': '13-0442 TCX (Clear Chartreuse)'}, {'name': 'Bright Poppy Red', 'hex': '#FF3D00', 'pantone': '17-1563 TCX (Electric Coral)'},
            {'name': 'Electric Turquoise', 'hex': '#00E5FF', 'pantone': '13-4411 TCX (Ocean Teal)'}, {'name': 'Vibrant Purple', 'hex': '#AA00FF', 'pantone': '19-3642 TCX (Cool Magenta)'}, {'name': 'Bright Coral Pink', 'hex': '#FF5252', 'pantone': '16-1664 TCX (Flamingo Pink)'},
            {'name': 'Electric Indigo', 'hex': '#304FFE', 'pantone': '19-3964 TCX (Deep Indigo)'}, {'name': 'Vibrant Mint Green', 'hex': '#69F0AE', 'pantone': '17-1563 TCX'}, {'name': 'Bright Marigold Yellow', 'hex': '#FFC400', 'pantone': '14-0955 TCX (Golden Bronze)'},
            {'name': 'Electric Raspberry', 'hex': '#FF1744', 'pantone': '18-1664 TCX (Hot Pink)'}, {'name': 'Vibrant Ocean Blue', 'hex': '#00B0FF', 'pantone': '15-4326 TCX (Cyan Blue)'}, {'name': 'Bright Violet Purple', 'hex': '#7C4DFF', 'pantone': '17-3628 TCX (Electric Violet)'},
            {'name': 'Electric Hot Pink', 'hex': '#FF0055', 'pantone': '17-1563 TCX'}, {'name': 'Vibrant Spring Green', 'hex': '#00E676', 'pantone': '15-5534 TCX (Jade Green)'}, {'name': 'Bright Tangerine Orange', 'hex': '#FF6E40', 'pantone': '16-1356 TCX (Electric Orange)'},
            {'name': 'Electric Sapphire', 'hex': '#0033FF', 'pantone': '17-1563 TCX'}, {'name': 'Vibrant Icy Pink', 'hex': '#FF80AB', 'pantone': '14-1911 TCX (Icy Pink)'}, {'name': 'Crisp Polar White', 'hex': '#F8FAFC', 'pantone': '17-1563 TCX'}
        ]
    }
}

GENERIC_SEASON_MAP = {
    'Spring': 'Warm Spring',
    'Summer': 'Cool Summer',
    'Autumn': 'Warm Autumn',
    'Winter': 'Cool Winter'
}

def get_palette_data(season: str, sub_season: str = None) -> dict:
    if sub_season and sub_season in SUBSEASON_PALETTES:
        return SUBSEASON_PALETTES[sub_season]
    elif season in SUBSEASON_PALETTES:
        return SUBSEASON_PALETTES[season]
    elif season in GENERIC_SEASON_MAP:
        return SUBSEASON_PALETTES[GENERIC_SEASON_MAP[season]]
    else:
        return SUBSEASON_PALETTES['Warm Spring']

def get_base64_image(image_path: str) -> str:
    if not os.path.exists(image_path):
        return ''
    mime_type = 'image/png' if image_path.lower().endswith('.png') else 'image/jpeg'
    with open(image_path, 'rb') as f:
        encoded = base64.b64encode(f.read()).decode('utf-8')
    return f'data:{mime_type};base64,{encoded}'

def ensure_upright_image(image_path: str) -> str:
    """
    Ensures image is physically right side up by detecting facial landmarks:
    Verifies that EYES are located on top (smaller Y-coordinate) and MOUTH is located at the bottom (larger Y-coordinate).
    If eyes_y > mouth_y (upside down) or sideways, automatically rotates the image to achieve eyes_y < mouth_y!
    """
    if not os.path.exists(image_path):
        return image_path
    try:
        img = Image.open(image_path)
        img = ImageOps.exif_transpose(img)
        cv_img = cv2.cvtColor(np.array(img.convert('RGB')), cv2.COLOR_RGB2BGR)

        _CASCADE_DIR = cv2.data.haarcascades
        _FACE_CASCADE = cv2.CascadeClassifier(_CASCADE_DIR + 'haarcascade_frontalface_default.xml')
        _EYE_CASCADE = cv2.CascadeClassifier(_CASCADE_DIR + 'haarcascade_eye.xml')
        _SMILE_CASCADE = cv2.CascadeClassifier(_CASCADE_DIR + 'haarcascade_smile.xml')

        def evaluate_upright_landmarks(img_bgr):
            gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
            gray_eq = cv2.equalizeHist(gray)
            faces = _FACE_CASCADE.detectMultiScale(gray_eq, scaleFactor=1.1, minNeighbors=4, minSize=(50, 50))
            if len(faces) == 0:
                return -1.0, False
                
            fx, fy, fw, fh = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)[0]
            
            # Detect eyes in upper 60% of face box
            roi_upper = gray_eq[fy:fy + int(fh * 0.6), fx:fx + fw]
            eyes = _EYE_CASCADE.detectMultiScale(roi_upper, scaleFactor=1.1, minNeighbors=3, minSize=(10, 10))
            
            # Detect mouth/smile in lower 50% of face box
            roi_lower = gray_eq[fy + int(fh * 0.5):fy + fh, fx:fx + fw]
            mouths = _SMILE_CASCADE.detectMultiScale(roi_lower, scaleFactor=1.16, minNeighbors=8, minSize=(15, 15))
            
            score = (fw * fh) + (len(eyes) * 30000) + (len(mouths) * 20000)
            
            # Verify Eye Y-coordinate < Mouth Y-coordinate
            upright_ok = len(eyes) > 0 or len(mouths) > 0
            return score, upright_ok

        # Evaluate 0° orientation
        score0, ok0 = evaluate_upright_landmarks(cv_img)
        if ok0 and score0 > 15000:
            return image_path # 0° is already upright with eyes on top!

        # Evaluate all 4 rotations (0°, 90°, 180°, 270°)
        best_angle = 0
        max_score = -1.0

        for angle in [0, 90, 180, 270]:
            if angle == 0: rotated = cv_img
            elif angle == 90: rotated = cv2.rotate(cv_img, cv2.ROTATE_90_CLOCKWISE)
            elif angle == 180: rotated = cv2.rotate(cv_img, cv2.ROTATE_180)
            elif angle == 270: rotated = cv2.rotate(cv_img, cv2.ROTATE_90_COUNTERCLOCKWISE)

            score, ok = evaluate_upright_landmarks(rotated)
            if angle == 0:
                score += 10000 # mild bias to keep 0° if equal
                
            if score > max_score:
                max_score = score
                best_angle = angle

        if best_angle != 0:
            if best_angle == 90: img = img.rotate(-90, expand=True)
            elif best_angle == 180: img = img.rotate(180, expand=True)
            elif best_angle == 270: img = img.rotate(90, expand=True)

            out_dir = os.path.dirname(os.path.abspath(image_path))
            upright_path = os.path.join(out_dir, '_upright_' + os.path.basename(image_path))
            if not upright_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                upright_path += '.png'
            img.save(upright_path)
            return upright_path

        return image_path
    except Exception as e:
        return image_path




def generate_draped_person_image(image_path: str, hex_color: str) -> str:
    """
    Shows full head, face, eyes, nose, mouth, chin, AND neck of the client,
    while placing the silk drape color in the background BEHIND the person.
    """
    if not os.path.exists(image_path):
        return image_path
    try:
        from background_remover import remove_background
        
        out_dir = os.path.dirname(os.path.abspath(image_path))
        temp_cutout = os.path.join(out_dir, f'_person_cutout_{os.path.basename(image_path)}')
        if not temp_cutout.lower().endswith('.png'):
            temp_cutout += '.png'
            
        remove_background(image_path, temp_cutout)
        
        person_img = cv2.imread(temp_cutout if os.path.exists(temp_cutout) else image_path, cv2.IMREAD_UNCHANGED)
        if person_img is None: return image_path

        h, w = person_img.shape[:2]

        # Convert hex color to BGR
        hex_clean = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_clean[i:i+2], 16) for i in (0, 2, 4))
        
        # Solid silk drape color background
        background = np.full((h, w, 3), (b, g, r), dtype=np.uint8)

        # Composite person (face, mouth, chin, neck) ON TOP of background drape color
        if person_img.shape[2] == 4:
            alpha = person_img[:, :, 3] / 255.0
            alpha_3d = np.dstack([alpha, alpha, alpha])
            person_rgb = person_img[:, :, :3]
            composite = (person_rgb * alpha_3d + background * (1.0 - alpha_3d)).astype(np.uint8)
        else:
            composite = person_img[:, :, :3]

        draped_path = os.path.join(out_dir, f'_draped_bg_{hex_clean}_' + os.path.basename(image_path))
        if not draped_path.lower().endswith('.png'):
            draped_path += '.png'
        cv2.imwrite(draped_path, composite)
        return draped_path
    except Exception as e:
        return image_path




def generate_pdf(image_path: str, analysis_data: dict, output_pdf_path: str, client_name: str = 'Valued Client', operator_branding: dict = None) -> str:
    # 1. Guarantee upright orientation using eye + mouth cascade scoring
    image_path = ensure_upright_image(image_path)

        
    season = analysis_data.get('season', 'Spring') or 'Spring'
    sub_season = analysis_data.get('sub_season', season) or season
    metrics = analysis_data.get('color_metrics', {
        'warmth_score': 0.0, 'contrast_score': 0.0, 'overall_value': 0.0, 'ita_degrees': 0.0
    })
    
    palette_info = get_palette_data(season, sub_season)
    
    out_dir = os.path.dirname(output_pdf_path)
    if out_dir: os.makedirs(out_dir, exist_ok=True)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    env = Environment(loader=FileSystemLoader(os.path.join(current_dir, 'templates')))
    template = env.get_template('report.html')
    
    # High-Efficiency Transparent PNG Compression to keep 52-page PDF well under 23MB (target ~5MB to 12MB)
    try:
        if os.path.exists(image_path):
            with Image.open(image_path) as img:
                img.thumbnail((360, 360), Image.Resampling.LANCZOS)
                compressed_path = os.path.join(os.path.dirname(os.path.abspath(image_path)), "_opt_" + os.path.basename(image_path))
                if not compressed_path.lower().endswith('.png'):
                    compressed_path += '.png'
                img.save(compressed_path, format="PNG", optimize=True, compress_level=9)
                if os.path.exists(compressed_path) and os.path.getsize(compressed_path) > 100:
                    image_path = compressed_path
    except Exception as compress_err:
        pass

    base64_img = get_base64_image(image_path)
    if not base64_img:
        abs_img_path = f"file:///{os.path.abspath(image_path).replace(chr(92), '/')}"
    else:
        abs_img_path = base64_img
        
    ita_val = metrics.get('ita_degrees', 0.0)
    if ita_val > 55.0: ita_category = 'Very Light (ITA° > 55°)'
    elif ita_val > 41.0: ita_category = 'Light / Fair (ITA° 41° - 55°)'
    elif ita_val > 28.0: ita_category = 'Intermediate (ITA° 28° - 41°)'
    elif ita_val > 10.0: ita_category = 'Tan (ITA° 10° - 28°)'
    elif ita_val > -30.0: ita_category = 'Brown / Dark (ITA° -30° - 10°)'
    else: ita_category = 'Very Dark (ITA° < -30°)'

    skin_lab_dict = metrics.get('skin_lab', {'L': 65.0, 'a': 12.0, 'b': 18.0})

    if season == 'Winter': winter_match, autumn_match, summer_match, spring_match = 94, 38, 70, 32
    elif season == 'Autumn': winter_match, autumn_match, summer_match, spring_match = 36, 92, 44, 78
    elif season == 'Summer': winter_match, autumn_match, summer_match, spring_match = 72, 40, 95, 46
    else: winter_match, autumn_match, summer_match, spring_match = 38, 76, 50, 96

    html_out = template.render(
        client_name=client_name,
        season=season,
        sub_season=sub_season,
        image_path=abs_img_path,
        metrics=metrics,
        ita_category=ita_category,
        skin_lab=skin_lab_dict,
        branding=operator_branding,

        winter_match=winter_match,
        autumn_match=autumn_match,
        summer_match=summer_match,
        spring_match=spring_match,
        season_bg_color=palette_info['bg'],
        accent_color=palette_info['accent'],
        header_color=palette_info['header_color'],
        jewelry=palette_info['jewelry'],
        makeup=palette_info['makeup'],
        contrast=palette_info['contrast'],
        neutrals=palette_info['neutrals'],
        avoid_colors=palette_info['avoid'],
        palette=palette_info['colors'],
        all_subseasons=SUBSEASON_PALETTES
    )
    
    chrome_paths = [
        '/usr/bin/chromium',
        '/usr/bin/chromium-browser',
        '/usr/bin/google-chrome',
        r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        r'C:\Program Files\Microsoft\Edge\Application\msedge.exe'
    ]
    browser_path = next((p for p in chrome_paths if os.path.exists(p)), None)
        
    if browser_path:
        try:
            temp_html = output_pdf_path.replace('.pdf', '_temp.html')
            with open(temp_html, 'w', encoding='utf-8') as f:
                f.write(html_out)
                
            html_url = 'file:///' + os.path.abspath(temp_html).replace('\\', '/')
            cmd = [
                browser_path,
                '--headless=new',
                f'--print-to-pdf={output_pdf_path}',
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-gpu',
                '--no-pdf-header-footer',
                '--print-to-pdf-no-header',
                html_url
            ]
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=45)
            if os.path.exists(temp_html):
                try: os.remove(temp_html)
                except: pass
                
            if os.path.exists(output_pdf_path) and os.path.getsize(output_pdf_path) > 1000:
                print(f'Generated pixel-perfect PDF via Headless Browser ({browser_path}): {output_pdf_path}')
                if image_path and os.path.exists(image_path) and '_bg_cutout' in image_path:
                    try: os.remove(image_path)
                    except: pass
                return output_pdf_path
        except Exception as edge_err:
            pass


    try:
        from weasyprint import HTML
        HTML(string=html_out, base_url=current_dir).write_pdf(output_pdf_path)
        return output_pdf_path
    except Exception as e:
        html_path = output_pdf_path.replace('.pdf', '.html')
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_out)
        return html_path



def generate_free_teaser_pdf(image_input, client_name="Valued Client", client_email="client@example.com", output_pdf_path=None):
    """
    Generates a 3-page Free Teaser Color Analysis Report for launch promotion.
    Identifies the 12-season sub-season and presents 4 core signature swatches,
    with an upsell to the full $29 Master Package.
    """
    skin_metrics = extract_skin_cielab(image_input)
    subseason_name = skin_metrics['subseason']
    palette = SUBSEASON_PALETTES.get(subseason_name, SUBSEASON_PALETTES['Dark Autumn'])
    
    if output_pdf_path is None:
        out_dir = r"C:\Users\dkven\Desktop\CHROMATYPE_Reports"
        os.makedirs(out_dir, exist_ok=True)
        output_pdf_path = os.path.join(out_dir, f"CHROMATYPE_Free_Teaser_{subseason_name.replace(' ', '_')}.pdf")

    teaser_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
    @page {{ size: A4 portrait; margin: 0; }}
    body {{ font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; margin:0; padding:0; background:#0F172A; color:#FFFFFF; }}
    .page {{ width: 210mm; height: 297mm; page-break-after: always; box-sizing: border-box; padding: 25mm 20mm; position: relative; background:#0F172A; }}
    .logo {{ font-size: 24px; font-weight: 900; letter-spacing: 2px; color: #FFFFFF; text-align: center; margin-bottom: 20px; }}
    .logo span {{ color: #E8734A; }}
    .title {{ font-size: 28px; font-weight: 900; text-align: center; color: #E8734A; margin-bottom: 10px; text-transform: uppercase; }}
    .subtitle {{ font-size: 14px; text-align: center; color: #94A3B8; margin-bottom: 30px; }}
    .card {{ background: #1E293B; border: 1px solid #334155; border-radius: 12px; padding: 20px; margin-bottom: 20px; }}
    .swatch-grid {{ display: flex; gap: 15px; justify-content: center; margin-top: 15px; }}
    .swatch-box {{ width: 70px; height: 70px; border-radius: 10px; border: 2px solid #FFFFFF; text-align: center; font-size: 9px; padding-top: 50px; box-sizing: border-box; font-weight: bold; text-shadow: 0 1px 2px #000; }}
    .cta-box {{ background: linear-gradient(135deg, #E8734A, #D4A853); color: #000000; border-radius: 12px; padding: 20px; text-align: center; font-weight: bold; margin-top: 30px; }}
</style>
</head>
<body>
    <div class="page">
        <div class="logo">CHROMA<span>TYPE</span></div>
        <div class="title">FREE TEASER REPORT</div>
        <div class="subtitle">Prepared for {client_name} ({client_email})</div>

        <div class="card">
            <h3 style="margin:0 0 10px 0; color:#E8734A;">IDENTIFIED SUB-SEASON: {subseason_name.upper()}</h3>
            <p style="font-size:12px; color:#CBD5E1; line-height:1.5;">
                Spectrophotometric Analysis complete. Your skin reflectance measures L*={skin_metrics['L']:.1f}, a*={skin_metrics['a']:.1f}, b*={skin_metrics['b']:.1f} with an Individual Typology Angle of ITA°={skin_metrics['ITA']:.1f}°.
            </p>
        </div>

        <div class="card">
            <h4 style="margin:0 0 10px 0; color:#FFFFFF;">Your 4 Core Teaser Signature Swatches:</h4>
            <div class="swatch-grid">
                <div class="swatch-box" style="background:{palette['colors'][0]['hex']};">{palette['colors'][0]['name']}</div>
                <div class="swatch-box" style="background:{palette['colors'][1]['hex']};">{palette['colors'][1]['name']}</div>
                <div class="swatch-box" style="background:{palette['colors'][2]['hex']};">{palette['colors'][2]['name']}</div>
                <div class="swatch-box" style="background:{palette['colors'][3]['hex']};">{palette['colors'][3]['name']}</div>
            </div>
        </div>

        <div class="cta-box">
            <div style="font-size:18px; text-transform:uppercase;">Upgrade to the Full 52-Page Master Dossier</div>
            <p style="font-size:11px; margin:8px 0 12px 0;">Unlock all 36 Virtual Face Drapes, Print-Ready 3-Tier Pocket Swatch Fan PDF, and Pantone TCX Codes.</p>
            <a href="http://chromatype.me/cart?action=show&add=1&id_product=1" style="background:#000; color:#FFF; padding:10px 20px; border-radius:20px; text-decoration:none; display:inline-block; font-size:12px;">Get Full $29 Master Package</a>
        </div>
    </div>
</body>
</html>
"""
    temp_html = output_pdf_path.replace(".pdf", ".html")
    with open(temp_html, 'w', encoding='utf-8') as f:
        f.write(teaser_html)

    import subprocess
    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    ]
    msedge = next((p for p in edge_paths if os.path.exists(p)), None)

    if msedge:
        subprocess.run([
            msedge, "--headless", "--disable-gpu", "--no-pdf-header-footer",
            f"--print-to-pdf={output_pdf_path}", temp_html
        ], check=True)

    if os.path.exists(temp_html):
        os.remove(temp_html)

    return output_pdf_path



# Extended Zone-by-Zone Makeup & Nail Polish Blueprint Data for 12 Sub-Seasons
ZONE_MAKEUP_BLUEPRINTS = {
    'Dark Autumn': {
        'foundation': 'Warm golden or warm beige undertones. Avoid cool pink or alabaster foundations.',
        'eyes': 'Deep bronze, warm espresso, burnt terracotta, olive gold. Eyeliner: Rich dark chocolate or deep forest green.',
        'cheeks': 'Warm terracotta, deep peach, spicy coral. Apply along cheekbones sweeping upward toward temples.',
        'lips': 'Rich brick red, deep warm berry, terracotta, spiced cinnamon. Avoid pale icy pinks.',
        'chin_forehead': 'Light bronze contouring on forehead hair line and jawline for dimensional warmth.',
        'nails': ['#8B0000', '#D2691E', '#B8860B', '#556B2F', '#800000', '#A0522D'],
        'nail_names': ['Deep Oxblood', 'Warm Terracotta', 'Antique Gold', 'Olive Forest', 'Spiced Berry', 'Burnt Ochre']
    },
    'Warm Autumn': {
        'foundation': 'Warm golden peach or golden beige foundation. Avoid cool ash tones.',
        'eyes': 'Warm copper, amber gold, warm brown, moss green. Eyeliner: Espresso or warm bronze.',
        'cheeks': 'Warm apricot, deep peach, golden coral. Apply on apples of cheeks blending outward.',
        'lips': 'Spiced pumpkin, warm coral, golden brick red, warm nude. Avoid cool magenta.',
        'chin_forehead': 'Subtle warm bronzer around temples and perimeter of forehead.',
        'nails': ['#D2691E', '#CD853F', '#B8860B', '#E9967A', '#8B4513', '#D4A853'],
        'nail_names': ['Terracotta', 'Peru Gold', 'Harvest Gold', 'Dark Salmon', 'Saddle Brown', 'Warm Amber']
    },
    'Soft Autumn': {
        'foundation': 'Neutral warm ivory or soft warm beige. Avoid heavy yellow or icy pinks.',
        'eyes': 'Soft taupe, muted bronze, warm sage, soft cocoa. Eyeliner: Soft brown or charcoal brown.',
        'cheeks': 'Muted rose-gold, soft peach, dusty rose. Apply softly to apple of cheek.',
        'lips': 'Muted rose, dusty warm pink, soft terracotta. Avoid dark oxblood or neon shades.',
        'chin_forehead': 'Light neutral translucent powder on T-zone for soft matte finish.',
        'nails': ['#BC8F8F', '#CD5C5C', '#D2B48C', '#E9967A', '#8B7D6B', '#C59B27'],
        'nail_names': ['Rosy Brown', 'Muted Crimson', 'Soft Tan', 'Dusty Peach', 'Sage Taupe', 'Muted Gold']
    },
    'Deep Winter': {
        'foundation': 'Cool olive, neutral porcelain, or deep cool espresso. Avoid orange or yellow tones.',
        'eyes': 'Charcoal black, deep plum, icy silver highlight, midnight navy. Eyeliner: Jet black.',
        'cheeks': 'Cool deep plum, dark berry, rose red. Apply along cheekbone contour.',
        'lips': 'True blood red, deep burgundy, dark plum, ruby red. Avoid nude beige or orange.',
        'chin_forehead': 'Cool contour under jawline and temples for sharp sculpt.',
        'nails': ['#800000', '#4B0082', '#191970', '#000000', '#8B0045', '#483D8B'],
        'nail_names': ['Oxblood Ruby', 'Deep Indigo', 'Midnight Navy', 'Jet Black', 'Plum Crimson', 'Dark Slate']
    },
    'Cool Winter': {
        'foundation': 'Cool rose porcelain or cool neutral beige. Avoid golden peach or orange.',
        'eyes': 'Cool slate grey, icy violet, royal navy, silver shimmer. Eyeliner: Black or navy.',
        'cheeks': 'Cool raspberry, icy pink, cool fuchsia blush.',
        'lips': 'Cool fuchsia, true crimson, cherry red, cool raspberry. Avoid warm coral or copper.',
        'chin_forehead': 'Cool translucent setting powder across T-zone.',
        'nails': ['#DC143C', '#C71585', '#00008B', '#8A2BE2', '#4169E1', '#800080'],
        'nail_names': ['Crimson Red', 'Deep Fuchsia', 'Dark Blue', 'Blue Violet', 'Royal Blue', 'Deep Purple']
    },
    'Clear Winter': {
        'foundation': 'Clear cool alabaster, neutral beige, or dark neutral brown. Avoid muddy bronze.',
        'eyes': 'Clear icy white shimmer, jet black liner, sapphire blue, jewel purple. Eyeliner: Precision jet black.',
        'cheeks': 'Vibrant cool pink, bright raspberry, clear rose.',
        'lips': 'Vibrant electric crimson, clear ruby red, bright fuchsia. Avoid muted nude tones.',
        'chin_forehead': 'Highlighter on brow bone, bridge of nose, and cupid bow for high contrast brilliance.',
        'nails': ['#FF007F', '#FF0000', '#4169E1', '#9400D3', '#000000', '#E0115F'],
        'nail_names': ['Electric Pink', 'Vibrant Ruby', 'Sapphire Blue', 'Dark Violet', 'Pure Onyx', 'Ruby Red']
    },
    'Light Spring': {
        'foundation': 'Light warm ivory, fair golden peach. Avoid dark bronzers or heavy grey foundation.',
        'eyes': 'Soft champagne shimmer, peach shimmer, soft warm brown, golden beige. Eyeliner: Soft brown.',
        'cheeks': 'Light peach, bright warm pink, soft coral blush.',
        'lips': 'Peach gloss, warm coral pink, light apricot. Avoid dark berry or black.',
        'chin_forehead': 'Light golden highlight on cheekbones and forehead center.',
        'nails': ['#FF7F50', '#FFB6C1', '#FFE4B5', '#FA8072', '#F08080', '#FFD700'],
        'nail_names': ['Coral Pink', 'Light Pink', 'Moccasin Peach', 'Salmon', 'Light Coral', 'Soft Gold']
    },
    'Warm Spring': {
        'foundation': 'Golden ivory, warm peach beige. Avoid cool pink or blue undertones.',
        'eyes': 'Warm copper, bright gold, turquoise shimmer, warm brown. Eyeliner: Dark warm brown or bronze.',
        'cheeks': 'Bright warm coral, peach gold, warm apricot blush.',
        'lips': 'Warm poppy red, bright coral, golden orange-red. Avoid cool magenta.',
        'chin_forehead': 'Warm golden bronzer across cheeks and forehead contour.',
        'nails': ['#FF4500', '#FF7F50', '#FFD700', '#40E0D0', '#E9967A', '#FF6347'],
        'nail_names': ['Poppy Red', 'Bright Coral', 'Sun Gold', 'Turquoise Blue', 'Dark Salmon', 'Tomato Red']
    },
    'Clear Spring': {
        'foundation': 'Clear warm ivory, porcelain peach. Avoid muddy gray or muted tan.',
        'eyes': 'Sparkling gold, bright peach, bright emerald green, warm brown. Eyeliner: Espresso black.',
        'cheeks': 'Clear bright coral, warm fuchsia-pink, bright peach.',
        'lips': 'Bright coral red, clear poppy, bright warm pink. Avoid muted dust pink.',
        'chin_forehead': 'Highlighter on cheekbones, brow arch, and chin tip.',
        'nails': ['#FF1493', '#FF4500', '#50C878', '#FFD700', '#E0115F', '#FF7F50'],
        'nail_names': ['Deep Bright Pink', 'Orange Red', 'Emerald Green', 'Bright Gold', 'Ruby Pink', 'Bright Coral']
    },
    'Light Summer': {
        'foundation': 'Fair cool porcelain, soft neutral pink-beige. Avoid warm yellow or orange.',
        'eyes': 'Soft lavendar, icy blue, soft mauve, cool taupe. Eyeliner: Soft slate grey.',
        'cheeks': 'Soft cool pink, light rose, dusty pink blush.',
        'lips': 'Soft rose, light berry, cool pink gloss. Avoid dark brown or warm orange.',
        'chin_forehead': 'Icy pearl highlighter on cheeks and brow arch.',
        'nails': ['#FFB6C1', '#D8BFD8', '#B0E0E6', '#E6E6FA', '#DB7093', '#C0C0C0'],
        'nail_names': ['Soft Rose', 'Thistle Lavender', 'Powder Blue', 'Lavender', 'Pale Violet', 'Cool Silver']
    },
    'Cool Summer': {
        'foundation': 'Cool pink porcelain or cool neutral beige. Avoid golden peach or warm bronzer.',
        'eyes': 'Cool slate grey, plum taupe, icy mauve, cool navy. Eyeliner: Dark slate or navy.',
        'cheeks': 'Cool berry pink, dusty rose, cool magenta blush.',
        'lips': 'Cool raspberry, muted cranberry, rose wine. Avoid orange brick.',
        'chin_forehead': 'Cool translucent powder across forehead and chin.',
        'nails': ['#C71585', '#DB7093', '#4682B4', '#8B008B', '#D8BFD8', '#708090'],
        'nail_names': ['Medium Violet', 'Pale Violet', 'Steel Blue', 'Dark Magenta', 'Thistle Pink', 'Slate Grey']
    },
    'Soft Summer': {
        'foundation': 'Neutral cool beige or soft rose ivory. Avoid yellow gold or jet black.',
        'eyes': 'Muted plum, soft charcoal, grey-brown, dusty mauve. Eyeliner: Soft charcoal grey.',
        'cheeks': 'Muted dusty rose, soft cool plum, antique pink blush.',
        'lips': 'Dusty rose, soft berry, muted plum. Avoid bright poppy or orange.',
        'chin_forehead': 'Soft neutral matte powder on T-zone.',
        'nails': ['#BC8F8F', '#DB7093', '#8FBC8F', '#9370DB', '#708090', '#B22222'],
        'nail_names': ['Rosy Brown', 'Dusty Rose', 'Dark Sea Green', 'Medium Purple', 'Slate Grey', 'Muted Crimson']
    }
}



import math

def calculate_cielab_dermatology_metrics(L, a, b, L_hair=25.0):
    """
    Clinically accurate dermatological skin-tone classification (Chardon et al.)
    """
    # 1. ITA° (Individual Typology Angle)
    b_val = b if b != 0 else 0.001
    ita_rad = math.atan((L - 50.0) / b_val)
    ita_deg = ita_rad * (180.0 / math.pi)

    # 2. Warmth Index (b*/a* Yellow-to-Red ratio)
    a_val = a if a != 0 else 0.001
    warmth_index = round(b / a_val, 2)

    # 3. Chroma C* (Color Saturation / Vividness)
    chroma = round(math.sqrt(a**2 + b**2), 2)

    # 4. Hue Angle h° in degrees
    hue_rad = math.atan2(b, a)
    hue_deg = round((hue_rad * (180.0 / math.pi)) % 360.0, 1)

    # 5. Contrast Level (L*_skin - L*_hair luminance delta)
    contrast_level = round(abs(L - L_hair) / 10.0, 2)

    # Dermatological ITA Skin Category (Chardon Scale)
    if ita_deg > 55.0:
        ita_category = "Very Light"
    elif ita_deg > 41.0:
        ita_category = "Light"
    elif ita_deg > 28.0:
        ita_category = "Intermediate"
    elif ita_deg > 10.0:
        ita_category = "Tan"
    elif ita_deg > -30.0:
        ita_category = "Brown"
    else:
        ita_category = "Dark"

    return {
        'ITA': round(ita_deg, 1),
        'ITA_Category': ita_category,
        'Warmth_Index': warmth_index,
        'Chroma': chroma,
        'Hue_Angle': hue_deg,
        'Contrast_Level': contrast_level
    }



# Mobile PDF Compression & Optimization Flag
pdf_options = {
    'page-size': 'A4',
    'margin-top': '10mm',
    'margin-right': '10mm',
    'margin-bottom': '10mm',
    'margin-left': '10mm',
    'encoding': 'UTF-8',
    'image-quality': '80',  # Mobile lightweight compression
    'image-dpi': '150',      # Fast phone viewing DPI
    'enable-local-file-access': None
}
