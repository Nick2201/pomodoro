import time
import pygame
from typing import List, Tuple

def play_random_track(track_list):
    """Plays a randomly chosen track from the given list using Pygame."""
    pygame.init()
    try:
        track_file = track_list.popTrack()  # or: random.choice(track_list)
        song = pygame.mixer.Sound(track_file)
        song.set_volume(0.3)

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

def calculate_elapsed_time(job_durations: List[int]) -> Tuple[int, List[int]]:
    elapsed_time = sum(job_durations)
    job_indices = list(range(len(job_durations)))
    return elapsed_time, job_indices

# # Usage example:
# job_durations = [10, 20, 30]
# duration, job_indices = calculate_elapsed_time(job_durations)
# print(f"Elapsed time: {duration} s, job indices: {job_indices}")  # Elapsed time: 60 s, job indices: [0, 1, 2]

def process_time_input(
                    job_dict: dict,
                    job: list, work:
                    str,
                    box_work: int) -> None:

    if input('Not Begin from 0? : ') == '+':
        need_to_convert_from_time = int(input('Write_time '))

        # Calculate job sequence based on time
        elapsed_time, job_indices = calculate_elapsed_time(need_to_convert_from_time)
        job_sequence = job_indices[1:]
        print([job_dict[job[x]] for x in job_sequence])

        # Update job state and calculate completion percentage
        job = job[elapsed_time:]
        count_work = job.count(work)
        percent = compute_completion_percentage(count_work, box_work)
        print(f'Осталось {percent} % -- {count_work} из {box_work}')
    else:
        pass










import datetime
from enum import Enum
from typing import List, Tuple

class JobType(Enum):
    TRACK_TIME = 0
    END_TIME = 1
    MEAL = 2
    WORK = 3
    REST = 4
    BIG_REST = 5

# Define job durations in seconds
track_time = 10
end_time = 90
meal = 1_190 - track_time
work = 410 - track_time
rest = 290 - track_time
big_rest = 710 - track_time

# Define job dictionary with explicit job types
job_dict = {
    JobType.TRACK_TIME: track_time,
    JobType.END_TIME: end_time,
    JobType.MEAL: meal,
    JobType.WORK: work,
    JobType.REST: rest,
    JobType.BIG_REST: big_rest,
}

# Define a function to generate a job sequence based on durations
def make_job_sequence(work_duration: int, rest_duration: int, big_rest_duration: int, meal_duration: int) -> List[int]:
    sequence = []
    for _ in range(4):
        sequence.extend([work_duration, work_duration, work_duration, work_duration, rest_duration])
    sequence.extend([work_duration, work_duration, work_duration, big_rest_duration])
    for _ in range(4):
        sequence.extend([work_duration, work_duration, work_duration, work_duration, rest_duration])
    sequence.extend([work_duration, work_duration, work_duration, work_duration, meal_duration])
    return sequence

# Example usage
now_time = datetime.datetime.now().strftime('%H:%M:%S')
job = make_job_sequence(work, rest, big_rest, meal)
print(now_time, job_dict)
print(job)