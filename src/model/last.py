import datetime
import time

class JobScheduler:
    def __init__(self, jobs, steps, job_dict, track_time):
        self.jobs = jobs
        self.steps = steps
        self.job_dict = job_dict
        self.track_time = track_time

    def run(self):
        for index, job_box in enumerate(self.jobs):
            job = Job(job_box, self.steps, self.job_dict)

            if index < len(self.jobs) - 1:
                next_job_box = self.jobs[index + 1]
                next_job_name = self.job_dict[next_job_box]
                next_job_time = self.steps[next_job_name].__reduce__()[1][0]
                job.set_next_job_time(next_job_time, next_job_name)
            else:
                job.set_next_job_time(0, 'end')

            job.start()

            if job.get_remaining_time() == self.track_time:
                job.end()

class Job:
    def __init__(self, job_box, steps, job_dict):
        self.current_job_time = steps[job_dict[job_box]].__reduce__()[1][0]
        self.job_name = job_dict[job_box]
        self.next_job_time = None
        self.next_job_name = None
        self.remaining_time = int(job_box)  # ensure that remaining_time is an integer

    def set_next_job_time(self, next_job_time, next_job_name):
        self.next_job_time = next_job_time
        self.next_job_name = next_job_name

    def get_remaining_time(self):
        return self.remaining_time

    def start(self):
        while self.remaining_time:
            self.remaining_time = str(int(self.remaining_time) - 1)  # convert to int, subtract 1, and convert back to str
            mins = int(self.remaining_time) // 60  # convert to int here as well
            sec = int(self.remaining_time) % 60  # convert to int here as well
            timer = '{:02d}:{:02d}'.format(mins, sec)

            status_text = self.get_status_text()

            try:
                print("\r{0}".format(timer) + status_text, end='')
                time.sleep(1)
            except Exception as ex:
                print(ex)
            finally:
                pass

            if self.remaining_time == '0':
                self.end()

    def get_status_text(self):
        if self.next_job_time is None or self.next_job_name is None:
            return f'| Now  {self.job_name} {self.current_job_time - 1} |  END'

        return f'| Now {self.job_name} {self.current_job_time - 1} | Next {self.next_job_name} {self.next_job_time}'

    def end(self):
        print(f'\nJob {self.job_name} is finished\n')

now_time = datetime.datetime.now().strftime('%H:%M:%S')
track_time = 10  # 10
end_time = 90  # 90
meal = 1_190 - track_time  # 1320  end_time -
work = 410 - track_time  # 870  end_time -
rest = 290 - track_time  # 300  end_time -
big_rest = 710 - track_time




if __name__ == '__main__':
    jobs = [
    work,work,work,work,rest,
    work,work,work,work,rest,
    work,work,work,big_rest,
    work,work,work,work,rest,
    work,work,work,work,meal
    ]

    job_dict = {track_time: "track_time", end_time: "end_time", meal: "meal", work: "work", rest: "rest",
            big_rest: 'big_rest'}

    steps = {'work': count_work_count,
         'rest': rest_steps,
         'big_rest': big_rest_count,
         'general': general_itertools,
         'meal': meal_count}

    scheduler = JobScheduler(jobs, steps, job_dict, track_time)
    scheduler.run()