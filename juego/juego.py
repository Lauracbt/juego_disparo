import pygame
import random

# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Crear la ventana del juego
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Juego de Disparos kodland")


# Clase para la nave espacial
class Spaceship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed = 5

    def update(self):
        # Obtener la entrada del teclado
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Mantener la nave espacial dentro de la pantalla
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


# Clase para los cuadrados
class Square(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -50)
        self.speed = random.randrange(1, 5)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randrange(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -50)
            self.speed = random.randrange(1, 5)


# Clase para los proyectiles
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 20))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = 10

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()


# Crear los grupos de sprites
all_sprites = pygame.sprite.Group()
squares = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Crear la nave espacial
spaceship = Spaceship()
all_sprites.add(spaceship)

# Generar los cuadrados
for _ in range(10):
    square = Square()
    all_sprites.add(square)
    squares.add(square)

# Variables de control del juego
clock = pygame.time.Clock()
running = True

# Bucle principal del juego
while running:
    # Controlar eventos del teclado y cierre de la ventana
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                spaceship.shoot()

    # Actualizar sprites
    all_sprites.update()

    # Comprobar colisiones entre los cuadrados y los proyectiles
    hits = pygame.sprite.groupcollide(squares, bullets, True, True)
    for hit in hits:
        square = Square()
        all_sprites.add(square)
        squares.add(square)

    # Comprobar colisiones entre la nave espacial y los cuadrados
    hits = pygame.sprite.spritecollide(spaceship, squares, False)
    if hits:
        running = False

    # Dibujar la pantalla
    screen.fill(WHITE)
    all_sprites.draw(screen)

    # Actualizar la pantalla
    pygame.display.flip()
    clock.tick(60)

# Salir del juego
pygame.quit()
