"""
Модуль, который использует библиотеку pygame и функцию randint из модуля random.
"""

from random import randint
import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()

# Тут опишите все классы игры.
class GameObject:
    """Экран объекта."""

    def __init__(self, body_color=APPLE_COLOR) -> None:
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = body_color

    def draw(self):
        """Заглушка метод определен в потомках."""
        raise NotImplementedError(f'Определите draw{type(self).__name__}')

class Apple(GameObject):
    """Яблоко."""

    def __init__(self, body_color=APPLE_COLOR) -> None:
        super().__init__(body_color)
        self.position = self.randomize_position()

    def randomize_position(self):
        """Случайная позиция яблока."""
        return (
            randint(0, GRID_WIDTH) * GRID_SIZE - GRID_SIZE,
            randint(0, GRID_HEIGHT) * GRID_SIZE - GRID_SIZE
        )

# Метод draw класса Snake
    def draw(self):
        """Отрисовывает объект на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

class Snake(GameObject):
    """Змейка."""

    def __init__(self):
        self.length = 1
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = (0, 255, 0)
        self.last = None

    def move(self):
        """
        Обновляет позиция змейка и ещё добавляет новую голову
        и удаляет последний сегмент, если длина не увеличилась.
        """
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

        cur_head = self.positions[0]
        x, y = self.direction
        new_head = ((cur_head[0] + (x * GRID_SIZE)) % SCREEN_WIDTH,
                    (cur_head[1] + (y * GRID_SIZE)) % SCREEN_HEIGHT)

        if len(self.positions) > 2 and new_head in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new_head)
            if len(self.positions) > self.length:
                self.positions.pop()

    def update_direction(self):
        """
        Возвращает позицию головы змейки
        (вроде первый элемент в списке positions).
        """        
        if self.next_direction:
            self.direction = self.next_direction

    # Метод draw класса Snake
    def draw(self):
        """Отрисовывает змейку на экране."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """
        Сбрасывает змейку в начальное состояние
        после столкновение с собой.
        """
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None

    def get_head_position(self):
        return self.positions[0]

def handle_keys(game_object):

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT

def main() -> None:
    """функция выполнения игры цикл."""
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position()

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()