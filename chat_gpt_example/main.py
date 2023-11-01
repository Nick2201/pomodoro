import time
import pyglet



full_link = "https://drive.google.com/file/d/0B6AV35TIZFRcOEdxVGE0OWF2MU0/view?usp=share_link&resourcekey=0-ELRGr17EJjdZAPjgj0dxTg"
name = "0B6AV35TIZFRcOEdxVGE0OWF2MU0"
def pomodoro(work_time, break_time):
    for i in range(4):
        print(f"Starting Pomodoro #{i+1}")
        print(f"Working for {work_time} minutes")
        music = pyglet.media.load("https://drive.google.com/file/d/0B6AV35TIZFRcNDZ5dlgwb1RzY0E/download") # replace <file_id> with the actual file ID of your music file
        music.play()
        time.sleep(work_time * 60) # convert minutes to seconds
        music.pause()
        print("Take a break!")
        print(f"Breaking for {break_time} minutes")
        music = pyglet.media.load(f"https://drive.google.com/file/d/0B6AV35TIZFRcNDZ5dlgwb1RzY0E/download") # replace <file_id> with the actual file ID of your music file
        music.play()
        time.sleep(break_time * 60)
        music.pause()
    print("All Pomodoros completed for the day!")

# Example usage
pomodoro(25, 5)
# Example usage
# https://drive.google.com/drive/folders/0B6AV35TIZFRcWGhxX09rTGlpSTg?resourcekey=0-h3ZaX8jHL1oxfIf7jJheyg&usp=share_link

# https://drive.google.com/file/d/0B6AV35TIZFRcOEdxVGE0OWF2MU0/view?usp=share_link&resourcekey=0-ELRGr17EJjdZAPjgj0dxTg

# sheet_id = "1EdRAZftvonBQnaqEIOxodRv8MTE3dMh9PzoQpH3bfJU"

# df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")
# print(df)