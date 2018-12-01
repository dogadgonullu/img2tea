#!/bin/env python3

import argparse
from collections import defaultdict

from PIL import Image
import numpy as np

teas = {'chamomile': [212, 125, 31],
        'hibiscus': [124, 5, 22],
        'gunpowder': [191, 134, 59],
        'echinacea': [226, 157, 46],
        'cinnamon': [206, 10, 28],
        'turmeric': [242, 183, 44],
        'rose': [244, 147, 131],
        'lemon verbana': [202, 163, 62],
        'mallow': [64, 132, 129],
        'calendula': [169, 75, 19],
        'purple basil': [96, 45, 76],
        'lemongrass': [216, 208, 133],
        'jasmine blossom': [240, 212, 128]
        }

tea_gram = 2000


def read_image(filename: str) -> np.ndarray:
    im = Image.open(filename)
    arr = np.array(im)
    return arr


def get_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) + abs(p1[2] - p2[2])


def get_nearest_tea(pixel: list) -> str:
    best_distance = float('inf')
    best_tea = None

    for tea, tea_value in teas.items():
        distance = get_distance(tea_value, pixel)
        if distance < best_distance:
            best_tea = tea
            best_distance = distance

    return best_tea


def print_recipe(tea_list: list) -> str:
    """
    Converts the tea list into a recipe string
    """

    recipe = '\n'

    recipe_no = np.random.randint(100, 100000)

    recipe += 'Personalised tea mix #{}/\n\n'.format(recipe_no)
    recipe += 'You can find your personalised tea recipe below/\n'
    recipe += 'Please brew in 80°C/\n\n'
    recipe += 'For one tea bag/\n\n'

    for tea, value in tea_list:
        recipe += '\t{} mg {}\n'.format(value, tea)

    recipe += '\nMix and enjoy/\n\n'
    recipe += 'Designed by Doga D for Digital Media 12/2018\n\n'

    return recipe


def img2tea(filename: str) -> str:
    image = read_image(filename)

    current_teas = defaultdict(int)

    # Count nearest tea occurrences in image
    for row in range(image.shape[0]):
        for col in range(image.shape[1]):
            pixel = image[row, col]
            nearest_tea = get_nearest_tea(pixel)
            current_teas[nearest_tea] += 1

    # Count total tea
    total_tea_count = 0
    for count in current_teas.values():
        total_tea_count += count

    # Convert tea counts to mg
    for tea, count in current_teas.items():
        current_teas[tea] = count / total_tea_count * tea_gram

    # Sort teas based on their weight, highest first
    raw_tea_list = sorted(current_teas.items(), key=lambda kv: kv[1], reverse=True)

    # Round to integers and add to list if higher then 10 mgs
    rounded_tea_list = []
    for tea, mg in raw_tea_list:
        mg = int(mg)
        if mg >= 10:
            rounded_tea_list.append((tea, mg))

    return print_recipe(rounded_tea_list)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert images to tea recipes.')
    parser.add_argument('filename', type=str, help='file path for the image')
    args = parser.parse_args()
    recipe = img2tea(args.filename)
    print(recipe)
