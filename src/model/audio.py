import pygame

from pygame import mixer
import time
from src.model.player import Playlist
play_list_default = Playlist(play_list_name='Default',music_folder = (r"music_folder"))


mixer.init()
track = play_list_default.popTrack()
print(track)
mixer.music.load(track)
mixer.music.play()




def end():
    try:
        pygame.init()
        random_muz = play_list_default.popTrack()
        print(random_muz)
        # random_muz = random_muze_choice()

        song = pygame.mixer.Sound(random_muz)

        song.set_volume(0.30)

        clock = pygame.time.Clock()
        song.play()

        run = 9
        while run != 0:
            clock.tick(1)
            time.sleep(1)
            run -= 1

        pygame.quit()
    except:
        pass
    finally:
        pass

end()