import pgzrun
from pgzero.actor import Actor 
import math
import random 

WIDTH = 800
HEIGHT = 600
TITLE = "Era do Gelo"

game_state = "menu"
sound_on = True


start_button = Rect((WIDTH/2 - 100, 250), (200, 50))
sound_button = Rect((WIDTH/2 - 100, 320), (200, 50))
exit_button = Rect((WIDTH/2 - 100, 390), (200, 50))
play_again_button = Rect((WIDTH/2 - 100, 320), (200, 50))

#classe do jogador- sid
class Player: 
    def __init__(self, idle_frames, walk_frames, pos, speed):
        self.idle_frames = idle_frames
        self.walk_frames = walk_frames
        self.actor = Actor(self.idle_frames[0], pos)
        self.speed = speed
        self.destination = pos
        self.anim_timer = 0.0
        self.idle_speed = 0.8
        self.walk_speed = 0.1
        self.current_frame = 0
        self.is_walking = False

    def update(self, dt):
        dx = self.destination[0] - self.actor.x
        dy = self.destination[1] - self.actor.y
        dist = math.hypot(dx, dy)
        if dist > 2:
            self.is_walking = True 
            dir_x = dx / dist
            dir_y = dy / dist 
            self.actor.x += dir_x * self.speed * dt
            self.actor.y += dir_y * self.speed * dt
        else:
            self.is_walking = False 
            self.actor.pos = self.destination
        self.update_animation(dt) 

    def update_animation(self, dt):
        self.anim_timer += dt
        active_animation = self.walk_frames if self.is_walking else self.idle_frames 
        speed = self.walk_speed if self.is_walking else self.idle_speed

        if self.anim_timer < speed:

            return
        self.anim_timer = 0.0
        self.current_frame = (self.current_frame + 1) % len(active_animation)
        self.actor.image = active_animation[self.current_frame]
    
    def draw(self):
        self.actor.draw()
        
    def go_to(self, pos):
        self.destination = pos
        
    def reset(self, pos): 
        self.destination = pos
        self.actor.pos = pos
        self.is_walking = False


# classe do capitão entranha--inimigo
class Enemy:
    def __init__(self, move_frames, pos, speed):
        self.move_frames = move_frames
        self.actor = Actor(self.move_frames[0], pos)
        self.speed = speed
        self.anim_timer = 0.0
        self.anim_speed = 0.15
        self.current_frame = 0
        self.patrol_distance = random.randint(100, 200)
        self.patrol_start_x = pos[0]
        self.direction = 1

    def update(self, dt):
        self.actor.x += self.direction * self.speed * dt
        if self.actor.x > self.patrol_start_x + self.patrol_distance:
            self.direction = -1
        elif self.actor.x < self.patrol_start_x - self.patrol_distance:
            self.direction = 1
        self.update_animation(dt)

    def update_animation(self, dt):
        self.anim_timer += dt
        if self.anim_timer < self.anim_speed:
            return
        self.anim_timer = 0.0
        self.current_frame = (self.current_frame + 1) % len(self.move_frames)
        self.actor.image = self.move_frames[self.current_frame]

    def draw(self):
        self.actor.draw()
        

player = Player(
    idle_frames=["sid_idle_0","sid_idle_1"],
    walk_frames=["sid_walk_1", "sid_walk_2", "sid_walk_3"], 
    pos=(60, HEIGHT - 50),
    speed=100
)
enemies = [] 
goal = Actor("sid_friends", (WIDTH - 120, 60))

def start_music():
    if sound_on:
        music.play("background_music") 
        music.set_volume(0.3)

def toggle_music():
    if sound_on:
        music.unpause()
    else:
        music.pause()

def stop_game():
    music.stop()


def draw_menu():
    screen.draw.text("Ajude o Sid a chegar aos seus amigos!", center=(WIDTH/2, 150), fontsize=40, color="white")
    screen.draw.filled_rect(start_button, "green")
    screen.draw.text("Iniciar", center=start_button.center, fontsize=30, color="black")
    sound_text = "Som: LIGADO" if sound_on else "Som: DESLIGADO"
    color = "yellow" if sound_on else "gray"
    screen.draw.filled_rect(sound_button, color)
    screen.draw.text(sound_text, center=sound_button.center, fontsize=30, color="black")
    screen.draw.filled_rect(exit_button, "red")
    screen.draw.text("Sair", center=exit_button.center, fontsize=30, color="black")


def draw_win_screen():
    screen.draw.text(
        "VENCEU!", 
        center=(WIDTH/2, 150), 
        fontsize=60, 
        color="white"
    )
    screen.draw.text(
        "Sid encontrou seus amigos!", 
        center=(WIDTH/2, 250), 
        fontsize=40, 
        color="yellow"
    )
    
 
    screen.draw.filled_rect(play_again_button, "orange")
    screen.draw.text("Jogar Novamente", center=play_again_button.center, fontsize=30, color="black")


def start_game():
    global enemies
    player.reset(pos=(WIDTH / 2, HEIGHT - 50))
    enemies = []
    for i in range(5):
        new_enemy = Enemy(
            move_frames=["enemy_move_0", "enemy_move_1"],
            pos=(random.randint(100, WIDTH-100), random.randint(300, 400)),
            speed=random.randint(40, 80)
        )
        enemies.append(new_enemy)

    
    start_music() 




def draw():
    screen.clear()
    
    if game_state == "menu":
        draw_menu()
    elif game_state == "playing":
        screen.blit("background", (0, 0))
        player.draw()
        for enemy in enemies:
            enemy.draw()
        goal.draw()

        
    elif game_state == "win": 
        draw_win_screen() 


def on_mouse_down(pos):
    global game_state, sound_on

    if game_state == "menu":
        if start_button.collidepoint(pos):
            game_state = "playing"
            start_game()
        elif sound_button.collidepoint(pos):
            sound_on = not sound_on
            toggle_music()
        elif exit_button.collidepoint(pos):
            exit()
            
    elif game_state == "playing":
        player.go_to(pos)
    
    
    elif game_state == "win": 
        if play_again_button.collidepoint(pos):
            game_state = "menu" 

def update(dt):
    global game_state
    
    if game_state == "playing":
        player.update(dt)
        for enemy in enemies:
            enemy.update(dt)
            if player.actor.colliderect(enemy.actor):
                game_state = "menu"
                stop_game()
    
        if game_state == "playing":
            if player.actor.colliderect(goal): 
                game_state = "win" 
                stop_game()
                

pgzrun.go()