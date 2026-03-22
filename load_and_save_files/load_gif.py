import os

from PIL import Image
from core import checking_exe_or_code

# Отключаем надписи "pygame 2.x.x и т.д."
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame


def load_gif():
    gif_path = checking_exe_or_code()
    if gif_path.exists():
        print("GIF файл найден!")

        # Инициализация pygame
        pygame.init()
        pygame.display.set_caption("Как отключить ограничитель попыток")

        # Открытие GIF с помощью Pillow
        gif = Image.open(gif_path)

        # Получение кадров
        frames = []
        try:
            while True:
                frames.append(gif.copy())
                gif.seek(gif.tell() + 1)
        except EOFError:
            pass

        # Настройка окна
        screen = pygame.display.set_mode(
            (gif.width, gif.height), pygame.SCALED | pygame.RESIZABLE
        )

        clock = pygame.time.Clock()
        running = True
        frame_index = 0

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Отображение текущего кадра
            screen.fill((0, 0, 0))  # Очистка экрана
            frame = frames[frame_index]
            frame = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
            screen.blit(frame, (0, 0))
            pygame.display.flip()

            # Переход к следующему кадру
            frame_index = (frame_index + 1) % len(frames)
            clock.tick(
                gif.info["duration"] // 10
            )  # Примените окончательное время между кадрами

        pygame.quit()
    else:
        print("GIF файл не найден.")


if __name__ == "__main__":
    load_gif()
