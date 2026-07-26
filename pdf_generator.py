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
            {'name': 'Peach Fuzz', 'hex': '#FFBE98'}, {'name': 'Warm Coral', 'hex': '#FF7F67'}, {'name': 'Buttercup Yellow', 'hex': '#FFDE59'},
            {'name': 'Soft Pistachio', 'hex': '#B5E7A0'}, {'name': 'Light Aquamarine', 'hex': '#7FE5D9'}, {'name': 'Golden Honey', 'hex': '#F4C430'},
            {'name': 'Apricot Shimmer', 'hex': '#FBCEB1'}, {'name': 'Warm Turquoise', 'hex': '#40E0D0'}, {'name': 'Periwinkle Warm', 'hex': '#8C9EFF'},
            {'name': 'Flamingo Pink', 'hex': '#FC8EAC'}, {'name': 'Light Sage', 'hex': '#BCCEB4'}, {'name': 'Creamy Ivory', 'hex': '#FFFDD0'},
            {'name': 'Coral Blush', 'hex': '#F88379'}, {'name': 'Soft Sunshine', 'hex': '#FFE37A'}, {'name': 'Mint Cream', 'hex': '#A8E6CF'},
            {'name': 'Warm Pearl', 'hex': '#F5E6D3'}, {'name': 'Peach Sorbet', 'hex': '#FFCBA4'}, {'name': 'Light Salmon', 'hex': '#FFA07A'},
            {'name': 'Golden Sand', 'hex': '#E6C280'}, {'name': 'Pale Aqua', 'hex': '#BCD4E6'}, {'name': 'Spring Green', 'hex': '#98FB98'},
            {'name': 'Warm Champagne', 'hex': '#F7E7CE'}, {'name': 'Blush Peach', 'hex': '#FDB9B7'}, {'name': 'Soft Tangerine', 'hex': '#FFC3A0'},
            {'name': 'Light Lime', 'hex': '#D4E157'}, {'name': 'Warm Powder Blue', 'hex': '#90CAF9'}, {'name': 'Vanilla Custard', 'hex': '#FFF8DC'},
            {'name': 'Golden Apricot', 'hex': '#F3A505'}, {'name': 'Light Melon', 'hex': '#FEBAAD'}, {'name': 'Soft Coral Red', 'hex': '#F07167'},
            {'name': 'Warm Mint Green', 'hex': '#A2E8DD'}, {'name': 'Golden Cream', 'hex': '#FFEAA7'}, {'name': 'Warm Lavender', 'hex': '#D1C4E9'},
            {'name': 'Bright Peach', 'hex': '#FF9E9D'}, {'name': 'Light Gold', 'hex': '#FFE082'}, {'name': 'Ivory Silk', 'hex': '#FFFFF0'}
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
            {'name': 'Vibrant Poppy', 'hex': '#FF4500'}, {'name': 'Golden Mango', 'hex': '#FFB300'}, {'name': 'Warm Coral', 'hex': '#FF6F59'},
            {'name': 'Tropical Turquoise', 'hex': '#00A896'}, {'name': 'Bright Lime', 'hex': '#7CB342'}, {'name': 'Warm Terracotta', 'hex': '#D84315'},
            {'name': 'Saffron Yellow', 'hex': '#F4C430'}, {'name': 'Warm Salmon Pink', 'hex': '#FF8A65'}, {'name': 'Bright Teal', 'hex': '#00897B'},
            {'name': 'Golden Wheat', 'hex': '#E5C158'}, {'name': 'Tangerine', 'hex': '#F57C00'}, {'name': 'Olive Gold', 'hex': '#9E9D24'},
            {'name': 'Spiced Orange', 'hex': '#E65100'}, {'name': 'Warm Canary', 'hex': '#FDD835'}, {'name': 'Golden Apricot', 'hex': '#FB8C00'},
            {'name': 'Coral Orange', 'hex': '#FF7043'}, {'name': 'Bright Warm Green', 'hex': '#43A047'}, {'name': 'Warm Amber', 'hex': '#FFB300'},
            {'name': 'Rich Ochre', 'hex': '#C0CA33'}, {'name': 'Deep Coral', 'hex': '#F4511E'}, {'name': 'Tropical Aqua', 'hex': '#26A69A'},
            {'name': 'Warm Copper', 'hex': '#D84315'}, {'name': 'Golden Maize', 'hex': '#FFEE58'}, {'name': 'Warm Rust', 'hex': '#BF360C'},
            {'name': 'Bright Chartreuse', 'hex': '#76FF03'}, {'name': 'Warm Flamingo', 'hex': '#FF5252'}, {'name': 'Golden Sand', 'hex': '#FFE082'},
            {'name': 'Warm Emerald', 'hex': '#00C853'}, {'name': 'Sunset Orange', 'hex': '#FF6D00'}, {'name': 'Warm Turquoise Blue', 'hex': '#00B8D4'},
            {'name': 'Warm Terracotta Red', 'hex': '#DD2C00'}, {'name': 'Golden Daffodil', 'hex': '#FFD600'}, {'name': 'Warm Coral Rose', 'hex': '#FF8A80'},
            {'name': 'Bright Papaya', 'hex': '#FFAB40'}, {'name': 'Warm Jade', 'hex': '#00E676'}, {'name': 'Golden Bronze Light', 'hex': '#FFC400'}
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
            {'name': 'Electric Coral', 'hex': '#FF3D00'}, {'name': 'Bright Turquoise', 'hex': '#00E5FF'}, {'name': 'Canary Yellow', 'hex': '#FFEA00'},
            {'name': 'Hot Pink Warm', 'hex': '#FF1744'}, {'name': 'Vibrant Emerald', 'hex': '#00E676'}, {'name': 'Bright Poppy', 'hex': '#F44336'},
            {'name': 'Luminous Violet', 'hex': '#651FFF'}, {'name': 'Sunny Marigold', 'hex': '#FFC400'}, {'name': 'Clear Aqua', 'hex': '#1DE9B6'},
            {'name': 'Warm Tangerine', 'hex': '#FF9100'}, {'name': 'Bright Fuchsia', 'hex': '#F50057'}, {'name': 'Pure Warm White', 'hex': '#FFFDF7'},
            {'name': 'Electric Orange', 'hex': '#FF6E40'}, {'name': 'Vibrant Cyan', 'hex': '#00B0FF'}, {'name': 'Lemon Lime', 'hex': '#C6FF00'},
            {'name': 'Bright Magenta Warm', 'hex': '#D500F9'}, {'name': 'Clear Emerald', 'hex': '#00BFA5'}, {'name': 'Neon Poppy', 'hex': '#FF1744'},
            {'name': 'Electric Yellow', 'hex': '#FFFF00'}, {'name': 'Vibrant Turquoise', 'hex': '#00E5FF'}, {'name': 'Bright Coral Red', 'hex': '#FF3D00'},
            {'name': 'Bright Marigold', 'hex': '#FFAB00'}, {'name': 'Luminous Pink', 'hex': '#FF4081'}, {'name': 'Clear Chartreuse', 'hex': '#AEEA00'},
            {'name': 'Vibrant Royal Warm', 'hex': '#3D5AFE'}, {'name': 'Electric Violet', 'hex': '#7C4DFF'}, {'name': 'Sunny Yellow', 'hex': '#FFD600'},
            {'name': 'Bright Teal Clear', 'hex': '#00BFA5'}, {'name': 'Vibrant Vermillion', 'hex': '#FF3D00'}, {'name': 'Luminous Cyan', 'hex': '#18FFFF'},
            {'name': 'Electric Fuchsia', 'hex': '#FF007F'}, {'name': 'Clear Lime Green', 'hex': '#64DD17'}, {'name': 'Bright Gold', 'hex': '#FFC400'},
            {'name': 'Vibrant Coral Pink', 'hex': '#FF5252'}, {'name': 'Luminous Aqua', 'hex': '#00E5FF'}, {'name': 'Crisp Warm White', 'hex': '#FFFFFF'}
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
            {'name': 'Soft Rose', 'hex': '#FFB6C1'}, {'name': 'Sky Blue', 'hex': '#87CEEB'}, {'name': 'Lavender Mist', 'hex': '#E6E6FA'},
            {'name': 'Cool Mint', 'hex': '#A8E6CF'}, {'name': 'Dusty Pink', 'hex': '#D8BFD8'}, {'name': 'Periwinkle', 'hex': '#CCCCFF'},
            {'name': 'Light Slate', 'hex': '#778899'}, {'name': 'Soft Orchid', 'hex': '#DA70D6'}, {'name': 'Powder Blue', 'hex': '#B0E0E6'},
            {'name': 'Icy Aqua', 'hex': '#AFEEEE'}, {'name': 'Lilac Rose', 'hex': '#C8A2C8'}, {'name': 'Pearl Gray', 'hex': '#E5E8E8'},
            {'name': 'Soft Powder Pink', 'hex': '#FFC0CB'}, {'name': 'Cloud Blue', 'hex': '#ADD8E6'}, {'name': 'Pale Wisteria', 'hex': '#C9A0DC'},
            {'name': 'Cool Seafoam', 'hex': '#93E9BE'}, {'name': 'Soft Carnation', 'hex': '#F4C2C2'}, {'name': 'Ice Blue', 'hex': '#D0F0C0'},
            {'name': 'Mist Gray', 'hex': '#D3D3D3'}, {'name': 'Soft Mauve Light', 'hex': '#E0B0FF'}, {'name': 'Baby Blue Cool', 'hex': '#A2C4C9'},
            {'name': 'Pale Lavender', 'hex': '#DCD0FF'}, {'name': 'Dusty Rose Light', 'hex': '#DCAE96'}, {'name': 'Cool Pearl White', 'hex': '#F8F9FA'},
            {'name': 'Soft Thistle', 'hex': '#D8BFD8'}, {'name': 'Light Cool Teal', 'hex': '#80CBD3'}, {'name': 'Pale Plum', 'hex': '#DDA0DD'},
            {'name': 'Soft Denim Light', 'hex': '#9BB7D4'}, {'name': 'Dusty Blush', 'hex': '#DE9AAC'}, {'name': 'Cool Platinum Gray', 'hex': '#E0E5E5'},
            {'name': 'Soft Hyacinth', 'hex': '#A2A2D0'}, {'name': 'Pale Aquamarine', 'hex': '#93DFB8'}, {'name': 'Light Rose Taupe', 'hex': '#905D5D'},
            {'name': 'Cool Hydrangea', 'hex': '#88ACE0'}, {'name': 'Soft Shell Pink', 'hex': '#FFD1DC'}, {'name': 'Crisp Pure White', 'hex': '#F0F8FF'}
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
            {'name': 'Classic Sapphire', 'hex': '#0F52BA'}, {'name': 'Cool Raspberry', 'hex': '#C2185B'}, {'name': 'Ocean Blue', 'hex': '#1976D2'},
            {'name': 'Deep Orchid', 'hex': '#8E24AA'}, {'name': 'Plum Rose', 'hex': '#880E4F'}, {'name': 'Cool Emerald', 'hex': '#00796B'},
            {'name': 'Slate Blue', 'hex': '#4682B4'}, {'name': 'Magenta Mist', 'hex': '#D81B60'}, {'name': 'Royal Violet', 'hex': '#5E35B1'},
            {'name': 'Icy Periwinkle', 'hex': '#7986CB'}, {'name': 'Cool Spruce', 'hex': '#004D40'}, {'name': 'Charcoal Slate', 'hex': '#37474F'},
            {'name': 'Cool Cranberry', 'hex': '#9C27B0'}, {'name': 'Cobalt Blue Cool', 'hex': '#1565C0'}, {'name': 'Cool Berry', 'hex': '#AD1457'},
            {'name': 'Deep Lavender', 'hex': '#7B1FA2'}, {'name': 'Pine Green Cool', 'hex': '#00695C'}, {'name': 'Cool Navy Blue', 'hex': '#1A237E'},
            {'name': 'Slate Teal', 'hex': '#006064'}, {'name': 'Cool Rosewood', 'hex': '#6A1B9A'}, {'name': 'French Blue', 'hex': '#007FFF'},
            {'name': 'Deep Fuchsia Cool', 'hex': '#AB47BC'}, {'name': 'Cool Spruce Green', 'hex': '#004D40'}, {'name': 'Twilight Violet', 'hex': '#4A148C'},
            {'name': 'Cool Indigo', 'hex': '#283593'}, {'name': 'Plum Purple Deep', 'hex': '#4A0033'}, {'name': 'Cool Steel Gray', 'hex': '#546E7A'},
            {'name': 'Ocean Teal Cool', 'hex': '#00838F'}, {'name': 'Deep Berry Rose', 'hex': '#880E4F'}, {'name': 'Cool Violet Blue', 'hex': '#3F51B5'},
            {'name': 'Dark Cool Slate', 'hex': '#263238'}, {'name': 'Cool Amethyst', 'hex': '#9C27B0'}, {'name': 'Deep Sea Blue', 'hex': '#0D47A1'},
            {'name': 'Cool Damson Plum', 'hex': '#311B92'}, {'name': 'Cool Wine Red', 'hex': '#4A001F'}, {'name': 'Pure Cold White', 'hex': '#F5F5F5'}
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
            {'name': 'Muted Rose', 'hex': '#C27BA0'}, {'name': 'Dusty Teal', 'hex': '#4A7C59'}, {'name': 'Smoky Slate', 'hex': '#708090'},
            {'name': 'Soft Plum', 'hex': '#7B5269'}, {'name': 'Muted Sage', 'hex': '#8F9E8B'}, {'name': 'Dusty Violet', 'hex': '#8B7D7B'},
            {'name': 'Rose Taupe', 'hex': '#905D5D'}, {'name': 'Smoky Blue', 'hex': '#5B7086'}, {'name': 'Soft Cocoa', 'hex': '#80685E'},
            {'name': 'Muted Lavender', 'hex': '#967BB6'}, {'name': 'Dusty Cedar', 'hex': '#AD6D75'}, {'name': 'Heather Gray', 'hex': '#B6B6B4'},
            {'name': 'Soft Mulberry', 'hex': '#854D5D'}, {'name': 'Muted Aqua', 'hex': '#6A998E'}, {'name': 'Dusty Mauve', 'hex': '#915C83'},
            {'name': 'Smoky Green', 'hex': '#556B2F'}, {'name': 'Soft Crimson Muted', 'hex': '#A75D5D'}, {'name': 'Muted Periwinkle', 'hex': '#7982B9'},
            {'name': 'Soft Charcoal', 'hex': '#4F5D65'}, {'name': 'Dusty Plum Rose', 'hex': '#704264'}, {'name': 'Muted Spruce', 'hex': '#3B6B64'},
            {'name': 'Soft Rosewood', 'hex': '#9E5B6A'}, {'name': 'Smoky Indigo', 'hex': '#465362'}, {'name': 'Dusty Raspberry', 'hex': '#A04768'},
            {'name': 'Muted Sage Teal', 'hex': '#588157'}, {'name': 'Soft Wine Muted', 'hex': '#723D46'}, {'name': 'Dusty Blue Gray', 'hex': '#6C7A89'},
            {'name': 'Muted Heather', 'hex': '#9B870C'}, {'name': 'Soft Olive Muted', 'hex': '#6B705C'}, {'name': 'Dusty Orchid', 'hex': '#86608E'},
            {'name': 'Smoky Navy Muted', 'hex': '#2C3E50'}, {'name': 'Soft Pewter', 'hex': '#8E9AAF'}, {'name': 'Dusty Rose Muted', 'hex': '#B5838D'},
            {'name': 'Muted Forest Green', 'hex': '#344E41'}, {'name': 'Soft Plum Gray', 'hex': '#605B56'}, {'name': 'Stone Beige Cool', 'hex': '#A39B8B'}
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
            {'name': 'Soft Terracotta', 'hex': '#C87D55'}, {'name': 'Muted Olive', 'hex': '#708238'}, {'name': 'Warm Rose Taupe', 'hex': '#A76D60'},
            {'name': 'Soft Teal', 'hex': '#3B7A57'}, {'name': 'Warm Camel', 'hex': '#C19A6B'}, {'name': 'Dusty Peach', 'hex': '#D9822B'},
            {'name': 'Muted Gold', 'hex': '#D4AF37'}, {'name': 'Soft Sage', 'hex': '#77896C'}, {'name': 'Warm Sand', 'hex': '#E5AA70'},
            {'name': 'Muted Rust', 'hex': '#B85233'}, {'name': 'Soft Moss', 'hex': '#4A5D4E'}, {'name': 'Creamy Beige', 'hex': '#F5F5DC'},
            {'name': 'Soft Amber', 'hex': '#D27D2D'}, {'name': 'Muted Jade', 'hex': '#5B8C5A'}, {'name': 'Dusty Coral Warm', 'hex': '#D46A6A'},
            {'name': 'Warm Khaki', 'hex': '#C3B091'}, {'name': 'Soft Copper', 'hex': '#B87333'}, {'name': 'Muted Mustard', 'hex': '#E1AD01'},
            {'name': 'Soft Walnut', 'hex': '#773F1A'}, {'name': 'Dusty Apricot', 'hex': '#DE8A5A'}, {'name': 'Muted Pine', 'hex': '#2D5A27'},
            {'name': 'Warm Mocha', 'hex': '#967969'}, {'name': 'Soft Ochre', 'hex': '#CC7722'}, {'name': 'Dusty Warm Rose', 'hex': '#BC6C25'},
            {'name': 'Muted Terracotta', 'hex': '#B25329'}, {'name': 'Soft Bronze', 'hex': '#CD7F32'}, {'name': 'Warm Slate Green', 'hex': '#606C38'},
            {'name': 'Dusty Goldenrod', 'hex': '#DAA520'}, {'name': 'Soft Cinnamon', 'hex': '#D2691E'}, {'name': 'Muted Eucalyptus', 'hex': '#5F7A61'},
            {'name': 'Warm Cocoa Light', 'hex': '#8C6747'}, {'name': 'Soft Brick Red', 'hex': '#B22222'}, {'name': 'Dusty Warm Tan', 'hex': '#D2B48C'},
            {'name': 'Muted Olive Drab', 'hex': '#6B8E23'}, {'name': 'Soft Amber Gold', 'hex': '#E59866'}, {'name': 'Warm Oat', 'hex': '#D6C7B2'}
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
            {'name': 'Rich Terracotta', 'hex': '#D35400'}, {'name': 'Burnt Orange', 'hex': '#CC5500'}, {'name': 'Golden Olive', 'hex': '#808000'},
            {'name': 'Warm Copper', 'hex': '#B87333'}, {'name': 'Deep Mustard', 'hex': '#E5A65D'}, {'name': 'Forest Green Warm', 'hex': '#2E7D32'},
            {'name': 'Warm Mahogany', 'hex': '#C0392B'}, {'name': 'Amber Gold', 'hex': '#FFBF00'}, {'name': 'Warm Rust Red', 'hex': '#A04000'},
            {'name': 'Deep Teal Warm', 'hex': '#00695C'}, {'name': 'Golden Camel', 'hex': '#C19A6B'}, {'name': 'Rich Chocolate', 'hex': '#4A235A'},
            {'name': 'Spiced Amber', 'hex': '#D35400'}, {'name': 'Golden Saffron', 'hex': '#F39C12'}, {'name': 'Warm Chestnut', 'hex': '#935116'},
            {'name': 'Warm Olive Drab', 'hex': '#556B2F'}, {'name': 'Deep Terracotta', 'hex': '#BA4A00'}, {'name': 'Golden Ochre', 'hex': '#B7950B'},
            {'name': 'Warm Cinnamon Red', 'hex': '#7B241C'}, {'name': 'Rich Teal Green', 'hex': '#117A65'}, {'name': 'Golden Bronze', 'hex': '#A0522D'},
            {'name': 'Warm Pumpkin', 'hex': '#E67E22'}, {'name': 'Deep Forest Olive', 'hex': '#1E8449'}, {'name': 'Golden Russet', 'hex': '#804000'},
            {'name': 'Warm Spiced Apple', 'hex': '#900C3F'}, {'name': 'Golden Honey Deep', 'hex': '#D4AC0D'}, {'name': 'Rich Sienna', 'hex': '#A0522D'},
            {'name': 'Warm Pine', 'hex': '#145A32'}, {'name': 'Deep Golden Amber', 'hex': '#B7950B'}, {'name': 'Warm Crimson Brown', 'hex': '#6E2C00'},
            {'name': 'Rich Emerald Warm', 'hex': '#196F3D'}, {'name': 'Golden Khaki Deep', 'hex': '#9A7D0A'}, {'name': 'Warm Terracotta Gold', 'hex': '#CA6F1E'},
            {'name': 'Rich Espresso', 'hex': '#3E2723'}, {'name': 'Warm Golden Wheat', 'hex': '#F7DC6F'}, {'name': 'Warm Ivory Cream', 'hex': '#FDFEFE'}
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
            {'name': 'Deep Espresso', 'hex': '#3B2F2F'}, {'name': 'Rich Burgundy', 'hex': '#800020'}, {'name': 'Dark Forest Green', 'hex': '#1E4620'},
            {'name': 'Deep Copper', 'hex': '#8B4513'}, {'name': 'Dark Teal', 'hex': '#004D40'}, {'name': 'Burnt Terracotta', 'hex': '#9E2A2B'},
            {'name': 'Deep Bronze', 'hex': '#5C4033'}, {'name': 'Dark Mustard Gold', 'hex': '#B8860B'}, {'name': 'Dark Plum Warm', 'hex': '#581845'},
            {'name': 'Deep Olive', 'hex': '#355E3B'}, {'name': 'Rich Chocolate Brown', 'hex': '#2E1A47'}, {'name': 'Warm Black Brown', 'hex': '#1C100B'},
            {'name': 'Deep Cinnamon', 'hex': '#7B241C'}, {'name': 'Dark Emerald Warm', 'hex': '#145A32'}, {'name': 'Deep Russet', 'hex': '#6E2C00'},
            {'name': 'Dark Golden Amber', 'hex': '#9A7D0A'}, {'name': 'Deep Crimson Warm', 'hex': '#641E16'}, {'name': 'Dark Spruce', 'hex': '#0B5345'},
            {'name': 'Deep Auburn', 'hex': '#78281F'}, {'name': 'Dark Ochre', 'hex': '#7D6608'}, {'name': 'Deep Maroon Warm', 'hex': '#512E5F'},
            {'name': 'Dark Olive Green', 'hex': '#196F3D'}, {'name': 'Deep Walnut', 'hex': '#4A235A'}, {'name': 'Dark Copper Red', 'hex': '#900C3F'},
            {'name': 'Deep Golden Brown', 'hex': '#6E2C00'}, {'name': 'Dark Teal Green', 'hex': '#0E6251'}, {'name': 'Deep Mahogany', 'hex': '#4A148C'},
            {'name': 'Dark Forest Olive', 'hex': '#114B1E'}, {'name': 'Deep Spiced Plum', 'hex': '#4A0033'}, {'name': 'Dark Goldenrod Deep', 'hex': '#85929E'},
            {'name': 'Deep Blackberry', 'hex': '#2C003E'}, {'name': 'Dark Moss Green', 'hex': '#1E3A1E'}, {'name': 'Deep Warm Charcoal', 'hex': '#212F3D'},
            {'name': 'Dark Chestnut', 'hex': '#5B2C6F'}, {'name': 'Deep Bronze Gold', 'hex': '#7D6608'}, {'name': 'Warm Off Black', 'hex': '#1B2631'}
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
            {'name': 'Deep Black', 'hex': '#0A0A0A'}, {'name': 'Midnight Blue', 'hex': '#000080'}, {'name': 'Dark Emerald', 'hex': '#004B23'},
            {'name': 'Deep Royal Purple', 'hex': '#311B92'}, {'name': 'Pure Crisp White', 'hex': '#FFFFFF'}, {'name': 'Deep Crimson Cool', 'hex': '#880E4F'},
            {'name': 'Dark Sapphire', 'hex': '#0D47A1'}, {'name': 'Deep Magenta Cool', 'hex': '#4A148C'}, {'name': 'Dark Charcoal', 'hex': '#212121'},
            {'name': 'Deep Ruby Red', 'hex': '#B71C1C'}, {'name': 'Dark Forest Emerald', 'hex': '#003300'}, {'name': 'Deep Plum Cool', 'hex': '#3E2723'},
            {'name': 'Midnight Indigo', 'hex': '#1A237E'}, {'name': 'Dark Bordeaux', 'hex': '#4A001F'}, {'name': 'Deep Spruce Cool', 'hex': '#003B46'},
            {'name': 'Dark Violet Blue', 'hex': '#283593'}, {'name': 'Deep Garnet', 'hex': '#800000'}, {'name': 'Dark Teal Cool', 'hex': '#004D40'},
            {'name': 'Deep Amethyst', 'hex': '#4A148C'}, {'name': 'Midnight Navy', 'hex': '#0B132B'}, {'name': 'Dark Berry Wine', 'hex': '#6A1B9A'},
            {'name': 'Deep Cobalt', 'hex': '#1565C0'}, {'name': 'Dark Emerald Pine', 'hex': '#002B1B'}, {'name': 'Deep Plum Violet', 'hex': '#300032'},
            {'name': 'Midnight Blue Black', 'hex': '#05051B'}, {'name': 'Dark Royal Ruby', 'hex': '#900C3F'}, {'name': 'Deep Slate Navy', 'hex': '#1B2A4A'},
            {'name': 'Dark Cool Green', 'hex': '#004D20'}, {'name': 'Deep Burgundy Cool', 'hex': '#581845'}, {'name': 'Midnight Purple', 'hex': '#20002C'},
            {'name': 'Dark Ocean Blue', 'hex': '#0F2027'}, {'name': 'Deep Cherry Red', 'hex': '#A00000'}, {'name': 'Dark Pine Cool', 'hex': '#032B25'},
            {'name': 'Deep Steel Black', 'hex': '#121212'}, {'name': 'Dark Icy Violet', 'hex': '#651FFF'}, {'name': 'Pure Platinum White', 'hex': '#FAFAFA'}
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
            {'name': 'Classic Royal Blue', 'hex': '#002366'}, {'name': 'True Cool Red', 'hex': '#D50000'}, {'name': 'Deep Fuchsia', 'hex': '#C51162'},
            {'name': 'Electric Violet Cool', 'hex': '#6200EA'}, {'name': 'Pure Icy White', 'hex': '#F8F9FA'}, {'name': 'Cool Emerald Green', 'hex': '#00C853'},
            {'name': 'Cobalt Blue Bright', 'hex': '#0055FF'}, {'name': 'Cool Raspberry Red', 'hex': '#E91E63'}, {'name': 'Icy Pink Light', 'hex': '#FF80AB'},
            {'name': 'Cool Slate Gray', 'hex': '#455A64'}, {'name': 'Pure Jet Black', 'hex': '#000000'}, {'name': 'Cool Magenta', 'hex': '#AA00FF'},
            {'name': 'Cool Sapphire Blue', 'hex': '#0D47A1'}, {'name': 'True Berry Red', 'hex': '#C2185B'}, {'name': 'Icy Lavender Blue', 'hex': '#8C9EFF'},
            {'name': 'Cool Spruce Green', 'hex': '#00BFA5'}, {'name': 'Cool Orchid Pink', 'hex': '#E040FB'}, {'name': 'Deep Cool Indigo', 'hex': '#304FFE'},
            {'name': 'Cool Cranberry Red', 'hex': '#D50032'}, {'name': 'Icy Blue Cool', 'hex': '#80D8FF'}, {'name': 'Cool Violet Purple', 'hex': '#7C4DFF'},
            {'name': 'Cool Ocean Teal', 'hex': '#00E5FF'}, {'name': 'Pure Charcoal Gray', 'hex': '#263238'}, {'name': 'Cool Plum Pink', 'hex': '#FF4081'},
            {'name': 'Cool Navy Sapphire', 'hex': '#1A237E'}, {'name': 'True Cool Pink', 'hex': '#FF1744'}, {'name': 'Icy Mint Green', 'hex': '#B9F6CA'},
            {'name': 'Cool Amethyst Purple', 'hex': '#651FFF'}, {'name': 'Cool Pine Green', 'hex': '#00B8D4'}, {'name': 'Cool Rose Pink', 'hex': '#F50057'},
            {'name': 'Deep Cool Blue', 'hex': '#2962FF'}, {'name': 'Icy Violet Light', 'hex': '#B388FF'}, {'name': 'Cool Steel Blue', 'hex': '#37474F'},
            {'name': 'Cool Wine Burgundy', 'hex': '#880E4F'}, {'name': 'Cool Electric Pink', 'hex': '#FF007F'}, {'name': 'Pure Snow White', 'hex': '#FFFFFF'}
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
            {'name': 'Electric Fuchsia', 'hex': '#FF007F'}, {'name': 'Vibrant Sapphire', 'hex': '#0040FF'}, {'name': 'Pure Neon Yellow', 'hex': '#FFEA00'},
            {'name': 'Bright Emerald Green', 'hex': '#00E676'}, {'name': 'Crisp Pure White', 'hex': '#FFFFFF'}, {'name': 'Pure Jet Black', 'hex': '#000000'},
            {'name': 'Electric Violet', 'hex': '#651FFF'}, {'name': 'Vibrant Ruby Red', 'hex': '#FF1744'}, {'name': 'Bright Cyan Blue', 'hex': '#00E5FF'},
            {'name': 'Electric Magenta', 'hex': '#F50057'}, {'name': 'Vibrant Lime Green', 'hex': '#76FF03'}, {'name': 'Bright Royal Blue', 'hex': '#2962FF'},
            {'name': 'Electric Crimson', 'hex': '#D50000'}, {'name': 'Vibrant Aqua Blue', 'hex': '#18FFFF'}, {'name': 'Bright Canary Yellow', 'hex': '#FFFF00'},
            {'name': 'Electric Orchid Pink', 'hex': '#FF4081'}, {'name': 'Vibrant Teal Green', 'hex': '#00BFA5'}, {'name': 'Bright Cobalt Blue', 'hex': '#3D5AFE'},
            {'name': 'Electric Plum', 'hex': '#D500F9'}, {'name': 'Vibrant Chartreuse', 'hex': '#AEEA00'}, {'name': 'Bright Poppy Red', 'hex': '#FF3D00'},
            {'name': 'Electric Turquoise', 'hex': '#00E5FF'}, {'name': 'Vibrant Purple', 'hex': '#AA00FF'}, {'name': 'Bright Coral Pink', 'hex': '#FF5252'},
            {'name': 'Electric Indigo', 'hex': '#304FFE'}, {'name': 'Vibrant Mint Green', 'hex': '#69F0AE'}, {'name': 'Bright Marigold Yellow', 'hex': '#FFC400'},
            {'name': 'Electric Raspberry', 'hex': '#FF1744'}, {'name': 'Vibrant Ocean Blue', 'hex': '#00B0FF'}, {'name': 'Bright Violet Purple', 'hex': '#7C4DFF'},
            {'name': 'Electric Hot Pink', 'hex': '#FF0055'}, {'name': 'Vibrant Spring Green', 'hex': '#00E676'}, {'name': 'Bright Tangerine Orange', 'hex': '#FF6E40'},
            {'name': 'Electric Sapphire', 'hex': '#0033FF'}, {'name': 'Vibrant Icy Pink', 'hex': '#FF80AB'}, {'name': 'Crisp Polar White', 'hex': '#F8FAFC'}
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
    if not os.path.exists(image_path):
        return image_path
    try:
        img = Image.open(image_path)
        img = ImageOps.exif_transpose(img)
        cv_img = cv2.cvtColor(np.array(img.convert('RGB')), cv2.COLOR_RGB2BGR)
        _CASCADE_DIR = cv2.data.haarcascades
        _FACE_CASCADE = cv2.CascadeClassifier(_CASCADE_DIR + 'haarcascade_frontalface_default.xml')
        _EYE_CASCADE = cv2.CascadeClassifier(_CASCADE_DIR + 'haarcascade_eye.xml')
        best_angle = 0
        max_score = -1.0
        for angle in [0, 90, 180, 270]:
            if angle == 0: rotated = cv_img
            elif angle == 90: rotated = cv2.rotate(cv_img, cv2.ROTATE_90_CLOCKWISE)
            elif angle == 180: rotated = cv2.rotate(cv_img, cv2.ROTATE_180)
            elif angle == 270: rotated = cv2.rotate(cv_img, cv2.ROTATE_90_COUNTERCLOCKWISE)
            gray = cv2.cvtColor(rotated, cv2.COLOR_BGR2GRAY)
            gray_eq = cv2.equalizeHist(gray)
            faces = _FACE_CASCADE.detectMultiScale(gray_eq, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))
            if len(faces) > 0:
                largest_face = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)[0]
                fx, fy, fw, fh = largest_face
                roi_upper = gray_eq[fy:fy + int(fh * 0.55), fx:fx + fw]
                eyes = _EYE_CASCADE.detectMultiScale(roi_upper, scaleFactor=1.1, minNeighbors=4, minSize=(12, 12))
                score = (fw * fh) + (len(eyes) * 10000)
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
    except Exception as e:
        return image_path

