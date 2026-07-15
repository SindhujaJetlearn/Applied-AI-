import pygame
import random
import sys
import math

# Initialize pygame and mixer
pygame.init()
pygame.mixer.init()

# Screen dimensions
WIDTH = 800
HEIGHT = 400

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 50, 0)
RED = (255, 0, 0)
BLUE = (0, 150, 255)
YELLOW = (255, 255, 0)

# Setup the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Endless Runner - Ultimate Realistic Radium Edition")

# Clock for controlling frame rate
clock = pygame.time.Clock()
FPS = 60

# Load Sounds
try:
    jump_sound = pygame.mixer.Sound("jump.wav")
    powerup_sound = pygame.mixer.Sound("powerup.wav")
    crash_sound = pygame.mixer.Sound("crash.wav")
    pygame.mixer.music.load("music.wav")
    pygame.mixer.music.play(-1) # Loop forever
    jump_sound.set_volume(0.3)
    powerup_sound.set_volume(0.5)
    crash_sound.set_volume(0.5)
    pygame.mixer.music.set_volume(0.4)
except pygame.error:
    print("Warning: Could not load sound files.")
    jump_sound = None
    powerup_sound = None
    crash_sound = None

def load_image(path, size, fallback_color):
    try:
        img = pygame.image.load(path).convert_alpha()
        img = pygame.transform.scale(img, size)
        img.set_colorkey(BLACK) # Remove black background for transparency
        return img
    except FileNotFoundError:
        surf = pygame.Surface(size, pygame.SRCALPHA)
        surf.fill(fallback_color)
        return surf

# Load images
player_image = load_image("player.png", (50, 50), GREEN)

obstacle_images = [
    load_image("obstacle.png", (40, 50), RED),    # Spike
    load_image("obstacle2.png", (40, 40), RED),   # 3D Cube
    load_image("obstacle3.png", (50, 50), RED)    # Saw blade
]

try:
    bg_image = pygame.image.load("bg.png").convert()
    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
except FileNotFoundError:
    bg_image = pygame.Surface((WIDTH, HEIGHT))
    bg_image.fill(BLACK)

# Game variables
gravity = 0.6
base_speed = 6
score = 0
game_active = True
bg_scroll = 0

# Powerup states
invincible_timer = 0
speed_timer = 0
multiplier_timer = 0

# Fonts
font = pygame.font.Font(None, 36)

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-2, -5)
        self.vy = random.uniform(-1, -4)
        self.lifetime = random.randint(10, 20)
        self.color = color

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.2 # gravity on particle
        self.lifetime -= 1

    def draw(self, surface):
        if self.lifetime > 0:
            size = self.lifetime // 4
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), size)

# Player class
class Player:
    def __init__(self):
        self.original_image = player_image
        self.image = player_image
        self.rect = self.image.get_rect(bottomleft=(50, HEIGHT - 50))
        self.y_velocity = 0
        self.is_jumping = False
        self.base_y = HEIGHT - 50
        self.animation_timer = 0
        self.particles = []

    def jump(self):
        if not self.is_jumping:
            self.y_velocity = -10 # Base jump
            self.is_jumping = True
            if jump_sound:
                jump_sound.play()
            
            # Jump particles
            for _ in range(10):
                self.particles.append(Particle(self.rect.centerx, self.rect.bottom, GREEN))

    def apply_gravity(self, space_held):
        # Variable jump height: less gravity if holding space while moving up
        current_gravity = gravity
        if space_held and self.y_velocity < 0:
            current_gravity = gravity * 0.5
            
        self.y_velocity += current_gravity
        self.rect.y += self.y_velocity

        if self.rect.bottom >= self.base_y:
            self.rect.bottom = self.base_y
            self.is_jumping = False
            self.y_velocity = 0
            
        # Running particles
        if not self.is_jumping and game_active and random.random() < 0.3:
            self.particles.append(Particle(self.rect.centerx - 10, self.rect.bottom, GREEN))

    def animate(self):
        if not self.is_jumping:
            speed_mult = 1.5 if speed_timer > 0 else 1.0
            self.animation_timer += 0.2 * speed_mult
            angle = math.sin(self.animation_timer) * 15 
            self.image = pygame.transform.rotate(self.original_image, angle)
            center = self.rect.center
            self.rect = self.image.get_rect(center=center)
            self.rect.bottom = self.base_y
        else:
            self.image = pygame.transform.rotate(self.original_image, 10) 
            center = self.rect.center
            self.rect = self.image.get_rect(center=center)

    def draw(self, surface):
        self.animate()
        
        # Draw particles
        for p in self.particles:
            p.update()
            p.draw(surface)
        self.particles = [p for p in self.particles if p.lifetime > 0]
        
        # Shadow
        shadow_width = max(10, 50 - int((self.base_y - self.rect.bottom) / 2.5))
        shadow_rect = pygame.Rect(0, 0, shadow_width, 10)
        shadow_rect.center = (self.rect.centerx, self.base_y + 5)
        shadow_surf = pygame.Surface((shadow_width, 10), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surf, (0, 100, 0, 150), shadow_surf.get_rect())
        surface.blit(shadow_surf, shadow_rect)
        
        # Invincibility shield effect
        if invincible_timer > 0:
            shield_radius = 35 + math.sin(pygame.time.get_ticks() / 100.0) * 5
            pygame.draw.circle(surface, BLUE, self.rect.center, int(shield_radius), 3)
            
        surface.blit(self.image, self.rect)

