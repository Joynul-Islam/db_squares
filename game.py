import pygame
from sqlmodel import create_engine, SQLModel, Session, select, col, or_
from sqlalchemy.exc import IntegrityError

from models import MySquare
import os

db_user = os.environ.get('MYSQL_DB_USER')
db_pass = os.environ.get('MYSQL_DB_PASS')
engine = create_engine(f'mysql+pymysql://{db_user}:{db_pass}@localhost/squares', echo=True)

SQLModel.metadata.create_all(engine)


# Initialize Pygame
pygame.init()

# Set up the window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Main game loop
running = True


def get_history(sid:str):
    with Session(engine) as session:
        squares = session.exec(select(MySquare).where(MySquare.session_id == sid)).all()
        return squares


with Session(engine) as session:
    sid = input("Enter session id: ")
    for sq in get_history(sid=sid):
        # Draw previous session's squares on the screen
        pygame.draw.rect(window, WHITE, (sq.x_pos, sq.y_pos, sq.x, sq.y))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                session.commit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Get the position of the mouse click
                mouse_pos = pygame.mouse.get_pos()

                new_square = MySquare(session_id=sid)
                new_square.x_pos = mouse_pos[0] - new_square.x // 2
                new_square.y_pos = mouse_pos[1] - new_square.y // 2

                # Draw the square on the screen
                pygame.draw.rect(window, WHITE, (new_square.x_pos, new_square.y_pos, new_square.x, new_square.y))

                session.add(new_square)

        # Fill the screen with black
        #window.fill(BLACK)

        # Update the screen
        pygame.display.update()

# Quit Pygame
pygame.quit()
