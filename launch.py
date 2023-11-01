import datetime,time


import pygame ,random
import os, itertools

# 3. Fitch with iter(dosen't work - why????)
# 4. 6:24| Now  16. work | Next  13 work ???
#Fitches
#1. % pass

# IndexError: list index out of range
from src.model.player import Playlist

play_list_default = Playlist(play_list_name='Default',music_folder = (r"C:\Users\nickl\My_softwares\another\Pomodoro_new\src\model\music_folder"))


def play_random_track(track_list=play_list_default,volume_level=0.1):
    """Plays a randomly chosen track from the given list using Pygame."""
    pygame.init()
    try:
        track_file = track_list.popTrack()  # or: random.choice(track_list)
        song = pygame.mixer.Sound(track_file)
        song.set_volume(volume_level)

        clock = pygame.time.Clock()
        song.play()

        seconds_remaining = 9
        while seconds_remaining > 0:
            clock.tick(1)
            minutes = seconds_remaining // 60
            seconds = seconds_remaining % 60
            timer_str = '{:02d}:{:02d}'.format(minutes, seconds)
            print(timer_str, end='\r')
            time.sleep(1)
            seconds_remaining -= 1

    finally:
        pygame.quit()
# time_now = datetime.datetime.now()

track_time = 10  # 10
end_time = 9  # 9
meal = 60*22- track_time  # 1320  end_time -
work = 400- track_time  # 870  end_time - / 1320- track_time
rest = 360 - track_time  # 300  end_time -
big_rest = 12*60+120 - track_time  # end_time -
think_time = 200 - track_time


job_dict = {
    track_time: "track_time",
    end_time: "end_time",
    meal: "meal",
    work: "work",
    rest: "rest",
    big_rest: 'big_rest',
    think_time: 'think_time'}




job = [
    work,think_time,
    work,think_time,
    rest,
    work,think_time,
    work,think_time,
    rest,
    work,think_time,
    work,think_time,
    big_rest,

    work,think_time,
    work,think_time,
    rest,
    work,think_time,
    work,think_time,
    rest,
    work,think_time,
    work,think_time,
    meal
    ]


job_dict = {
    track_time: "track_time",
    end_time: "end_time",
    meal: "meal",
    work: "work",
    rest: "rest",
    big_rest: 'big_rest',
    think_time: 'think_time'}






rest_steps = itertools.count(1, 1)
count_work_count = itertools.count(1, 1)
big_rest_count = itertools.count(1, 1)
general_itertools = itertools.count(1, 1)
meal_count = itertools.count(1, 1)
think_time = itertools.count(1, 1)

steps = {'work': count_work_count,
         'rest': rest_steps,
         'big_rest': big_rest_count,
         'general': general_itertools,
         'meal': meal_count,
         'think_time':think_time}


def definitive_now_time(minutes: int):
    lista = []
    count = -1
    sec = minutes * 60
    while sec >= 0:
        count += 1
        sec = sec - job[count]
        lista.append(count)
    return count, lista


box_work = job.count(work)
print(box_work)

answer = input('Not Begin from 0? : ')
if answer == '+':
    need_to_convert_from_time = int(input('Write_time '))

    new_rule = definitive_now_time(need_to_convert_from_time)
    print([job_dict[job[x]] for x in new_rule[1][1:]])
    job = job[new_rule[0]:]
    count_work = job.count(work)
    percent = int(count_work / box_work * 100)
    print(f'Осталось {percent} % -- {count_work} из {box_work}')
else:
    pass

# def start(start_box = 0):

for index, job_box in enumerate(job):
    t = job_box
    now_count = next(steps[job_dict[job_box]])  #     next_episode = steps[job_dict[job_box]].__reduce__()[1][0]
    now_time = datetime.datetime.now().strftime('%H:%M:%S')
    if index < len(job) - 1:

        nex = steps[job_dict[job[index + 1]]].__reduce__()[1][0]
        now = steps[job_dict[job[index]]].__reduce__()[1][0]
    else:
        nex = 'stoooop!'

    if index < len(job) - 2:
        text = f'| {now_time} | {now_time} |Now  {index + 1}. {job_dict[job[index]]}  {now - 1} | Next  {nex} {job_dict[job[index + 1]]} '
    if index == len(job) - 1:
        text = f'| Now  {index + 1}. {now - 1} |  END'
    else:
        print('passed')

    while t:

        t -= 1
        mins = t // 60
        sec = t % 60
        timer = '{:02d}:{:02d}'.format(mins, sec)

        try:

            print("\r{0}".format(timer) + text, end='')

            time.sleep(1)
        except Exception as ex:
            print(ex)

        finally:
            pass

        if t == track_time:
            play_random_track()

            break
