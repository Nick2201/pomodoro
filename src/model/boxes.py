from abc import abstractclassmethod


hour_box = {
    'track_time' :  10,
    'end_time' :  90,
    'meal' :  60*22,
    'work' :  600,
    'rest' :  360,
    'big_rest' :  12*60+120,
    'think_time' :  300,
}

box_queue = [
    hour_box['work']*2,
    hour_box['rest'],
    hour_box['rest'],
    hour_box['work']*2,

    hour_box['big_rest']*1,

    hour_box['work']*2,
    hour_box['rest'],
    hour_box['work']*2,
    hour_box['rest'],
    hour_box['work']*2,

    hour_box['meal']*1,
 ]
hour_sec = 60*60*3
# print(f'{sum(box_queue)} | {hour_sec} | {hour_sec-sum(box_queue)}')

# class TimeBox:
#     # Interface
#     @abstractclassmethod
#     def end():
# TASK: 
import multiprocessing
from tqdm import tqdm
import time
def play_music(time_play):

    print("Playing music...",end='\n')
    time.sleep(time_play)
    print("Music stopped",end='\n')



class TimeBox:
    def __init__(self, interval, name, main=True, mus_time=2):
        self.interval = interval
        self.name = name
        self.main = main
        self.mus_time = mus_time
    def run(self):
        pass


class Plan:
    def __init__(self, *timeboxes):
        self.sequence = []
        for timebox in timeboxes:
            self.sequence.append(timebox)
        self.soon_end = max([tb.interval for tb in timeboxes])

    def add_seq(self, sequence):
        for tb in sequence:
            self.sequence.append(tb)
            self.soon_end += tb.interval

    def run(self):
        for timebox in self.sequence:
            timebox.run()



class Pom_unit:
    def __init__(self, timeboxes):
        self.timeboxes = timeboxes
        self.full_time = sum([i.interval for i in timeboxes])

    def run(self,mus_time=2):
        for timebox in self.timeboxes:
            timme_box = timebox.interval

            for i in tqdm(range(timebox.interval), desc=f"{timebox.name}"):
                time.sleep(1)
                timme_box -= 1

                if timme_box == mus_time:
                    music_process = multiprocessing.Process(target=play_music, args=(mus_time,))
                    music_process.start()



if __name__ == '__main__':
    job = TimeBox(interval=8, name='job', main=True)
    rest = TimeBox(interval=6, name='rest', main=True)
    # soon_end = 40
    # play_music_time =TimeBox(interval=2, name='rest', main=True)
    # play_music_time = 2

    plan_test = Plan(job)

    pom_unit = [job, job, rest, job]
    plan_test.add_seq(pom_unit)
    tb = Pom_unit(timeboxes=[job, job, rest, job])

    main_proc = multiprocessing.Process(target=tb.run)
    # Запускаем процессы
    main_proc.start()

    # Ждем, пока оба процесса завершатся
    main_proc.join()



    print("Both processes have finished")


