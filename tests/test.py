from unittest import TestCase

from img2tea import img2tea, read_image, get_nearest_tea


class TestImg2Tea(TestCase):

    def test_read_jpg(self):
        im = read_image('images/rabby.jpg')
        self.assertEqual((407, 377, 3), im.shape)

    def test_read_png(self):
        im = read_image('images/apple.png')
        self.assertEqual((512, 512, 4), im.shape)

    def test_get_nearest_tea(self):
        pixel = [240, 180, 49]
        tea = get_nearest_tea(pixel)
        self.assertEqual('turmeric', tea)

    def test_img2tea(self):
        recipe = img2tea('images/rabby.jpg')
        print(recipe)
