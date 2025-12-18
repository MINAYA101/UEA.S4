import pygame
import random
import sys
from pygame.locals import *

# Constantes del juego
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SIDEBAR_WIDTH = 200

# Colores (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 120, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Formas de los tetrominós con sus respectivos colores
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]]   # Z
]

# Colores correspondientes a cada forma
SHAPE_COLORS = [CYAN, YELLOW, MAGENTA, ORANGE, BLUE, GREEN, RED]

class Tetromino:
    """
    Clase que representa un tetrominó (pieza del Tetris).
    Contiene la forma, color, posición y métodos para manipular la pieza.
    """
    
    def __init__(self, x, y):
        """Inicializa un tetrominó con forma y color aleatorios."""
        self.x = x
        self.y = y
        self.shape_idx = random.randint(0, len(SHAPES) - 1)
        self.shape = SHAPES[self.shape_idx]
        self.color = SHAPE_COLORS[self.shape_idx]
        self.rotation = 0
        
    def rotate(self):
        """Rota el tetrominó 90 grados en sentido horario."""
        # Transpone la matriz (cambia filas por columnas)
        rotated = list(zip(*self.shape[::-1]))
        # Convierte tuplas a listas
        self.shape = [list(row) for row in rotated]
        
    def get_positions(self):
        """Devuelve las posiciones de cada bloque del tetrominó en la cuadrícula."""
        positions = []
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    positions.append((self.x + x, self.y + y))
        return positions
    
    def draw(self, screen, grid_x, grid_y):
        """Dibuja el tetrominó en la pantalla."""
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    rect_x = grid_x + (self.x + x) * GRID_SIZE
                    rect_y = grid_y + (self.y + y) * GRID_SIZE
                    pygame.draw.rect(screen, self.color, 
                                    (rect_x, rect_y, GRID_SIZE, GRID_SIZE))
                    pygame.draw.rect(screen, WHITE, 
                                    (rect_x, rect_y, GRID_SIZE, GRID_SIZE), 1)
                    
    def get_bounding_box(self):
        """Devuelve el cuadro delimitador del tetrominó."""
        return {
            'left': self.x,
            'right': self.x + len(self.shape[0]),
            'top': self.y,
            'bottom': self.y + len(self.shape)
        }


class Grid:
    """
    Clase que representa la cuadrícula del juego.
    Maneja la colocación de piezas, la detección de colisiones y la eliminación de líneas.
    """
    
    def __init__(self, width, height):
        """Inicializa una cuadrícula vacía."""
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.colors = [[BLACK for _ in range(width)] for _ in range(height)]
        
    def is_collision(self, tetromino):
        """Verifica si el tetrominó colisiona con los bloques existentes o los bordes."""
        for x, y in tetromino.get_positions():
            # Verificar límites de la cuadrícula
            if x < 0 or x >= self.width or y >= self.height:
                return True
            # Verificar si hay un bloque en esa posición
            if y >= 0 and self.grid[y][x]:
                return True
        return False
    
    def add_tetromino(self, tetromino):
        """Agrega un tetrominó a la cuadrícula."""
        for x, y in tetromino.get_positions():
            if y >= 0:  # Solo agregar si está dentro de la cuadrícula
                self.grid[y][x] = 1
                self.colors[y][x] = tetromino.color
                
    def clear_lines(self):
        """Elimina las líneas completas y devuelve el número de líneas eliminadas."""
        lines_cleared = 0
        # Comenzar desde la parte inferior
        y = self.height - 1
        while y >= 0:
            if all(self.grid[y]):
                # Mover todas las filas superiores hacia abajo
                for y2 in range(y, 0, -1):
                    self.grid[y2] = self.grid[y2 - 1][:]
                    self.colors[y2] = self.colors[y2 - 1][:]
                # Crear una nueva fila vacía en la parte superior
                self.grid[0] = [0 for _ in range(self.width)]
                self.colors[0] = [BLACK for _ in range(self.width)]
                lines_cleared += 1
                # No decrementar y porque necesitamos revisar la nueva fila en esta posición
            else:
                y -= 1
        return lines_cleared
    
    def draw(self, screen, grid_x, grid_y):
        """Dibuja la cuadrícula en la pantalla."""
        # Dibujar el fondo de la cuadrícula
        pygame.draw.rect(screen, BLACK, 
                        (grid_x, grid_y, self.width * GRID_SIZE, self.height * GRID_SIZE))
        
        # Dibujar las líneas de la cuadrícula
        for x in range(self.width + 1):
            pygame.draw.line(screen, GRAY, 
                            (grid_x + x * GRID_SIZE, grid_y),
                            (grid_x + x * GRID_SIZE, grid_y + self.height * GRID_SIZE))
        for y in range(self.height + 1):
            pygame.draw.line(screen, GRAY,
                            (grid_x, grid_y + y * GRID_SIZE),
                            (grid_x + self.width * GRID_SIZE, grid_y + y * GRID_SIZE))
        
        # Dibujar los bloques colocados
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x]:
                    rect_x = grid_x + x * GRID_SIZE
                    rect_y = grid_y + y * GRID_SIZE
                    pygame.draw.rect(screen, self.colors[y][x],
                                    (rect_x, rect_y, GRID_SIZE, GRID_SIZE))
                    pygame.draw.rect(screen, WHITE,
                                    (rect_x, rect_y, GRID_SIZE, GRID_SIZE), 1)


