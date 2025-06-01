import pygame
import math
import time
import cv2
import numpy as np

amplitude_base = 20.0
frequency_base = 10.0

def run_wave_animation(evolutive=True, image_queue=None):
    global amplitude_base, frequency_base

    pygame.init()
    screen_width, screen_height = 1280, 960
    render_width, render_height = 320, 240
    pygame.display.set_caption("🌊")
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    start_time = time.time()

    def wave_height_at(x, y, t, iterations):
        if y == 0:
            return 0
        wave_height = math.cos(x * y) * max(0, t - 8)
        for i in range(int(iterations)):
            amplitude = amplitude_base / 40.0
            frequency = frequency_base * (2.0 + math.cos(i))
            phase = math.cos(i * i)
            dx = math.sin(i * i)
            dy = math.cos(i * i * i)
            time_shift = t / 14.0 * iterations
            nx = x / 2.0 / y
            ny = 160 * 2.0 / y
            wave_height -= amplitude * abs(math.sin(frequency * (ny * dy + nx * dx) + time_shift + phase))
        return wave_height

    running = True
    while running:
        t = time.time() - start_time

        render_surface = pygame.Surface((render_width, render_height))
        render_surface.fill((0, 0, 0))

        for fx in range(render_width):
            prev_wave_height = 0
            for fy in range(render_height):
                vp_x, vp_y = render_width / 2, render_height / 2
                d = 160
                cx = vp_x - fx
                cy = vp_y - fy
                if cy == 0:
                    continue
                dist = math.sqrt(cx ** 2 + cy ** 2)

                iterations = 2 if fy < render_height / 2 else 6
                wave_height = wave_height_at(fx, fy, t if evolutive else 4, iterations)
                wave_scale = min(2 * (t if evolutive else 4), 40)
                perspective_height = wave_height * wave_scale * cy / d

                if evolutive:
                    radius = min(2 * t - 7, 50)
                    blob_color = dist / radius if radius > 0 else 0
                    color_val = blob_color if dist < radius else 1.0 - abs(perspective_height - prev_wave_height) / 6.0
                else:
                    color_val = 1.0 - abs(perspective_height - prev_wave_height) / 6.0

                p_color = max(0.0, min(1.0, color_val + (cy - dist) / 512.0))
                shade = int(255 * p_color)

                y1 = int(fy + perspective_height)
                y2 = int(fy + prev_wave_height)
                pygame.draw.line(render_surface, (shade, shade, shade), (fx, y1), (fx, y2))
                prev_wave_height = perspective_height

        scaled_surface = pygame.transform.scale(render_surface, (screen_width, screen_height))
        screen.blit(scaled_surface, (0, 0))

        if image_queue:
            try:
                image = image_queue.get_nowait()
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                surf = pygame.surfarray.make_surface(image.swapaxes(0, 1))
                surf = pygame.transform.scale(surf, (320, 240))
                screen.blit(surf, (screen_width - 240, 0))
            except:
                pass

        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
