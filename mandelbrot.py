import math
import numpy as np
import colorsys
import matplotlib
import matplotlib.pyplot as plt


def mag(z):
    return math.sqrt(z.real**2 + z.imag**2)


def mapRange(x, from_min, from_max, to_min, to_max):
    ratio = (x - from_min) / (from_max - from_min)
    return to_min + (ratio * (to_max - to_min))


class Mandelbrot:
    def __init__(self, max_mag, n_iter):
        self.max_mag = max_mag
        self.n_iter = n_iter

    def isMember(self, c):
        z = complex(0, 0)
        for i in range(self.n_iter):
            if mag(z) > self.max_mag:
                # Diverged
                return (False, i)
            z = z**2 + c
        return (True, i)

    def genImage(self, limits, img_width=400, img_height=300):
        img = np.zeros((img_height, img_width, 3))
        for i in range(img_height):
            for j in range(img_width):
                x = j / img_width * (limits[2] - limits[0]) + limits[0]
                y = i / img_height * (limits[3] - limits[1]) + limits[1]
                c = complex(x, y)
                is_member, iters = self.isMember(c)
                if is_member:
                    img[i, j, :] = np.array([0, 0, 0])
                else:
                    h = iters / self.n_iter
                    img[i, j, :] = np.array(colorsys.hsv_to_rgb(h, 1, 0.9))
        return img

    def genImageFaster(self, limits, img_width=400, img_height=300):
        iters = np.zeros((img_height, img_width))
        z = np.zeros((img_height, img_width), dtype=complex)

        c_real = np.mgrid[0:img_height, 0:img_width][1]
        c_real = (c_real * (limits[2] - limits[0]) / img_width) + limits[0]

        c_img = np.mgrid[0:img_height, 0:img_width][0]
        c_img = (c_img * (limits[3] - limits[1]) / img_height) + limits[1]

        c = c_real + c_img * complex(0, 1)

        for i in range(self.n_iter):
            z = z ** 2 + c
            mag = np.sqrt(z.real ** 2 + z.imag ** 2)
            iters[np.where(mag < self.max_mag)
                  ] = iters[np.where(mag < self.max_mag)] + 1

        hue = iters / self.n_iter
        saturation = np.ones((img_height, img_width))
        brightness = np.ones((img_height, img_width))

        brightness[np.where(iters == self.n_iter)] = 0

        img = np.dstack(
            [
                iters / self.n_iter,
                saturation,
                brightness
            ]
        )

        img = matplotlib.colors.hsv_to_rgb(img)

        return img
