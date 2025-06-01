import pygame
import math
import time

pygame.init()
screen_width, screen_height = 320, 240
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

start_time = time.time()

def wave_height_at(x, y, t, iterations):
    if y == 0:
        return 0
    wave_height = math.cos(x * y) * max(0, t - 8)
    for i in range(int(iterations)):
        amplitude = i / 40.0
        frequency = 2.0 + math.cos(i)
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
    screen.fill((0, 0, 0))

    for fx in range(screen_width):
        prev_wave_height = 0
        for fy in range(screen_height):
            vp_x, vp_y = 160, 120.5
            d = 160
            cx = vp_x - fx
            cy = vp_y - fy
            if cy == 0:
                continue
            nx = cx / 2.0 / cy
            ny = d * 2.0 / cy
            dist = math.sqrt(cx ** 2 + cy ** 2)

            iterations = 4 if fy < 120 else 16
            wave_height = wave_height_at(fx, fy, t, iterations)
            wave_scale = min(2 * t, 40)
            perspective_height = wave_height * wave_scale * cy / d

            # Blob/ship in the middle
            radius = min(2 * t - 7, 50)
            blob_color = dist / radius if radius > 0 else 0
            h_color = 1.0 - abs(perspective_height - prev_wave_height) / 6.0
            color_val = blob_color if dist < radius else h_color
            p_color = max(0.0, min(1.0, color_val + (cy - dist) / 512.0))
            shade = int(255 * p_color)

            # Draw vertical line
            y1 = int(fy + perspective_height)
            y2 = int(fy + prev_wave_height)
            pygame.draw.line(screen, (shade, shade, shade), (fx, y1), (fx, y2))
            prev_wave_height = perspective_height

    pygame.display.flip()
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
