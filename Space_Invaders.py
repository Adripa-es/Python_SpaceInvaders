import pygame
import random
import math
from pygame import mixer

# Inicializamos las herramientas necesarias para usar pygame
pygame.init()

# Titulo del juego
pygame.display.set_caption("SPACE INVADERS")

# Preparamos cosas basicas del juego
icono = pygame.image.load("Dia 10\SpInv_Icono.png")

# Icono de la ventana del juego
pygame.display.set_icon(icono)

# Agregar sonidos
mixer.music.load("Dia 10\SpInv_MusicaFondo.mp3")
mixer.music.set_volume(0.3)
# el argumento es la cantidad de veces que se repita la musica (-1 es infinito)
mixer.music.play(-1)

sonidoColision = mixer.Sound("Dia 10\SpInv_Colision.mp3")
sonidoColision.set_volume(1)
sonidoDisparo = mixer.Sound("Dia 10\SpInv_Disparo.mp3")
sonidoDisparo.set_volume(0.3)
sonidoInicio = mixer.Sound("Dia 10\Inicio.mp3")
sonidoInicio.set_volume(0.1)
sonidoInicio.play()

# Variables globales
pantalla = pygame.display.set_mode((800, 600))
fondoImg = pygame.image.load("Dia 10\SpInv_Fondo.jpg")
enEjecucion = True

# Variables del jugador
jugadorImg = pygame.image.load("Dia 10\SpInv_Jugador.png")
jugadorImg = pygame.transform.scale(
    jugadorImg, (64, 64))  # para reescalar la imagen

jugadorX = (pygame.display.Info().current_w / 2) - (64 / 2)
jugadorY = 564 - 64
velocidadX = 0

# Variables del enemigo
enemigoImg = []
enemigoX = []
enemigoY = []
velEnemigoX = []
velEnemigoY = []
cantidadEnemigos = 8

# Fin Juego
fuenteFinal = pygame.font.Font("Dia 10\H4VintageRetro.ttf", 40)

# creamos una lista de 8 enemigos
for enemigo in range(cantidadEnemigos):
    enemigoImg.append(pygame.image.load("Dia 10\SpInv_Enemigo.png"))
    enemigoX.append(random.randint(0, 736))
    enemigoY.append(random.randint(50, 200))
    velEnemigoX.append(0.5)
    velEnemigoY.append(50)

# Variables del proyectil
proyectilImg = pygame.image.load("Dia 10\SpInv_bala.png")
proyectilX = jugadorX + 16
proyectilY = jugadorY + 10
velProyectilX = 0
velProyectilY = 3
proyectilVisible = False

# Variables para la puntuacion
pts = 0
# variable que contendrá los puntos a nivel visual
# la fuente hay que descargarla e meterla en la misma carpeta
fuente = pygame.font.Font("Dia 10\H4VintageRetro.ttf", 32)
textoX = 10
textoY = 10


def mostrar_Pts():
    global pts, textoX, textoY
    texto = fuente.render(f"Puntos: {pts}", True, (255, 255, 255))
    pantalla.blit(texto, (textoX, textoY))


# Funcion para dibujar el jugador en la pantalla
def dibujar_jugador():
    pantalla.blit(jugadorImg, (jugadorX, jugadorY))

# Funcion para dibujar el enemigo en la pantalla


def dibujar_enemigo(enemigo):
    pantalla.blit(enemigoImg[enemigo], (enemigoX[enemigo], enemigoY[enemigo]))

# Funcion para dibujar el proyectil en la pantalla


def dibujar_proyectil(proyectilX, proyectilY):
    global proyectilVisible
    proyectilVisible = True
    # Se añaden 16 y 10 px para centrar mejor el disparo
    pantalla.blit(proyectilImg, (proyectilX + 16, proyectilY + 10))

# Funcion para detectar colisiones entre dos objetos


def detectar_colisiones(objtX1, objtY1, objtX2, objtY2):
    diferenciaX = math.pow(objtX2 - objtX1, 2)
    diferenciaY = math.pow(objtY2 - objtY1, 2)
    distancia = math.sqrt(diferenciaX + diferenciaY)
    if distancia < 27:
        return True
    else:
        return False

# Funcion para mantener al jugador dentro de los bordes
def mantener_bordes_jugador():
    global jugadorX
    if jugadorX <= 0:
        jugadorX = 0
    elif jugadorX >= 736:
        jugadorX = 736

