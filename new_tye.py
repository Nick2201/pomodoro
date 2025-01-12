import time
import datetime
import threading
import random
import os

import pygame
################################################################################
# Пример упрощённого класса Playlist, который хранит пути к трекам из некоторой папки
################################################################################
class Playlist:
    def __init__(self, music_folder: str):
        """
        music_folder (str): Путь к папке с треками.
        """
        self.music_folder = music_folder
        # Найдём все mp3-файлы в папке (можете добавить wav и т.п.)
        self.tracks = [
            os.path.join(self.music_folder, f)
            for f in os.listdir(self.music_folder)
            if f.endswith('.mp3')
        ]
    
    def popTrack(self):
        """
        Возвращает случайный трек из списка (удобно, если хотим «удалять» его из набора).
        Если нужно просто случайный трек без удаления, используйте random.choice(self.tracks).
        """
        if not self.tracks:
            raise ValueError("Нет треков в плейлисте!")
        track = random.choice(self.tracks)
        # Можно либо удалять трек из списка, либо оставить (если хотим переиспользовать)
        # self.tracks.remove(track)
        return track

################################################################################
# Функция для асинхронного запуска воспроизведения трека (чтобы не блокировать таймер)
################################################################################

def play_random_track_async(
        playlist: Playlist, 
        volume_level=0.1, 
        play_duration=None
        )->None: # multithreading
    """
    - playlist: объект типа Playlist (у которого есть метод popTrack()).
    - volume_level: громкость (0.0 ... 1.0).
    - play_duration: Если хотим ограничить воспроизведение, указываем (в секундах).
                     Если None, то трек будет играть полностью.
    """
    def _play():
        pygame.mixer.init()
        track_file = playlist.popTrack()
        sound = pygame.mixer.Sound(track_file)
        sound.set_volume(volume_level)
        channel = sound.play()  # Запускаем
        if play_duration is not None:
            # Спим нужное количество секунд
            time.sleep(play_duration)
            # Останавливаем воспроизведение
            channel.stop()
        else:
            # Если play_duration=None, ждём пока звук не перестанет играть
            while channel.get_busy():
                time.sleep(0.2)

        # Отключаем микшер (по желанию, если в дальнейшем не нужно)
        pygame.mixer.quit()

    # Запуск в отдельном потоке
    threading.Thread(target=_play, daemon=True).start()

################################################################################
# Классы Box и TimeBlock (логика таймера)
################################################################################
class Box:
    """
    Базовый класс для любого временного блока (Work, Rest и т.д.).
    
    Параметры:
        name (str): Название блока.
        duration_minutes (float): Длительность блока (в минутах).
        attention (bool): Нужно ли предупреждение о скором окончании.
        attention_delta (float): За сколько минут до конца предупреждать (если attention=True).
    """
    def __init__(self, name, duration_minutes, attention=True, attention_delta=1.0):
        self.name = name
        self.duration_minutes = duration_minutes
        self.attention = attention
        self.attention_delta = attention_delta

    def __repr__(self):
        return f"{self.name}({self.duration_minutes} min)"

class TimeBlock:
    """
    Последовательность Box'ов (например, [Work, Rest, Work, Meal...]).
    """
    def __init__(self, boxes, playlist=None, start_time=None):
        """
        boxes (list of Box): Список Box'ов.
        playlist (Playlist or None): Плейлист с треками (если хотим включать музыку).
        start_time (datetime or None): Если None, то таймер начнётся "сейчас".
        """
        self.boxes = boxes
        self.playlist = playlist
        self.start_time = start_time or datetime.datetime.now()
        self.completed_works = 0  # Счетчик завершенных задач Work
        self.total_works = sum(1 for box in boxes if box.name == "Work")  # Всего Work блоков

    def run(self):
        """
        Основной цикл: перебираем Box'ы по очереди и «крутим» их.
        """
        current_start = self.start_time
        
        for i, box in enumerate(self.boxes):
            # Определим название следующего Box (или '---', если нет)
            next_box_name = self.boxes[i+1].name if i < len(self.boxes) - 1 else "---"

            # Пример: при старте каждого Box - проигрываем случайный трек (3 секунды)
            # Если не нужно, можно закомментировать.
            # if self.playlist:
            #     play_random_track_async(self.playlist, volume_level=0.3, play_duration=3)

            # Запускаем «отсчёт» для одного Box
            self._run_single_box(box, next_box_name)

            # Обновляем start_time (необязательно, здесь больше «логический» шаг)
            current_start = datetime.datetime.now()
        print()
        # В конце всех блоков — например, тоже можно запустить музыку
        if self.playlist:
            play_random_track_async(self.playlist, volume_level=0.3, play_duration=3)
        print("\n=== Все блоки завершены! ===")
    def get_info_about_block(self):
        # Общая информация
        total_duration = self.get_total_duration()
        total_works = self.get_total_works()

        # Словарь для информации обо всех уникальных блоках
        unique_boxes_info = {}
        for box in self.boxes:
            if box.name not in unique_boxes_info:
                unique_boxes_info[box.name] = {
                    "total_time": 0,  # Суммарное время для данного типа блока
                    "count": 0       # Количество блоков данного типа
                }
            unique_boxes_info[box.name]["total_time"] += box.duration_minutes
            unique_boxes_info[box.name]["count"] += 1

        # Округляем значения в unique_boxes_info
        for box_name, info in unique_boxes_info.items():
            info["total_time"] = round(info["total_time"])

        # Финальный словарь
        info_dict = {
            "total_duration": round(total_duration),
            "total_works": round(total_works),
            "unique_boxes_info": unique_boxes_info
        }

        # Возвращаем JSON
        from tabulate import tabulate

        table_data = [
            {
                "Название блока": name,
                "Общее время (мин)": round(info["total_time"]),
                "Количество": info["count"],
                "% времени": f"{(info['total_time'] / total_duration) * 100:.2f}%"
            }
            for name, info in unique_boxes_info.items()
        ]

        # Преобразование в таблицу
        table_output = tabulate(table_data, headers="keys", tablefmt="grid")

        # Финальная информация
        info_dict = {
            "total_duration": round(total_duration),
            "total_works": round(total_works)
        }

        # Выводим общую информацию и таблицу
        print("Общая информация:")
        print(tabulate(info_dict.items(), headers=["Параметр", "Значение"], tablefmt="grid"))

        print("\nДетали по уникальным блокам:")
        print(table_output)
