import os, random
from pathlib import Path

class Playlist:
    def __init__(self,
                 play_list_name:str,
                 music_folder):

        self.play_list_name = play_list_name
        self.abs_path = Path(music_folder)
        self.track_list = [track for track in self.abs_path.iterdir() if track.is_file()]


    def popTrack(self):
        now_muz = random.choice(self.track_list)
        self.track_list.remove(now_muz)
        return now_muz
    @property
    def info(self):
        print(len(self.track_list))


# play_list_default = Playlist(play_list_name='Default',)