# Funcion para mantener al enemigo dentro de los bordes
def mantener_bordes_enemigo(enemigo):
    global enemigoX, enemigoY, velEnemigoX, velEnemigoY
    if enemigoX[enemigo] <= 0:
        velEnemigoX[enemigo] = 0.5
        enemigoY[enemigo] += velEnemigoY[enemigo]
    elif enemigoX[enemigo] >= 736:
        velEnemigoX[enemigo] = -0.5
        enemigoY[enemigo] += velEnemigoY[enemigo]

    if enemigoY[enemigo] > 600:
        enemigoY[enemigo] = random.randint(50, 200)

# Funcion para controlar los eventos del teclado
def control_teclado():
    # ponemos global para que se puedan actualizar en todas partes que estén
    global velocidadX
    global enEjecucion
    global proyectilX
    for eventos in pygame.event.get():
        # si el evento es del tipo quit (osea cerrar la ventana con la X)
        # evento cerrar
        if eventos.type == pygame.QUIT:
            enEjecucion = False

        # cuando alguna tecla sea pulsada
        if eventos.type == pygame.KEYDOWN:
            if eventos.key == pygame.K_LEFT:
                velocidadX = -1
            if eventos.key == pygame.K_RIGHT:
                velocidadX = 1
            # cuando se pulse el boton de disparar y no haya bala visible
            if eventos.key == pygame.K_SPACE and not proyectilVisible:
                sonidoDisparo.play()
                proyectilX = jugadorX
                dibujar_proyectil(proyectilX, proyectilY)


            if eventos.key == pygame.K_r:
                reiniciar_partida()

        # evento soltar flechas
        if eventos.type == pygame.KEYUP:
            # si una de las teclas de movimiento lateral se suelta
            if eventos.key == pygame.K_LEFT or eventos.key == pygame.K_RIGHT:
                velocidadX = 0

def FinalJuego():
    miFuenteFinal = fuenteFinal.render("GAME OVER", True, (255, 255, 255))
    # mensaje centrado (a ojo)
    pantalla.blit(miFuenteFinal, (200, 150))

def reiniciar_partida():
    global pts, enemigoX, enemigoY, proyectilVisible
    pts = 0
    enemigoX = [random.randint(0, 736) for i in range(cantidadEnemigos)]
    enemigoY = [random.randint(50, 200) for i in range(cantidadEnemigos)]
    proyectilVisible = False
    sonidoInicio.play()



# Ejecucion del juego
while enEjecucion:

    # pintamos la pantalla de un color definido por valores de RGB
    #pantalla.fill((205, 144, 228))

    pantalla.blit(fondoImg, (0, 0))

    control_teclado()

    # modificar ubicacion del jugador
    jugadorX += velocidadX

    # mantener dentro de bordes al jugador
    mantener_bordes_jugador()

    # mantener dentro de bordes al enemigo
    for enemigo in range(cantidadEnemigos):

        # Colision con jugador
        if enemigoY[enemigo] > 500:
            # se resetean las posiciones de los enemigos
            for k in range(cantidadEnemigos):
                enemigoY[k] = 1000

            FinalJuego()
            break

        enemigoX[enemigo] += velEnemigoX[enemigo]
        mantener_bordes_enemigo(enemigo)

        # Verificar colisiones
        colision = detectar_colisiones(
            enemigoX[enemigo], enemigoY[enemigo], proyectilX, proyectilY)
        if colision:
            sonidoColision.play()

            proyectilVisible = False
            pts += 1

            # cada vez que el proyectil y el enemigo colisionen,
            # la posicion del enemigo se reinicia a una aleatoria otra vez
            enemigoX[enemigo] = random.randint(0, 736)
            enemigoY[enemigo] = random.randint(50, 200)
        dibujar_enemigo(enemigo)

    # cuando la bala ya no sea visible, entonces reseteamos su posicion
    if proyectilY <= -64:
        proyectilY = 500
        proyectilVisible = False

    # movimiento proyectil
    if proyectilVisible:
        dibujar_proyectil(proyectilX, proyectilY)
        proyectilY -= velProyectilY

    dibujar_jugador()

    mostrar_Pts()

    # para actualizar el color de la pantalla
    pygame.display.update()
