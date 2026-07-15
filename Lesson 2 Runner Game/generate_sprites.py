import pygame
import sys

# Need a display mode to initialize some pygame drawing features properly in some OS
pygame.init()
pygame.display.set_mode((100, 100), pygame.HIDDEN)

# 1. Create a transparent player image (Neon Cyborg Runner)
surf = pygame.Surface((50, 50), pygame.SRCALPHA)
# Head
pygame.draw.rect(surf, (0, 255, 255), (15, 5, 20, 20), border_radius=5)
# Glowing Eye visor
pygame.draw.rect(surf, (255, 255, 0), (20, 10, 15, 6))
# Body
pygame.draw.rect(surf, (0, 200, 200), (10, 25, 30, 20), border_radius=4)
# Arm
pygame.draw.rect(surf, (0, 150, 150), (20, 28, 20, 8), border_radius=3)
# Legs (simple)
pygame.draw.rect(surf, (0, 150, 150), (15, 45, 8, 5))
pygame.draw.rect(surf, (0, 150, 150), (27, 45, 8, 5))
pygame.image.save(surf, "player.png")

# 2. Create obstacle 1 (Laser barrier)
surf_obs1 = pygame.Surface((40, 50), pygame.SRCALPHA)
# Base
pygame.draw.rect(surf_obs1, (100, 100, 100), (5, 40, 30, 10), border_radius=3)
# Laser
pygame.draw.rect(surf_obs1, (255, 0, 0), (15, 0, 10, 40))
pygame.draw.rect(surf_obs1, (255, 150, 150), (18, 0, 4, 40)) # Inner glow
pygame.image.save(surf_obs1, "obstacle.png")

# 3. Create obstacle 2 (Floating Mine)
surf_obs2 = pygame.Surface((40, 40), pygame.SRCALPHA)
# Spikes
pygame.draw.line(surf_obs2, (200, 200, 200), (20, 0), (20, 40), 6)
pygame.draw.line(surf_obs2, (200, 200, 200), (0, 20), (40, 20), 6)
pygame.draw.line(surf_obs2, (200, 200, 200), (5, 5), (35, 35), 4)
pygame.draw.line(surf_obs2, (200, 200, 200), (5, 35), (35, 5), 4)
# Core
pygame.draw.circle(surf_obs2, (100, 100, 100), (20, 20), 12)
pygame.draw.circle(surf_obs2, (255, 50, 50), (20, 20), 6) # glowing center
pygame.image.save(surf_obs2, "obstacle2.png")

# 4. Create obstacle 3 (Neon Spike trap)
surf_obs3 = pygame.Surface((50, 50), pygame.SRCALPHA)
# Base
pygame.draw.rect(surf_obs3, (50, 50, 50), (0, 40, 50, 10))
# Spikes
pygame.draw.polygon(surf_obs3, (255, 150, 0), [(5, 40), (15, 15), (25, 40)])
pygame.draw.polygon(surf_obs3, (255, 150, 0), [(25, 40), (35, 15), (45, 40)])
# Inner bright
pygame.draw.polygon(surf_obs3, (255, 255, 100), [(10, 40), (15, 25), (20, 40)])
pygame.draw.polygon(surf_obs3, (255, 255, 100), [(30, 40), (35, 25), (40, 40)])
pygame.image.save(surf_obs3, "obstacle3.png")

pygame.quit()
print("Generated new transparent sprites!")