class Game:
    """
    Clase principal del juego Tetris.
    Coordina todos los componentes y maneja la lógica del juego.
    """
    
    def __init__(self):
        """Inicializa el juego con todos sus componentes."""
        pygame.init()
        
        # Configurar la pantalla
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris - POO")
        
        # Configurar reloj para controlar FPS
        self.clock = pygame.time.Clock()
        self.fps = 60
        
        # Configurar fuentes
        self.font = pygame.font.SysFont('Arial', 24)
        self.big_font = pygame.font.SysFont('Arial', 36, bold=True)
        
        # Calcular posición de la cuadrícula para centrarla
        self.grid_x = (SCREEN_WIDTH - SIDEBAR_WIDTH - GRID_WIDTH * GRID_SIZE) // 2
        self.grid_y = (SCREEN_HEIGHT - GRID_HEIGHT * GRID_SIZE) // 2
        
        # Inicializar componentes del juego
        self.grid = Grid(GRID_WIDTH, GRID_HEIGHT)
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        
        # Variables del juego
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.paused = False
        
        # Control de velocidad (caída automática)
        self.fall_speed = 0.5  # segundos por cuadro
        self.fall_time = 0
        
        # Configurar eventos de tiempo para la caída automática
        self.FALL_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.FALL_EVENT, int(self.fall_speed * 1000))
        
    def new_piece(self):
        """Crea una nueva pieza en la posición inicial."""
        # La pieza aparece en la parte superior central
        start_x = GRID_WIDTH // 2 - 1
        start_y = 0
        return Tetromino(start_x, start_y)
    
    def move_piece(self, dx, dy):
        """Intenta mover la pieza actual y devuelve si fue exitoso."""
        self.current_piece.x += dx
        self.current_piece.y += dy
        
        if self.grid.is_collision(self.current_piece):
            # Deshacer el movimiento si hay colisión
            self.current_piece.x -= dx
            self.current_piece.y -= dy
            return False
        return True
    
    def rotate_piece(self):
        """Intenta rotar la pieza actual."""
        # Guardar la rotación actual
        original_shape = self.current_piece.shape
        
        # Rotar la pieza
        self.current_piece.rotate()
        
        # Si hay colisión después de rotar, revertir la rotación
        if self.grid.is_collision(self.current_piece):
            self.current_piece.shape = original_shape
    
    def drop_piece(self):
        """Hace caer la pieza actual hasta que toque el fondo o otra pieza."""
        while self.move_piece(0, 1):
            pass  # Continuar moviendo hacia abajo hasta que haya colisión
        
        # Cuando no se puede mover más hacia abajo, colocar la pieza
        self.place_piece()
    
    def place_piece(self):
        """Coloca la pieza actual en la cuadrícula y genera una nueva."""
        # Agregar la pieza actual a la cuadrícula
        self.grid.add_tetromino(self.current_piece)
        
        # Verificar y eliminar líneas completas
        lines = self.grid.clear_lines()
        if lines > 0:
            self.update_score(lines)
        
        # Crear nueva pieza
        self.current_piece = self.next_piece
        self.next_piece = self.new_piece()
        
        # Verificar si el juego ha terminado (colisión al crear nueva pieza)
        if self.grid.is_collision(self.current_piece):
            self.game_over = True
    
    def update_score(self, lines):
        """Actualiza la puntuación basada en el número de líneas eliminadas."""
        # Puntos según el número de líneas eliminadas a la vez
        line_points = {1: 100, 2: 300, 3: 500, 4: 800}
        
        # Sumar puntos
        self.score += line_points.get(lines, 0) * self.level
        
        # Actualizar líneas eliminadas y nivel
        self.lines_cleared += lines
        self.level = self.lines_cleared // 10 + 1
        
        # Aumentar la velocidad con cada nivel
        new_speed = max(50, 1000 - (self.level - 1) * 100)  # En milisegundos
        pygame.time.set_timer(self.FALL_EVENT, new_speed)
    
    def draw_sidebar(self):
        """Dibuja la barra lateral con información del juego."""
        sidebar_x = SCREEN_WIDTH - SIDEBAR_WIDTH
        
        # Fondo de la barra lateral
        pygame.draw.rect(self.screen, (40, 40, 60), 
                        (sidebar_x, 0, SIDEBAR_WIDTH, SCREEN_HEIGHT))
        
        # Título
        title = self.big_font.render("TETRIS", True, YELLOW)
        self.screen.blit(title, (sidebar_x + 20, 30))
        
        # Información del juego
        score_text = self.font.render(f"Puntuación: {self.score}", True, WHITE)
        level_text = self.font.render(f"Nivel: {self.level}", True, WHITE)
        lines_text = self.font.render(f"Líneas: {self.lines_cleared}", True, WHITE)
        
        self.screen.blit(score_text, (sidebar_x + 20, 100))
        self.screen.blit(level_text, (sidebar_x + 20, 140))
        self.screen.blit(lines_text, (sidebar_x + 20, 180))
        
        # Siguiente pieza
        next_text = self.font.render("Siguiente:", True, WHITE)
        self.screen.blit(next_text, (sidebar_x + 20, 250))
        
        # Dibujar la siguiente pieza
        next_piece_x = sidebar_x + 60
        next_piece_y = 300
        
        # Dibujar el fondo para la siguiente pieza
        pygame.draw.rect(self.screen, BLACK, 
                        (next_piece_x - 10, next_piece_y - 10, 100, 100))
        
        # Dibujar la siguiente pieza centrada
        for y, row in enumerate(self.next_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    rect_x = next_piece_x + x * GRID_SIZE
                    rect_y = next_piece_y + y * GRID_SIZE
                    pygame.draw.rect(self.screen, self.next_piece.color,
                                    (rect_x, rect_y, GRID_SIZE, GRID_SIZE))
                    pygame.draw.rect(self.screen, WHITE,
                                    (rect_x, rect_y, GRID_SIZE, GRID_SIZE), 1)
        
        # Controles
        controls_y = 450
        controls = [
            "Controles:",
            "← → : Mover",
            "↑ : Rotar",
            "↓ : Bajar rápido",
            "Espacio: Caída rápida",
            "P : Pausa",
            "R : Reiniciar",
            "ESC : Salir"
        ]
        
        for i, text in enumerate(controls):
            control_text = self.font.render(text, True, WHITE)
            self.screen.blit(control_text, (sidebar_x + 20, controls_y + i * 30))
        
        # Mensaje de pausa
        if self.paused:
            pause_text = self.big_font.render("PAUSA", True, YELLOW)
            text_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(pause_text, text_rect)
        
        # Mensaje de game over
        if self.game_over:
            game_over_text = self.big_font.render("GAME OVER", True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(game_over_text, text_rect)
            
            restart_text = self.font.render("Presiona R para reiniciar", True, WHITE)
            text_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
            self.screen.blit(restart_text, text_rect)
    
    def draw(self):
        """Dibuja todos los elementos del juego en la pantalla."""
        # Fondo
        self.screen.fill((20, 20, 40))
        
        # Dibujar la cuadrícula
        self.grid.draw(self.screen, self.grid_x, self.grid_y)
        
        # Dibujar la pieza actual
        self.current_piece.draw(self.screen, self.grid_x, self.grid_y)
        
        # Dibujar la barra lateral
        self.draw_sidebar()
        
        # Actualizar la pantalla
        pygame.display.flip()
    
    def handle_events(self):
        """Maneja los eventos del juego (teclado, temporizadores, etc.)."""
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                
                if not self.game_over:
                    if event.key == K_p:
                        self.paused = not self.paused
                    
                    if not self.paused:
                        if event.key == K_LEFT:
                            self.move_piece(-1, 0)
                        elif event.key == K_RIGHT:
                            self.move_piece(1, 0)
                        elif event.key == K_DOWN:
                            self.move_piece(0, 1)
                        elif event.key == K_UP:
                            self.rotate_piece()
                        elif event.key == K_SPACE:
                            self.drop_piece()
                
                if event.key == K_r:
                    self.__init__()  # Reiniciar el juego
            
            # Evento de caída automática
            if event.type == self.FALL_EVENT and not self.paused and not self.game_over:
                if not self.move_piece(0, 1):
                    self.place_piece()
    
    def run(self):
        """Bucle principal del juego."""
        while True:
            self.handle_events()
            self.draw()
            self.clock.tick(self.fps)


# Punto de entrada del programa
if __name__ == "__main__":
    print("Iniciando Tetris...")
    print("Controles:")
    print("  Flechas: Mover y rotar")
    print("  Espacio: Caída rápida")
    print("  P: Pausa")
    print("  R: Reiniciar")
    print("  ESC: Salir")
    print("\n¡Disfruta del juego!")
    
    game = Game()
    game.run()