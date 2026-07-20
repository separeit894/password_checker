import os

from PIL import Image
from core import checking_exe_or_code

# Turn off the labels ( not necessarily ) "pygame 2.x.x"
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame


def load_gif():
    gif_path = checking_exe_or_code()
    if gif_path.exists():
        print("GIF file found!")

        # init pygame
        pygame.init()
        pygame.display.set_caption("Как отключить ограничитель попыток")

        # open GIF with Pillow
        gif = Image.open(gif_path)

        # Recruitment
        frames = []
        try:
            while True:
                frames.append(gif.copy())
                gif.seek(gif.tell() + 1)
        except EOFError:
            pass

        # Configuration Window
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

            # Show current frame
            screen.fill((0, 0, 0))  # Clean Window
            frame = frames[frame_index]
            frame = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
            screen.blit(frame, (0, 0))
            pygame.display.flip()

            # transition to next frame
            frame_index = (frame_index + 1) % len(frames)
            clock.tick(
                gif.info["duration"] // 10
            )  # Apply the final time between frames.

        pygame.quit()
    else:
        print("GIF file not found.")


if __name__ == "__main__":
    load_gif()
