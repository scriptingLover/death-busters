import pygame
import random
import sys
import time

pygame.init()

screen_width = 1000
screen_height = 850
screen = pygame.display.set_mode((screen_width, screen_height))
currentmode = "Non AFK"
pygame.display.set_caption(f"Death Busters ({currentmode})")

font = pygame.font.Font(None, 36)

background_img = pygame.image.load("grassbg.png").convert()
background_img = pygame.transform.scale(background_img, (screen_width, screen_height))

class Humanoid:
    def __init__(self, name: str, img_path: str):
        self.original_img = pygame.image.load(img_path).convert_alpha()
        self.name = name
        self.processed_img = self.process_image()
        self.size = max(self.processed_img.get_width(), self.processed_img.get_height())
        self.x = (screen_width - self.size) // 2
        self.y = (screen_height - self.size) // 2

    def process_image(self):
        processed_img = self.original_img.copy()
        for x in range(processed_img.get_width()):
            for y in range(processed_img.get_height()):
                pixel_color = processed_img.get_at((x, y))
                if pixel_color == (255, 255, 255, 255):
                    fill_color = (255, 255, 255, 0)
                    processed_img.set_at((x, y), fill_color)
        return processed_img

    def draw(self):
        humanoid_surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        humanoid_surface.blit(self.processed_img, (0, 0))

        text = font.render(self.name, True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.size // 2, self.size // 2))
        humanoid_surface.blit(text, text_rect)

        screen.blit(humanoid_surface, (self.x, self.y))


class Tool:
    def __init__(self, holder: Humanoid, img_path: str):
        self.holder = holder
        self.original_img = pygame.image.load(img_path).convert_alpha()
        self.processed_img = self.process_image()

    def process_image(self):
        processed_img = self.original_img.copy()
        for x in range(processed_img.get_width()):
            for y in range(processed_img.get_height()):
                pixel_color = processed_img.get_at((x, y))
                if pixel_color == (255, 255, 255, 255):
                    fill_color = (255, 255, 255, 0)
                    processed_img.set_at((x, y), fill_color)
        return processed_img

    def draw(self):
        tool_surface = pygame.Surface((self.holder.size, self.holder.size), pygame.SRCALPHA)
        resized_img = pygame.transform.scale(self.processed_img, (self.holder.size, self.holder.size))
        tool_surface.blit(resized_img, (4.5, -1))

        screen.blit(tool_surface, (self.holder.x, self.holder.y))


class Enemy(Humanoid):
    def __init__(self, name: str, img_path: str):
        super().__init__(name, img_path)
        self.direction = random.choice(["LEFT", "RIGHT", "UP", "DOWN"])
        self.speed = 2
        self.last_change_time = time.time()
        self.change_interval = 0.5

    def move(self):
        elapsed_time = time.time() - self.last_change_time
        if elapsed_time >= self.change_interval:
            self.direction = random.choice(["LEFT", "RIGHT", "UP", "DOWN"])
            self.last_change_time = time.time()

        if self.direction == "LEFT":
            self.x -= self.speed
        elif self.direction == "RIGHT":
            self.x += self.speed
        elif self.direction == "UP":
            self.y -= self.speed
        elif self.direction == "DOWN":
            self.y += self.speed


class Game:
    def __init__(self):
        enemies = ["Runner",
                  "Juggernaut"]
        rand_enemy = random.choice(enemies)

        if rand_enemy == "Runner":
            self.enemy = Enemy(rand_enemy, "./enemy_crops/crop_runner.png")
        elif rand_enemy == "Juggernaut":
            self.enemy = Enemy(rand_enemy, "./enemy_crops/crop_juggernaut.png")

        self.player = Humanoid("You", "./player_crops/crop_player_red.png")
        self.tool = Tool(self.player, "sword.png")
        self.clock = pygame.time.Clock()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def handle_movement_player(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.x -= 5
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.x += 5
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.player.y -= 5
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.player.y += 5

    def run(self):
        running = True
        while running:
            self.handle_events()
            self.handle_movement_player()
            self.enemy.move()

            screen.blit(background_img, (0, 0))

            self.player.draw()
            self.enemy.draw()
            self.tool.draw()
            pygame.display.flip()

            self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.run()