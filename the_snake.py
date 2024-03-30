"""
Модуль, использующий библиотеку pygame.

и функцию randint из модуля random.
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


class GameObject:
    """Экран объекта."""

    def __init__(self, body_color=APPLE_COLOR) -> None:
        """Задает новый объект и Цвет тела объекта."""
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = body_color

    def draw(self):
        """Заглушка метод определен в потомках."""
        raise NotImplementedError(f'Определите draw{type(self).__name__}')


class Apple(GameObject):
    """Яблоко."""

    def __init__(self, body_color=APPLE_COLOR) -> None:
        """Инициализирует яблоко на игром поле."""
        super().__init__(body_color)
        self.position = self.randomize_position()

    def randomize_position(self):
        """Установка случайного положения яблока на поле."""
        return (
            randint(1, GRID_WIDTH) * GRID_SIZE - GRID_SIZE,
            randint(1, GRID_HEIGHT) * GRID_SIZE - GRID_SIZE
            )

    def draw(self):
        """Отрисовывает объект на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Змейка."""

    def __init__(self):
        """Инициализирует начальное состояние змеи."""
        self.length = 1
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = (0, 255, 0)
        self.last = None
        self.reset()

    def move(self):
        """
        Обновляет позицию змеи и добавляет новую голову.

        и удаляет последний сегмент, если длина не увеличилась.
        """
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

        cur_head = self.get_head_position()
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
        Возвращает позицию головы змейки.

        (вроде первый элемент в списке positions).
        """
        if self.next_direction:
            self.direction = self.next_direction

    def draw(self):
        """Отрисовывает змейку на экране."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """
        Сбрасывает змейку в начальное состояние.

        после столкновение с собой.
        """
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None

    def get_head_position(self):
        """Возвращает позицию головы змеи."""
        return self.positions[0]


def handle_keys(game_object):
    """Обработка нажитий на клавиши для управления змеей."""
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
