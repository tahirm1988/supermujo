 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/super_mujo.py b/super_mujo.py
new file mode 100644
index 0000000000000000000000000000000000000000..2ffa82172d5ee8a0f55dfc0dced6292e6d20607f
--- /dev/null
+++ b/super_mujo.py
@@ -0,0 +1,355 @@
+"""Super Mujo - A small Bosnian themed platformer built with pygame.
+
+Run this module directly to play the game:
+
+    python super_mujo.py
+
+The controls are explained in the in-game intro screen.
+"""
+
+from __future__ import annotations
+
+import os
+from dataclasses import dataclass
+from typing import List, Tuple
+
+import pygame
+
+
+# Window settings
+WIDTH, HEIGHT = 960, 540
+FPS = 60
+
+
+# Colours
+SKY = (135, 206, 235)
+GROUND = (205, 133, 63)
+ROCK = (120, 110, 110)
+PLAYER = (13, 71, 161)
+GOAL = (255, 215, 0)
+TEXT = (20, 20, 20)
+UI_BG = (245, 245, 245)
+ITEM = (19, 141, 117)
+
+
+@dataclass
+class LevelData:
+    """Container for level specific configuration."""
+
+    name: str
+    flavour_text: str
+    tiles: List[str]
+    background_colour: Tuple[int, int, int]
+
+
+LEVELS: List[LevelData] = [
+    LevelData(
+        name="Baščaršija",
+        flavour_text="Pokupi kahvu i čevape prije nego što odeš na slijedeći trg!",
+        background_colour=(180, 220, 255),
+        tiles=[
+            "                                                G",
+            "                                                G",
+            "                                                G",
+            "                                                G",
+            "                                                G",
+            "                ####                           G",
+            "                #  #                           G",
+            "       K        #  #                           G",
+            "############  ######    ######       ####   ####",
+        ],
+    ),
+    LevelData(
+        name="Stari most",
+        flavour_text="Pređi most u Mostaru i sakupi suvenir stećak.",
+        background_colour=(170, 210, 240),
+        tiles=[
+            "                                           GGGGG",
+            "                                           GGGGG",
+            "             ######                         GGGGG",
+            "             #    #                         GGGGG",
+            "     K       #    ####                      GGGGG",
+            "##############       ######        ####   #######",
+        ],
+    ),
+    LevelData(
+        name="Planina Prenj",
+        flavour_text="Popni se na vrhove i uživaj u pogledima na Dinaride!",
+        background_colour=(150, 210, 200),
+        tiles=[
+            "                                           GGGGG",
+            "                                           GGGGG",
+            "   ####            ####         #######     GGGGG",
+            "   #  #            #  #         #     #     GGGGG",
+            "K  #  ####     #####  ####      #     ####  GGGGG",
+            "############  ############################  #####",
+        ],
+    ),
+]
+
+
+TILE_SIZE = 60
+
+
+class Player(pygame.sprite.Sprite):
+    def __init__(self, pos: Tuple[int, int]) -> None:
+        super().__init__()
+        self.image = pygame.Surface((40, 60))
+        self.image.fill(PLAYER)
+        self.rect = self.image.get_rect(topleft=pos)
+        self.vel = pygame.math.Vector2(0, 0)
+        self.on_ground = False
+
+    def update(self, keys: pygame.key.ScancodeWrapper, platforms: pygame.sprite.Group) -> None:
+        self._handle_movement(keys)
+        self._apply_gravity()
+        self._collide(platforms)
+
+    def _handle_movement(self, keys: pygame.key.ScancodeWrapper) -> None:
+        speed = 5
+        self.vel.x = 0
+        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
+            self.vel.x = -speed
+        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
+            self.vel.x = speed
+        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.on_ground:
+            self.vel.y = -14
+            self.on_ground = False
+
+    def _apply_gravity(self) -> None:
+        gravity = 0.7
+        self.vel.y += gravity
+        if self.vel.y > 18:
+            self.vel.y = 18
+        self.rect.x += int(self.vel.x)
+        self.rect.y += int(self.vel.y)
+
+    def _collide(self, platforms: pygame.sprite.Group) -> None:
+        self.on_ground = False
+        for tile in platforms:
+            if self.rect.colliderect(tile.rect):
+                if self.vel.y > 0 and self.rect.bottom >= tile.rect.top:
+                    self.rect.bottom = tile.rect.top
+                    self.vel.y = 0
+                    self.on_ground = True
+                elif self.vel.y < 0 and self.rect.top <= tile.rect.bottom:
+                    self.rect.top = tile.rect.bottom
+                    self.vel.y = 0
+                elif self.vel.x > 0 and self.rect.right >= tile.rect.left:
+                    self.rect.right = tile.rect.left
+                elif self.vel.x < 0 and self.rect.left <= tile.rect.right:
+                    self.rect.left = tile.rect.right
+
+
+class Tile(pygame.sprite.Sprite):
+    def __init__(self, pos: Tuple[int, int], height: int = TILE_SIZE) -> None:
+        super().__init__()
+        self.image = pygame.Surface((TILE_SIZE, height))
+        self.image.fill(GROUND)
+        self.rect = self.image.get_rect(topleft=pos)
+
+
+class Rock(pygame.sprite.Sprite):
+    def __init__(self, pos: Tuple[int, int], width: int = TILE_SIZE, height: int = TILE_SIZE) -> None:
+        super().__init__()
+        self.image = pygame.Surface((width, height))
+        self.image.fill(ROCK)
+        self.rect = self.image.get_rect(topleft=pos)
+
+
+class Goal(pygame.sprite.Sprite):
+    def __init__(self, pos: Tuple[int, int]) -> None:
+        super().__init__()
+        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
+        self.image.fill(GOAL)
+        self.rect = self.image.get_rect(topleft=pos)
+
+
+class Item(pygame.sprite.Sprite):
+    def __init__(self, pos: Tuple[int, int], label: str) -> None:
+        super().__init__()
+        self.image = pygame.Surface((36, 36))
+        self.image.fill(ITEM)
+        self.rect = self.image.get_rect(center=(pos[0] + TILE_SIZE // 2, pos[1] + TILE_SIZE // 2))
+        self.label = label
+
+
+class Level:
+    def __init__(self, data: LevelData, font: pygame.font.Font) -> None:
+        self.data = data
+        self.platforms = pygame.sprite.Group()
+        self.goal = pygame.sprite.GroupSingle()
+        self.items = pygame.sprite.Group()
+        self.decor = pygame.sprite.Group()
+        self.player_start = (40, HEIGHT - TILE_SIZE * 2)
+        self.font = font
+        self._build()
+
+    def _build(self) -> None:
+        flavour_items = ["kahvu", "čevape", "suvenir", "bosansku kahvu"]
+        item_index = 0
+        for y, row in enumerate(self.data.tiles):
+            for x, char in enumerate(row):
+                world_x = x * TILE_SIZE
+                world_y = HEIGHT - (len(self.data.tiles) - y) * TILE_SIZE
+                if char == "#":
+                    tile = Tile((world_x, world_y))
+                    self.platforms.add(tile)
+                elif char == "G":
+                    rock = Rock((world_x, world_y + TILE_SIZE // 2), height=TILE_SIZE // 2)
+                    self.platforms.add(rock)
+                elif char == "K":
+                    if item_index < len(flavour_items):
+                        label = flavour_items[item_index]
+                    else:
+                        label = "poslasticu"
+                    item_index += 1
+                    item = Item((world_x, world_y), label)
+                    self.items.add(item)
+                elif char == " ":
+                    continue
+        if self.platforms:
+            last_tile = max(self.platforms, key=lambda t: t.rect.x)
+            goal_pos = (last_tile.rect.right + 40, last_tile.rect.top - TILE_SIZE)
+        else:
+            goal_pos = (WIDTH - TILE_SIZE * 2, HEIGHT - TILE_SIZE * 3)
+        self.goal.add(Goal(goal_pos))
+
+    def draw(self, surface: pygame.Surface, player: Player) -> None:
+        surface.fill(self.data.background_colour)
+        self.platforms.draw(surface)
+        self.goal.draw(surface)
+        self.items.draw(surface)
+        surface.blit(player.image, player.rect)
+
+    def draw_ui(self, surface: pygame.Surface, collected: List[str]) -> None:
+        panel = pygame.Surface((WIDTH, 90), pygame.SRCALPHA)
+        panel.fill((*UI_BG, 200))
+        surface.blit(panel, (0, 0))
+        title = self.font.render(f"{self.data.name} - Super Mujo", True, TEXT)
+        surface.blit(title, (20, 10))
+        flavour = self.font.render(self.data.flavour_text, True, TEXT)
+        surface.blit(flavour, (20, 40))
+        if collected:
+            collected_text = ", ".join(collected)
+            collected_surface = self.font.render(f"Skupljeno: {collected_text}", True, TEXT)
+            surface.blit(collected_surface, (20, 65))
+
+
+def show_intro(screen: pygame.Surface, font: pygame.font.Font) -> None:
+    clock = pygame.time.Clock()
+    intro_lines = [
+        "Dobrodošao u Super Muja!",
+        "Kreći se sa strelicama ili A/D.",
+        "Skoči sa SPACE ili strelicom gore.",
+        "Pokupi specijalitete i dođi do zlatnog cilja.",
+        "Pritisni bilo koju tipku da kreneš u avanturu!",
+    ]
+    waiting = True
+    while waiting:
+        for event in pygame.event.get():
+            if event.type == pygame.QUIT:
+                pygame.quit()
+                raise SystemExit
+            if event.type == pygame.KEYDOWN:
+                waiting = False
+        screen.fill(SKY)
+        for idx, line in enumerate(intro_lines):
+            text = font.render(line, True, TEXT)
+            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 160 + idx * 40))
+        pygame.display.flip()
+        clock.tick(FPS)
+
+
+def show_outro(screen: pygame.Surface, font: pygame.font.Font) -> None:
+    clock = pygame.time.Clock()
+    outro_lines = [
+        "Svaka čast, Mujo!",
+        "Prošao si kroz Bosnu i donio osmijeh u svako selo.",
+        "Pritisni ESC za izlaz ili R za novu avanturu.",
+    ]
+    while True:
+        for event in pygame.event.get():
+            if event.type == pygame.QUIT:
+                pygame.quit()
+                raise SystemExit
+            if event.type == pygame.KEYDOWN:
+                if event.key == pygame.K_ESCAPE:
+                    pygame.quit()
+                    raise SystemExit
+                if event.key == pygame.K_r:
+                    return
+        screen.fill((120, 180, 200))
+        for idx, line in enumerate(outro_lines):
+            text = font.render(line, True, TEXT)
+            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 180 + idx * 45))
+        pygame.display.flip()
+        clock.tick(FPS)
+
+
+def play_level(
+    screen: pygame.Surface, clock: pygame.time.Clock, font: pygame.font.Font, data: LevelData
+) -> bool:
+    level = Level(data, font)
+    player = Player(level.player_start)
+    collected: List[str] = []
+    running = True
+    while running:
+        for event in pygame.event.get():
+            if event.type == pygame.QUIT:
+                pygame.quit()
+                raise SystemExit
+
+        keys = pygame.key.get_pressed()
+        player.update(keys, level.platforms)
+
+        if player.rect.top > HEIGHT:
+            return False
+
+        for item in pygame.sprite.spritecollide(player, level.items, dokill=True):
+            collected.append(item.label)
+
+        if pygame.sprite.spritecollide(player, level.goal, dokill=False):
+            return True
+
+        level.draw(screen, player)
+        level.draw_ui(screen, collected)
+        pygame.display.flip()
+        clock.tick(FPS)
+
+
+def run() -> None:
+    os.environ.setdefault("SDL_VIDEO_CENTERED", "1")
+    pygame.init()
+    screen = pygame.display.set_mode((WIDTH, HEIGHT))
+    pygame.display.set_caption("Super Mujo")
+    clock = pygame.time.Clock()
+    font = pygame.font.SysFont("freesansbold", 24)
+
+    show_intro(screen, font)
+
+    current_level = 0
+    while True:
+        success = play_level(screen, clock, font, LEVELS[current_level])
+        if success:
+            current_level = (current_level + 1) % len(LEVELS)
+            if current_level == 0:
+                show_outro(screen, font)
+        else:
+            screen.fill((240, 120, 120))
+            fail_text = font.render("Ups! Mujo je pao. Pritisni R za pokušaj ponovo.", True, TEXT)
+            screen.blit(fail_text, (WIDTH // 2 - fail_text.get_width() // 2, HEIGHT // 2))
+            pygame.display.flip()
+            waiting = True
+            while waiting:
+                for event in pygame.event.get():
+                    if event.type == pygame.QUIT:
+                        pygame.quit()
+                        raise SystemExit
+                    if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
+                        waiting = False
+
+
+if __name__ == "__main__":
+    run()
+
 
EOF
)