class Obstacle:
    def __init__(self):
        self.image = random.choice(obstacle_images)
        self.rect = self.image.get_rect(bottomleft=(WIDTH + random.randint(0, 100), HEIGHT - 50))
        self.base_y = HEIGHT - 50

    def update(self, speed):
        self.rect.x -= speed

    def draw(self, surface):
        shadow_width = self.rect.width
        shadow_rect = pygame.Rect(0, 0, shadow_width, 10)
        shadow_rect.center = (self.rect.centerx, self.base_y + 5)
        shadow_surf = pygame.Surface((shadow_width, 10), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surf, (100, 0, 0, 150), shadow_surf.get_rect())
        surface.blit(shadow_surf, shadow_rect)
        
        surface.blit(self.image, self.rect)

class Powerup:
    def __init__(self):
        self.type = random.choice(['shield', 'speed', 'multiplier'])
        self.rect = pygame.Rect(WIDTH + 50, HEIGHT - 150, 30, 30)
        self.base_y = HEIGHT - 150
        
    def update(self, speed):
        self.rect.x -= speed
        # Hover effect
        self.rect.y = self.base_y + math.sin(pygame.time.get_ticks() / 150.0) * 10
        
    def draw(self, surface):
        color = BLUE if self.type == 'shield' else (WHITE if self.type == 'speed' else YELLOW)
        # Draw glowing orb
        pygame.draw.circle(surface, color, self.rect.center, 15)
        pygame.draw.circle(surface, WHITE, self.rect.center, 8)

# Create instances
player = Player()
obstacles = []
powerups = []

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

powerup_timer = pygame.USEREVENT + 2
pygame.time.set_timer(powerup_timer, 5000)

def display_ui():
    score_surface = font.render(f'Score: {int(score)}', True, GREEN)
    screen.blit(score_surface, (10, 10))
    
    y_offset = 40
    if invincible_timer > 0:
        t = font.render(f'Shield: {invincible_timer/60:.1f}s', True, BLUE)
        screen.blit(t, (10, y_offset))
        y_offset += 30
    if speed_timer > 0:
        t = font.render(f'Super Speed: {speed_timer/60:.1f}s', True, WHITE)
        screen.blit(t, (10, y_offset))
        y_offset += 30
    if multiplier_timer > 0:
        t = font.render(f'3x Multiplier: {multiplier_timer/60:.1f}s', True, YELLOW)
        screen.blit(t, (10, y_offset))

def draw_background(surface, scroll):
    bg_x = scroll % WIDTH
    surface.blit(bg_image, (bg_x - WIDTH, 0))
    surface.blit(bg_image, (bg_x, 0))

# Main game loop
while True:
    space_held = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        space_held = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()
            
            if event.type == obstacle_timer:
                obstacles.append(Obstacle())
                time = random.randint(1000, 2000)
                if speed_timer > 0:
                    time = int(time * 0.7)
                pygame.time.set_timer(obstacle_timer, time)
                
            if event.type == powerup_timer:
                if random.random() < 0.6: # 60% chance to actually spawn a powerup every 5-10s
                    powerups.append(Powerup())
                pygame.time.set_timer(powerup_timer, random.randint(5000, 10000))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                obstacles.clear()
                powerups.clear()
                player.rect.bottom = HEIGHT - 50
                player.particles.clear()
                score = 0
                bg_scroll = 0
                invincible_timer = 0
                speed_timer = 0
                multiplier_timer = 0
                if pygame.mixer.get_init() and not pygame.mixer.music.get_busy():
                    pygame.mixer.music.play(-1)

    if game_active:
        # Update timers
        if invincible_timer > 0: invincible_timer -= 1
        if speed_timer > 0: speed_timer -= 1
        if multiplier_timer > 0: multiplier_timer -= 1

        current_speed = base_speed * 1.5 if speed_timer > 0 else base_speed

        bg_scroll -= current_speed * 0.3
        draw_background(screen, bg_scroll)

        player.apply_gravity(space_held)
        player.draw(screen)
        
        # Powerups
        for p in powerups:
            p.update(current_speed)
            p.draw(screen)
            if player.rect.colliderect(p.rect):
                if powerup_sound: powerup_sound.play()
                if p.type == 'shield': invincible_timer = 60 * 5 # 5 seconds
                elif p.type == 'speed': speed_timer = 60 * 5
                elif p.type == 'multiplier': multiplier_timer = 60 * 5
                p.rect.x = -100 # mark for removal

        powerups = [p for p in powerups if p.rect.right > 0]

        # Obstacles
        for obstacle in obstacles:
            obstacle.update(current_speed)
            obstacle.draw(screen)
            
            hitbox_offset_x = 10
            hitbox_offset_y = 10
            player_hitbox = player.rect.inflate(-hitbox_offset_x, -hitbox_offset_y)
            obstacle_hitbox = obstacle.rect.inflate(-hitbox_offset_x, -hitbox_offset_y)
            
            if player_hitbox.colliderect(obstacle_hitbox):
                if invincible_timer > 0:
                    # Destroy obstacle if invincible
                    obstacle.rect.x = -100
                    if jump_sound: jump_sound.play() # little feedback
                else:
                    if crash_sound: crash_sound.play()
                    if pygame.mixer.get_init(): pygame.mixer.music.stop()
                    game_active = False
                
        obstacles = [obs for obs in obstacles if obs.rect.right > 0]

        score_inc = 0.05
        if speed_timer > 0: score_inc *= 2
        if multiplier_timer > 0: score_inc *= 3
        score += score_inc
        
        display_ui()
        
    else:
        draw_background(screen, bg_scroll)
        game_over_text = font.render('Game Over! Press SPACE to restart.', True, GREEN)
        game_over_rect = game_over_text.get_rect(center=(WIDTH/2, HEIGHT/2))
        screen.blit(game_over_text, game_over_rect)
        display_ui()

    pygame.display.update()
    clock.tick(FPS)