# f"""
# Всего блоков    : {len(self.boxes)},\n 
# Всего минут     : {round(total_duration)},\n
# Всего работ     : {round(total_works)}\n
# Время на работу : {round(work_box_time)}"""

    def get_total_duration(self):
        total_duration = sum(box.duration_minutes for box in self.boxes)
        return total_duration
    def get_total_works(self):
        total_works = sum(1 for box in self.boxes if box.name == "Work")
        return total_works
    
    def _run_single_box(self, box, next_box_name):
        """
        Отсчитываем время одного Box. Каждую секунду:
        {Время начала Box} | {Название Box} | {минуты:секунды осталось} | {следующий Box} | {выполнено/всего}
        """
        duration_seconds = box.duration_minutes * 60
        start_time_box = time.time()
        start_time_str = datetime.datetime.now().strftime('%H:%M')

        attention_beep_done = False
        
        print(f"Start: [ {start_time_str} ]")

        while True:
            elapsed = time.time() - start_time_box
            if elapsed >= duration_seconds:
                # Если блок завершен, увеличиваем счетчик выполненных задач, если это Work
                if box.name == "Work":
                    self.completed_works += 1
                break

            remain = duration_seconds - elapsed
            minutes_left = int(remain // 60)
            seconds_left = int(remain % 60)

            remain_if_str = ""
            if box.attention and remain < (box.attention_delta * 60):
                remain_if_str = "soon end"
                if not attention_beep_done and self.playlist:
                    play_random_track_async(self.playlist, volume_level=0.3, play_duration=2)
                    attention_beep_done = True

            # Формируем строку
            works_left = self.total_works - self.completed_works
            percent_done = round(self.completed_works / self.total_works) * 100
            out_str = (
                f"{box.name} | "
                f"{minutes_left:02d}:{seconds_left:02d} | "
                f"{next_box_name} | "
                f"{remain_if_str} | "
                f"{self.completed_works}/{self.total_works} |"
                f"Done: {percent_done}% | "
                f"Remaining: {works_left}"
            )

            print(out_str, end='\r', flush=True)
            time.sleep(1)

        # Перевод строки, чтобы зафиксировать результат
        print()


################################################################################
# Пример использования
################################################################################

if __name__ == "__main__":
    # 1) Создадим плейлист (укажите папку с mp3):
    my_playlist = Playlist(music_folder = (r"src/model/music_folder"))  # Папка, где лежат some1.mp3, some2.mp3 и т.д.

    work = Box("Work", 13.958323867987747,  attention_delta=0.3)  # ~6 секунд
    rest = Box("Rest", 5.999999999999978,  attention_delta=0.5)  # ~3 секунды
    big_rest = Box("BigRest", 12.0, attention_delta=0.2)  # ~6 сек.
    meal = Box("Meal", 22,  attention_delta=0.2)
    think = Box("Think", 2.791666666666275, attention_delta=0.2)
    # 3) Собираем воедино в TimeBlock
    my_block = TimeBlock(
        boxes=[
                work,think,
                work,think,rest,
                work,think,
                work,think,big_rest,
                work,think,
                work,think,rest,
                work,think,
                work,think,meal
            ],
        playlist=my_playlist  # Можно передать None, если музыка не нужна
    )
    total_duration_seconds = my_block.get_total_duration()
    total_duration_minutes = total_duration_seconds / 60
    my_block.get_info_about_block()
    print(total_duration_minutes )

    # 4) Запускаем
    my_block.run()

   