def crop_face_only(image_path: str) -> str:
    if not os.path.exists(image_path):
        return image_path
    try:
        cv_img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        if cv_img is None: return image_path
        gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        _CASCADE_DIR = cv2.data.haarcascades
        _FACE_CASCADE = cv2.CascadeClassifier(_CASCADE_DIR + 'haarcascade_frontalface_default.xml')
        faces = _FACE_CASCADE.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))
        if len(faces) == 0: return image_path
        faces = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)
        (fx, fy, fw, fh) = faces[0]
        h_img, w_img = gray.shape[:2]
        crop_top = max(0, int(fy - fh * 0.45))
        crop_bottom = min(h_img, int(fy + fh * 1.25))
        crop_left = max(0, int(fx - fw * 0.25))
        crop_right = min(w_img, int(fx + fw * 1.25))
        cropped_cv = cv_img[crop_top:crop_bottom, crop_left:crop_right]
        out_dir = os.path.dirname(os.path.abspath(image_path))
        face_only_path = os.path.join(out_dir, '_face_only_' + os.path.basename(image_path))
        if not face_only_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            face_only_path += '.png'
        cv2.imwrite(face_only_path, cropped_cv)
        return face_only_path
    except Exception as e:
        return image_path

def generate_pdf(image_path: str, analysis_data: dict, output_pdf_path: str, client_name: str = 'Valued Client') -> str:
    image_path = ensure_upright_image(image_path)
    image_path = crop_face_only(image_path)
    
    try:
        from background_remover import remove_background
        temp_cutout = output_pdf_path.replace('.pdf', '_bg_cutout.png')
        remove_background(image_path, temp_cutout)
        if os.path.exists(temp_cutout) and os.path.getsize(temp_cutout) > 1000:
            image_path = temp_cutout
    except Exception as bg_err:
        pass
        
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
    
    edge_path = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
    if not os.path.exists(edge_path):
        edge_path = r'C:\Program Files\Microsoft\Edge\Application\msedge.exe'
        
    if os.path.exists(edge_path):
        try:
            temp_html = output_pdf_path.replace('.pdf', '_temp.html')
            with open(temp_html, 'w', encoding='utf-8') as f:
                f.write(html_out)
                
            html_url = 'file:///' + os.path.abspath(temp_html).replace('\\', '/')
            cmd = [
                edge_path,
                '--headless=new',
                f'--print-to-pdf={output_pdf_path}',
                '--no-pdf-header-footer',
                '--print-to-pdf-no-header',
                html_url
            ]
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if os.path.exists(temp_html):
                try: os.remove(temp_html)
                except: pass
                
            if os.path.exists(output_pdf_path) and os.path.getsize(output_pdf_path) > 1000:
                print(f'Generated pixel-perfect PDF via Headless Edge: {output_pdf_path}')
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
