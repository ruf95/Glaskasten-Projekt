import math
import pygame
import os
import subprocess
import sys
from pathlib import Path

SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080 
CURRENT_COVER_HEIGHT, CURRENT_COVER_WIDTH = 810, 546 #Anzeigegröße der Spielcover bei Auswahl
BG_COVER_HEIGHT, BG_COVER_WIDTH = 656, 441 #Anzeigegröße der Spielcover im Hintergrund
COVER_POS_X, COVER_POS_Y = 960, 540
SPACING = 525 #Abstand zwischen den Spielen
SCRIPT_PATH = Path(__file__).parent #Pfad in dem sich das Skript befindet
COVER_PATH = SCRIPT_PATH / "Cover" #Hat den Pfad zum Cover-Ordner
ANIMATIONSPEED = 0.08
GAME_PATH = SCRIPT_PATH / "Games"
running = True

pygame.init()
clock = pygame.time.Clock()


class GameEntry:
    def __init__(self, title, current_cover_surface, bg_cover_surface, game_path):
        self.title = title
        self.current_cover_surface = current_cover_surface
        self.bg_cover_surface = bg_cover_surface
        self.game_path = game_path
        
        
def game_loader (COVER_PATH, GAME_PATH):
    image_formats = {'.png', '.jpg', '.jpeg', '.bmp'} #Zugelassene Formate
    game_format = {'.py'}
    
    covers = {f.stem: f for f in COVER_PATH.iterdir() if f.is_file() and f.suffix.lower() in image_formats} #Checkt nach Covern
    games  = {f.stem: f for f in GAME_PATH.iterdir()  if f.is_file() and f.suffix.lower() in game_format}
    
    print("Found covers:", list(covers.keys()))
    print("Found games:", list(games.keys()))
    
    loaded_games = []
    for name in games:
        if name in covers:                                      #Checkt ob Name von Games auch in Cover enthalten
            cover_surface = pygame.image.load(str(covers[name])) #Lädt das Cover
            current_cover_surface = pygame.transform.scale(             #Skaliert das Cover
                cover_surface, (CURRENT_COVER_WIDTH, CURRENT_COVER_HEIGHT))
            bg_cover_surface = pygame.transform.scale(             #Skaliert das Cover kleiner
                cover_surface, (BG_COVER_WIDTH, BG_COVER_HEIGHT))

            loaded_games.append(GameEntry(                              #Packt Games mit Name, Cover (groß/klein) & Pfad in Liste
                title=name,
                current_cover_surface = current_cover_surface,
                bg_cover_surface = bg_cover_surface,
                game_path=games[name]))

    return loaded_games

initialized_games = game_loader(COVER_PATH, GAME_PATH)

        
class picking_wheel:
    def __init__(self, game_list):
        self.game_list = initialized_games
        self.running = True
        self.target_index = 0 #Eigentliche neue Position der Cover
        self.current_scrol_pos = 0.0 #Jetzige Position der Cover
        self.animation_target = 0 #Punkt zu dem man immer hin animiert
        self.is_animating = False
        
        
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #Beendet Skript wenn Fenster geschlossen
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and not self.is_animating:
                # Lädt das nächste Cover
                    self.target_index = (self.target_index + 1) %len(self.game_list)
                    self.animation_target += 1
                    self.is_animating = True
         
                elif event.key == pygame.K_LEFT and not self.is_animating:
                # Lädt das vorherige Cover
                    self.target_index = (self.target_index - 1)%len(self.game_list)
                    self.animation_target -= 1
                    self.is_animating = True
                    
                elif event.key == pygame.K_ESCAPE and not self.is_animating:
                    #Beendet das Skript wenn ESC gedrückt wird
                    self.running = False
                elif event.key == pygame.K_RETURN and not self.is_animating:
                    #Wählt das Current Game aus
                    if self.game_list:
                        self.launch_game()
        return self.running

    def launch_game(self):
        current_game = self.game_list[self.target_index]
        current_game_path = str(current_game.game_path)
        
        try:
            print(f"Starte das Spiel: " ,{current_game.title})
            # Das Hauptskript (das Auswahlrad) wartet hier, bis das Spiel beendet ist.
            subprocess.run(
                [sys.executable, current_game_path],
                check=True,
                cwd=os.path.dirname(current_game_path) # Setzt das Arbeitsverzeichnis für das Spiel
            )
            print(f"Spiel beendet. Zurück im Auswahlrad.")

        except subprocess.CalledProcessError as e:
            print(f"Fehler beim Starten des Spiels ',{current_game.title}': {e}")
        except FileNotFoundError:
            print("Fehler: Das Spiel-Skript konnte nicht gefunden werden.")
        
    def update(self):
        #Wenn die Animation läuft bewege current_scrol_pos näher an animation_target
        if self.is_animating:
            diff = self.animation_target - self.current_scrol_pos #Differenz zwischen Ziel und aktueller Pos
            self.current_scrol_pos += diff * ANIMATIONSPEED     #Zwischenschrittberechnung
            
            if abs(diff) < 0.01:                                #Wenn aktuelle Pos nah genug an Ziel setze auf Ziel
                self.current_scrol_pos = self.animation_target
                self.is_animating = False                       #Deaktiviere Animationssequenz
    
    def draw(self, screen):
        screen.fill((30,30,30)) #Macht den Hintergrund schwarz
        
        # Sorgt dafür dass der Index nie zu groß oder zu klein wird
        len_games = len(self.game_list)     
        if len_games == 0: return           # Sicherheitscheck falls keine Spiele da sind

        left_index = (self.target_index - 1) % len_games
        right_index = (self.target_index + 1) % len_games
        
        left_game = self.game_list[left_index]
        right_game = self.game_list[right_index]
        
        #Offset für Animation berechnen
        offset_factor = self.current_scrol_pos - self.animation_target
        global_x_offset = offset_factor * SPACING
        
        range_of_covers = [-2, -1, 1, 2]
        
        for i in range_of_covers:
            index = (self.target_index + i) % len_games
            game = self.game_list[index]
            x_pos = COVER_POS_X + (i*SPACING) - global_x_offset #Verschiebt geladene Cover
            
            cover = game.bg_cover_surface
            rect = cover.get_rect(center=(x_pos, COVER_POS_Y))
            screen.blit(cover, rect)
        
        current_game = self.game_list[self.target_index]
        current_cover = current_game.current_cover_surface
        
        center_x = COVER_POS_X - global_x_offset
        center_rect = current_cover.get_rect(center=(center_x, COVER_POS_Y))
        screen.blit(current_cover, center_rect)
            
        
        
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #Setzt die Bildschirmgröße
    pygame.display.set_caption("Game Selection") #Setzt Titel des Fensters
    picker = picking_wheel(initialized_games) #Automatische Instanzierung der picking_wheel Klasse 


    while picker.running:
        if not picker.handle_input():
            break
        
        picker.update()
        picker.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    
    
if __name__ == "__main__":
    main()


