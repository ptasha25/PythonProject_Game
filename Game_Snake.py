import random
import pygame
import pygame_menu
import time
from random import randrange
import sqlite3

class Game:
    pygame.init()
    __size_of_field = 1000
    __size_of_object = 50
    __rad_of_eyes = 5
    __circul_of_eyes = 2
    _surface = pygame.display.set_mode((__size_of_field, __size_of_field))
    _menu = pygame_menu.Menu('SNAKE', __size_of_field, __size_of_field,
                                  theme=pygame_menu.themes.THEME_BLUE)

    def write_name():
        placement = 430
        length = 140
        width = 32
        clock = pygame.time.Clock()
        display_screen = pygame.display.set_mode((Game.__size_of_field, Game.__size_of_field))
        my_font = pygame.font.SysFont('Comic Sans MS', 40)

        user_text = ''

        input_rect = pygame.Rect(placement, placement - 10, length, width)
        color_active = pygame.Color('lightskyblue')
        color_passive = pygame.Color('gray15')
        color = color_passive

        active = False
        its_writen = False

        while True:
            if its_writen == True:
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    its_writen = True
                    #return user_text
                    break

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        its_writen = True
                        break

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_rect.collidepoint(event.pos):
                        active = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[0:-1]
                    else:
                        user_text += event.unicode

            display_screen.fill(('white'))

            if active:
                color = color_active
            else:
                color = color_passive

            pygame.draw.rect(display_screen, color, input_rect)

            text_surface = my_font.render('Your name:', 1, ("lightskyblue"))
            display_screen.blit(text_surface, (0, 0))
            pygame.display.flip()
            text_surface = my_font.render(user_text, True, ("black"))
            display_screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
            input_rect.w = max(100, text_surface.get_width() + 10)
            pygame.display.flip()
            clock.tick(60)
        return user_text

    def best_scores(user):
        bd = sqlite3.connect('sqlite_python.bd')
        cur = bd.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS snake_records(
           name TEXT,
           score INTEGER);
        """)
        writen_name = user[0]
        score = user[1]
        cur.execute(f"SELECT name, score FROM snake_records WHERE name = '{writen_name}' AND score = {score}")
        data = cur.fetchone()
        if data is None:
            cur.execute("INSERT INTO snake_records VALUES(?, ?);", user)
            result = cur.fetchall()
            bd.commit()
        cur.close()
    @staticmethod
    def pressing_the_button(dx, dy):
        dir = {'W': True, 'S': True, 'A': True, 'D': True}
        key = pygame.key.get_pressed()
        if key[pygame.K_w] and dir['W']:
            dir = {'W': True, 'S': False, 'A': True, 'D': True}
            dx, dy = 0, -1
        if key[pygame.K_s] and dir['S']:
            dx, dy = 0, 1
            dir = {'W': False, 'S': True, 'A': True, 'D': True}
        if key[pygame.K_a] and dir['A']:
            dx, dy = -1, 0
            dir = {'W': True, 'S': True, 'A': True, 'D': False}
        if key[pygame.K_d] and dir['D']:
            dx, dy = 1, 0
            dir = {'W': True, 'S': True, 'A': False, 'D': True}
        return dx, dy

    @staticmethod
    def set_colors(sc, SIZE, snake, apple, score, cloud):
        font_score = pygame.font.SysFont('Arial', 26, bold=True)
        [(pygame.draw.rect(sc, pygame.Color('green'), (i, j, SIZE - 2, SIZE - 2))) for i, j in snake]
        pygame.draw.circle(sc, pygame.Color("black"), (snake[-1][0] + SIZE // 2 - 10, snake[-1][1] + SIZE // 2), Game.__rad_of_eyes, Game.__circul_of_eyes)
        pygame.draw.circle(sc, pygame.Color("black"), (snake[-1][0] + SIZE // 2 + 10, snake[-1][1] + SIZE // 2), Game.__rad_of_eyes, Game.__circul_of_eyes)
        pygame.draw.rect(sc, pygame.Color('red'), (*apple, SIZE, SIZE))
        for i in range (len(cloud)):
            pygame.draw.rect(sc, pygame.Color('white'), (*cloud[i][0], SIZE, SIZE))
            pygame.draw.rect(sc, pygame.Color('white'), (*cloud[i][1], SIZE, SIZE))
        render_score = font_score.render(f'SCORE: {score}', 1, pygame.Color('orange'))
        sc.blit(render_score, (5, 5))

    def red_eyes(indexes, size, snake, sc, SIZE):
        if (size > 1):
            pygame.draw.circle(sc, pygame.Color("red"),
                               (snake[-2][0] + SIZE // 2 - 10, snake[-2][1] + SIZE // 2), Game.__rad_of_eyes)
            pygame.draw.circle(sc, pygame.Color("red"),
                               (snake[-2][0] + SIZE // 2 + 10, snake[-2][1] + SIZE // 2), Game.__rad_of_eyes)
        else:
            pygame.draw.circle(sc, pygame.Color("red"),
                               (indexes[0] + SIZE // 2 - 10, indexes[1] + SIZE // 2), Game.__rad_of_eyes)
            pygame.draw.circle(sc, pygame.Color("red"),
                               (indexes[0] + SIZE // 2 + 10, indexes[1] + SIZE // 2), Game.__rad_of_eyes)

    def start_the_game():
        RES = Game.__size_of_field
        SIZE = Game.__size_of_object
        END = 200
        number_of_clouds = 4
        x, y = randrange(0, RES, SIZE), randrange(0, RES, SIZE)
        apple = randrange(0, RES, SIZE), randrange(0, RES, SIZE)
        cloud = [[], [], [], []]
        for i in range(number_of_clouds):
            cloud[i].append((randrange(0, RES, SIZE), randrange(0, RES, SIZE)))
            if cloud[i][0] == apple:
                cloud[i][0] = (cloud[i][0][0] + SIZE, cloud[i][0][1])
            cloud[i].append((cloud[i][0][0] + SIZE, cloud[i][0][1]))
        length = 1
        snake = [(x, y)]
        score = 0
        dx, dy = 0, 0
        fps = 8

        sc = pygame.display.set_mode([RES, RES])
        clock = pygame.time.Clock()
        font_end = pygame.font.SysFont('Arial', 70, bold=True)

        while True:
            sc.fill(pygame.Color('blue'))

            Game.set_colors(sc, SIZE, snake, apple, score, cloud)

            pre_for_one = (x, y)
            x += dx * SIZE
            y += dy * SIZE
            snake.append((x, y))
            snake = snake[-length:]

            if snake[-1] == apple:
                apple = randrange(0, RES, SIZE), randrange(0, RES, SIZE)
                length += 1
                score += 1
                fps += 0.5

            in_cloud = False
            for clouds in cloud:
                if clouds[0] == snake[-1] or clouds[1] == snake[-1]:
                    Game.red_eyes(pre_for_one, len(snake), snake, sc, SIZE)
                    render_end = font_end.render('GAME OVER', 1, pygame.Color('orange'))
                    sc.blit(render_end, (RES // 2 - END, RES // 3))
                    pygame.display.flip()
                    time.sleep(3)
                    in_cloud = True
                    break
            if in_cloud == True:
                break


            if x < 0 or x > RES - SIZE or y < 0 or y > RES - SIZE or len(snake) != len(set(snake)):
                Game.red_eyes(pre_for_one, len(snake), snake, sc, SIZE)
                render_end = font_end.render('GAME OVER', 1, pygame.Color('orange'))
                sc.blit(render_end, (RES // 2 - END, RES // 3))
                pygame.display.flip()
                time.sleep(3)
                break

            pygame.display.flip()
            clock.tick(fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        return

            dx, dy = Game.pressing_the_button(dx, dy)

        Game.best_scores((str(Game.write_name()), score));

    def records():
        value_gap = 200
        value_x = 350
        value_y = 250
        sc = pygame.display.set_mode([Game.__size_of_field, Game.__size_of_field])
        clock = pygame.time.Clock()
        fps = 8
        sqlite_connection = sqlite3.connect('sqlite_python.bd')
        cursor = sqlite_connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS snake_records(
                   name TEXT,
                   score INTEGER);
                """)
        cursor.execute("""
                SELECT name, max(score) score from snake_records
                GROUP by name
                ORDER by score DESC
                limit 5
                """)
        records = cursor.fetchmany(5)
        while True:
            x, y = value_x, value_y
            sc.fill(pygame.Color('blue'))
            my_font = pygame.font.SysFont('Comic Sans MS', 30)
            for row in records:
                text_surface = my_font.render(f'Name: {row[0]}', 1, ("yellow"))
                sc.blit(text_surface, (x, y))
                text_surface = my_font.render(f'Score: {row[1]}', 1, ("yellow"))
                sc.blit(text_surface, (x + value_gap, y))
                y += value_gap // 2
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        #pygame.quit()
                        return
            pygame.display.update()
            clock.tick(fps)
        cursor.close()


    _menu.add.button('Play', start_the_game)
    _menu.add.button('Quit', pygame_menu.events.EXIT)
    _menu.add.button('RECORDS', records)
    def run(self):
        self._menu.mainloop(self._surface)

play_snake = Game()
play_snake.run()
