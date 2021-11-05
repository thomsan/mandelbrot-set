import numpy as np
import colorsys
from numpy import newaxis

class MandelbrotRenderer:
    def __init__(self, width=1000, height =800, x=-0.5, y=0, zoom=1.0, max_iterations=1000, threshold_factor=0.1):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.zoom = zoom
        self.max_iterations = max_iterations
        self.threshold_factor = threshold_factor


    def zoom_in(self, factor=1.1):
        self.zoom *= factor


    def zoom_out(self, factor=1.1):
        self.zoom *= 1.0/factor


    def move_left(self, factor=0.001):
        self.x -= self.width*factor/self.zoom


    def move_right(self, factor=0.001):
        self.x += self.width*factor/self.zoom


    def move_up(self, factor=0.001):
        self.y -= self.height*factor/self.zoom


    def move_down(self, factor=0.001):
        self.y += self.height*factor/self.zoom


    def compute_mandelbrot(self):
        x_width = 1.5
        y_height = 1.5 * self.height/self.width
        x_min = self.x - x_width/self.zoom
        x_max = self.x + x_width/self.zoom
        y_min = self.y - y_height/self.zoom
        y_max = self.y + y_height/self.zoom

        x = np.linspace(x_min, x_max, self.width).reshape((1, self.width))
        y = np.linspace(y_min, y_max, self.height).reshape((self.height, 1))
        c = x + 1j * y

        z = np.zeros(c.shape, dtype=np.complex128)
        div_time = np.zeros(z.shape, dtype=int)
        m = np.full(c.shape, True, dtype=bool)

        for i in range(self.max_iterations):
            z[m] = z[m]**2 + c[m]

            diverged = np.greater(np.abs(z), 2, out=np.full(c.shape, False), where=m) # Find diverging

            div_time[diverged] = i
            m[np.abs(z) > 2] = False
        return div_time.T


    def DEPRECATED_get_image(self):
        image = np.ndarray(([self.size[0], self.size[1], 3]))
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                image[x][y] = self.get_pixel_value(x,y)

        image = (image * 255).astype(int)
        return image


    def DEPRECATED_get_pixel_value(self, p_x, p_y):
        # scale to mandelbrot scale x[-2.0, 0.47], y[-1.12, 1.12]
        x0 = np.interp(p_x, (0, self.size[0]), (self.x_min * self.zoom, self.x_max * self.zoom))
        y0 = np.interp(p_y, (0, self.size[1]), (self.y_min * self.zoom, self.y_max * self.zoom))
        i = 0
        x = 0
        y = 0

        while x*x + y*y <= 2*2 and i < self.max_iterations:
            x_n = x*x - y*y + x0
            y = 2*x*y + y0
            x = x_n
            i = i+1

        return self.get_color(i/self.max_iterations)


    def DEPRECATED_get_color(self, iteration_factor: float):
        if iteration_factor < self.threshold_factor:
            return (0,0,0)

        return colorsys.hsv_to_rgb(iteration_factor, 1.0, 1.0)
