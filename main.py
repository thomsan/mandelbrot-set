import sys

import numpy as np
import pygame as pg
from matplotlib import cm

from mandelbrot_renderer import MandelbrotRenderer


class MandelbrotVisualizer:
    def __init__(self, screen_width=1000, screen_height=800, render_scale=1.0, max_iterations=100):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.render_scale = render_scale
        pg.init()
        pg.display.set_caption('Mandelbrot Set')
        self.screen = pg.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pg.time.Clock()
        self.renderer = MandelbrotRenderer(width=((int) (screen_width*render_scale)), height=((int) (screen_height*render_scale)), max_iterations=max_iterations)
        self.stopped = False
        self.update_image()
        self.render_loop()


    def render_loop(self):
        while not self.stopped:
            self.clock.tick(60)

            for event in pg.event.get():
                keys = pg.key.get_pressed()
                if keys[pg.K_o]:
                    self.renderer.zoom_out()
                if keys[pg.K_i]:
                    self.renderer.zoom_in()
                if keys[pg.K_w]:
                    self.renderer.move_up()
                if keys[pg.K_s]:
                    self.renderer.move_down()
                if keys[pg.K_d]:
                    self.renderer.move_right()
                if keys[pg.K_a]:
                    self.renderer.move_left()
                self.update_image()

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.stopped = True

            self.screen.fill((0, 0, 0))
            self.screen.blit(self.surface, (0, 0))

            pg.display.update()

        pg.quit()
        quit()


    def update_image(self):
        self.image = self.renderer.compute_mandelbrot() * 10
        #colmap = cm.get_cmap('viridis', np.max(self.image) + 1)
        #lut = (colmap.colors[...,0:3]*255).astype(np.uint8)
        #result = np.zeros((*self.image.shape,3), dtype=np.uint8)
        #np.take(lut, self.image, axis=0, out=self.image)
        self.surface = pg.Surface((self.renderer.width, self.renderer.height))
        pg.surfarray.blit_array(self.surface, self.image)
        self.surface = pg.transform.scale(self.surface, (self.screen_width, self.screen_height))
        self.screen.blit(self.surface, (0,0))


if __name__ == "__main__":
    visualizer = MandelbrotVisualizer(render_scale=0.2, max_iterations=50)
