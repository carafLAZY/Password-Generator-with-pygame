import pyperclip
import pygame
import string
import random
import os

pygame.init()
pygame.font.init()
pygame.sysfont.initsysfonts()

width, height = 720, 720
fps = 60
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.display.set_caption('Password Generator')

font_sys = pygame.font.SysFont('Arial', 40)
length_font_sys = pygame.font.SysFont('Arial', 200)

def sys_text(text, x, y):
    text = font_sys.render(text, True, (0, 0, 0))
    screen.blit(text, (x, y))

def length_text(text, x, y):
    text = length_font_sys.render(text, True, (0, 0, 0))
    screen.blit(text, (x, y))

def password_gen(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''
    max = 22

    length_a_number = str(length).isdigit()
    
    if length_a_number == True:
        length_num = int(length)
        if length_num > 22:
            password = f'Lower than {max} or {max}'
        
        if length_num <= 22:
            for ex in range(length_num):
                password += random.choice(characters)
        return password

    if length_a_number == False:
        password = 'Please put only a number'
        return password

def main():
    flicker = [500, False]
    length_rect = pygame.Rect(200, 100, 300, 300)
    file_rect = pygame.Rect(584, 562, 30, 30)
    length_value = 15
    length = length_value
    time_flash = pygame.time.get_ticks()
    clicked = True
    generator_switch = False
    password = password_gen(length_value)
    box_color_1 = (99, 99, 99)
    file_turn = [0, 1]
    file_storing = []
    no_duplicate_system = [0, 0]
    box_color2 = (234, 255, 0)
    storing_trigger = False
    
    run = True
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        mouse_x, mouse_y = pygame.mouse.get_pos()
        elapsed_time_flash = pygame.time.get_ticks() - time_flash

        #Flick animation
        if elapsed_time_flash >= flicker[0]:
            time_flash = pygame.time.get_ticks()
            length = ''
            flicker[1] = not flicker[1]
        if flicker[1] == False:
            length = length_value
        #Flick animation -end
        
        #Create file function
        for file in range(file_turn[1]):
            if os.path.exists(f'{file_turn[0]}.txt'):
                print(f'{file_turn[0]}.txt exists')
                file_turn[0] += 1
            else:
                file_turn[1] -= 1
                createFile = open(f"{file_turn[0]}.txt", 'x')
                print('None')
        
        #Anti duplicate
        if not no_duplicate_system[0] == no_duplicate_system[1] and storing_trigger == True:
            no_duplicate_system[0] = no_duplicate_system[1]
            OpenTxtFile = open(f"{file_turn[0]}.txt", 'w')
            file_storing.append(no_duplicate_system[0])
                
            for texts in file_storing:
                to_file = texts + '\n'
                OpenTxtFile.write(to_file)
                
            OpenTxtFile.close()
            print(file_storing)
            storing_trigger = False

        if not no_duplicate_system[0] == no_duplicate_system[1]:
            box_color2 = (234, 255, 0)
        if no_duplicate_system[0] == no_duplicate_system[1]:
            box_color2 = (190, 190, 190)
        #Create file func--end
        
        #Rects
        if length_rect.collidepoint(mouse_x, mouse_y):
            flicker[1] = False
            if pygame.mouse.get_pressed()[0] == True and clicked == True:
                length_value += 1
                clicked = False
                generator_switch = True
            if pygame.mouse.get_pressed()[2] == True and clicked == True:
                length_value -= 1
                clicked = False
                generator_switch = True
            if pygame.mouse.get_pressed()[1] == True and clicked == True:
                clicked = False
                generator_switch = True
        
        if file_rect.collidepoint(mouse_x, mouse_y):
            if pygame.mouse.get_pressed()[0] == True and clicked == True:
                storing_trigger = True
                clicked = False
        
        if pygame.mouse.get_pressed()[0] == False and pygame.mouse.get_pressed()[2] == False and pygame.mouse.get_pressed()[1] == False:
            clicked = True
        #Rects --end
            
        #min and max
        if length_value <= 0:
            length_value = 0
        if length_value >= 22:
            length_value = 22
        #min max -- end
        if generator_switch == True:
            password = password_gen(length_value)
            generator_switch = False
        
        no_duplicate_system[1] = password
        pyperclip.copy(password)
        screen.fill((190, 190, 190))
        pygame.draw.rect(screen, box_color_1, (200, 100, 300, 300))
        pygame.draw.rect(screen, box_color2, (584, 562, 30, 30))
        pygame.draw.rect(screen, box_color_1, (100, 480, 520, 75))
        sys_text(f'Storing on {file_turn[0]}.txt', 10, 10)
        length_text(str(length), 230, 140)
        sys_text(str(password), 120, 490)
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()