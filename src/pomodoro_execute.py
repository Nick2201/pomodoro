import datetime,time

import pygame ,random
import os, \
    itertools



# Task#
# Bags:






# 3. Fitch with iter(dosen't work - why????)
# 4. 6:24| Now  16. work | Next  13 work ???
#Fitches
#1. % pass

# IndexError: list index out of range

def random_muze_choice():
    fold_name = r"C:\Users\nickl\nick_\ProjectsPy\Pomodoro_new\music_folder"
    names = os.listdir(os.path.abspath(fold_name))
    muzlo = []
    for name in names:
        fullname = os.path.join(os.path.abspath(fold_name), name)
        if os.path.isfile(fullname):
            muzlo.append(fullname)
    now_muz = random.choice(muzlo)

    return now_muz


def end():
    try:
        pygame.init()
        random_muz = random_muze_choice()
        song = pygame.mixer.Sound(random_muz)

        song.set_volume(0.30)

        clock = pygame.time.Clock()
        song.play()

        run = 9
        while run != 0:
            clock.tick(1)

            mins = t // 60
            sec = t % 60
            timer = '{:02d}:{:02d}'.format(mins, sec)
            # print("'\r{0}".format(timer) + ti, end='')
            time.sleep(1)
            run -= 1

        pygame.quit()
    except:
        pass
    finally:
        pass


time_now = datetime.datetime.now()

track_time = 10  # 10
end_time = 90  # 90
meal = 1560 - track_time  # 1320  end_time -
work = 420 - track_time  # 870  end_time -
rest = 180 - track_time  # 300  end_time -
big_rest = 600 - track_time  # end_time -
# job = [work, end_time, work, end_time, res] * 5 + [work, end_time, meal]

job_dict = {track_time: "track_time", end_time: "end_time", meal: "meal", work: "work", rest: "rest",
            big_rest: 'big_rest'}

job = [work, work, work, rest, work, work, work, rest, work, work, work, rest, work, work, big_rest, work, work, work,
       rest, work, work, work, rest, work, work, meal, ]


rest_steps = itertools.count(1, 1)
count_work_count = itertools.count(1, 1)
big_rest_count = itertools.count(1, 1)
general_itertools = itertools.count(1, 1)
meal_count = itertools.count(1, 1)

steps = {'work': count_work_count,
         'rest': rest_steps,
         'big_rest': big_rest_count,
         'general': general_itertools,
         'meal': meal_count}


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
    if index < len(job) - 1:

        nex = steps[job_dict[job[index + 1]]].__reduce__()[1][0]
        now = steps[job_dict[job[index]]].__reduce__()[1][0]
    else:
        nex = 'stoooop!'

    if index < len(job) - 2:
        text = f'| Now  {index + 1}. {job_dict[job[index]]}  {now - 1} | Next  {nex} {job_dict[job[index + 1]]} '
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
            end()

            break
