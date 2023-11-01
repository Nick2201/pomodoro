import multiprocessing
from tqdm import tqdm
import time

class TimeBox:
    def __init__(self, interval, name):
        self.interval = interval
        self.name = name

    def run(self):
        for i in tqdm(range(self.interval), desc=f"{self.name}"):
            time.sleep(1)

def play_music(time_play):
    print("Playing music...")
    time.sleep(time_play)
    print("Music stopped")

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
        processes = []
        for timebox in self.sequence:
            pomodoro_process = multiprocessing.Process(target=self._run_timebox, args=(timebox,))
            music_process = multiprocessing.Process(target=play_music, args=(self.soon_end,))

            processes.extend([pomodoro_process, music_process])

            pomodoro_process.start()
            music_process.start()

        for process in processes:
            process.join()

    def _run_timebox(self, timebox):
        timebox.run()

if __name__ == '__main__':
    job = TimeBox(interval=7, name='job')
    rest = TimeBox(interval=3, name='rest')

    plan_test = Plan(job, rest)
    pom_unit = [job, job, rest, job]
    plan_test.add_seq(pom_unit)

    plan_test.run()
