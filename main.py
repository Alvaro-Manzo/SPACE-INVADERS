import pygame
import random
import math
from pygame import mixer

def iniciar_juego():
    global jugador_x, jugador_y, jugador_x_cambio
    global enemigo_x, enemigo_y, enemigo_x_cambio, enemigo_y_cambio
    global balas, puntaje, juego_terminado

    jugador_x = 368
    jugador_y = 500
    jugador_x_cambio = 0

    enemigo_x = []
    enemigo_y = []
    enemigo_x_cambio = []
    enemigo_y_cambio = []
    for _ in range(cantidad_enemigos):
        enemigo_x.append(random.randint(0, 736))
        enemigo_y.append(random.randint(50, 200))
        enemigo_x_cambio.append(1)
        enemigo_y_cambio.append(50)

    balas = []
    puntaje = 0
    juego_terminado = False

# Inicializar pygame
pygame.init()
pantalla = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Invasión Espacial")
icono = pygame.image.load("ovni (1).png")
pygame.display.set_icon(icono)
fondo = pygame.image.load("Fondo.jpg")

# Música de fondo
mixer.music.load("MusicaFondo.mp3")
mixer.music.set_volume(0.3)
mixer.music.play(-1)

# Jugador
img_jugador = pygame.image.load("astronave.png")

# Enemigos
img_enemigo = [pygame.image.load("ovni (1).png") for _ in range(8)]
cantidad_enemigos = 8

# Bala
img_bala = pygame.image.load("bala.png")

# Puntaje
fuente = pygame.font.Font("freesansbold.ttf", 32)
texto_x = 10
texto_y = 10

# Texto final
fuente_final = pygame.font.Font("freesansbold.ttf", 40)
fuente_reiniciar = pygame.font.Font("freesansbold.ttf", 30)

def mostrar_puntaje(x, y):
    texto = fuente.render(f"Puntaje: {puntaje}", True, (255, 255, 255))
    pantalla.blit(texto, (x, y))

def texto_final():
    mensaje = fuente_final.render("JUEGO TERMINADO", True, (255, 255, 255))
    pantalla.blit(mensaje, (220, 200))

def preguntar_reinicio():
    texto = fuente_reiniciar.render("¿Quieres volver a jugar? (S/N)", True, (255, 255, 0))
    pantalla.blit(texto, (180, 270))

def jugador(x, y):
    pantalla.blit(img_jugador, (x, y))

def enemigo(x, y, idx):
    pantalla.blit(img_enemigo[idx], (x, y))

def disparar_bala(x, y):
    pantalla.blit(img_bala, (x + 16, y + 10))

def hay_colision(x1, y1, x2, y2):
    distancia = math.hypot(x2 - x1, y2 - y1)
    return distancia < 27

# Comenzar primer juego
iniciar_juego()

# Bucle principal
se_ejecuta = True
while se_ejecuta:
    pantalla.blit(fondo, (0, 0))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            se_ejecuta = False

        if not juego_terminado:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    jugador_x_cambio = -4
                if evento.key == pygame.K_RIGHT:
                    jugador_x_cambio = 4
                if evento.key == pygame.K_SPACE:
                    sonido_bala = mixer.Sound("disparo.mp3")
                    sonido_bala.play()
                    balas.append({"x": jugador_x, "y": jugador_y, "velocidad": -5})

            if evento.type == pygame.KEYUP:
                if evento.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    jugador_x_cambio = 0
        else:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_s:
                    iniciar_juego()
                elif evento.key == pygame.K_n:
                    se_ejecuta = False

    if not juego_terminado:
        jugador_x += jugador_x_cambio
        jugador_x = max(0, min(jugador_x, 736))

        # Enemigos
        for i in range(cantidad_enemigos):
            if enemigo_y[i] > 500:
                for j in range(cantidad_enemigos):
                    enemigo_y[j] = 1000
                juego_terminado = True
                break

            velocidad_fija = 2.8  # <<--- ENEMIGO RÁPIDO PERO CONSTANTE
            enemigo_x[i] += enemigo_x_cambio[i] * velocidad_fija

            if enemigo_x[i] <= 0:
                enemigo_x_cambio[i] = 1
                enemigo_y[i] += enemigo_y_cambio[i]
            elif enemigo_x[i] >= 736:
                enemigo_x_cambio[i] = -1
                enemigo_y[i] += enemigo_y_cambio[i]

            for bala in list(balas):
                if hay_colision(enemigo_x[i], enemigo_y[i], bala["x"], bala["y"]):
                    sonido_colision = mixer.Sound("golpe.mp3")
                    sonido_colision.play()
                    balas.remove(bala)
                    enemigo_x[i] = random.randint(0, 736)
                    enemigo_y[i] = random.randint(90, 200)
                    puntaje += 1

            enemigo(enemigo_x[i], enemigo_y[i], i)

        # Balas
        for bala in list(balas):
            bala["y"] += bala["velocidad"]
            if bala["y"] < 0:
                balas.remove(bala)
            else:
                disparar_bala(bala["x"], bala["y"])

        jugador(jugador_x, jugador_y)
        mostrar_puntaje(texto_x, texto_y)
    else:
        texto_final()
        preguntar_reinicio()

    pygame.display.update()
