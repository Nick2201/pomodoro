import pygame

# clock = pygame.time.Clock()
# seconds_remaining = 30
# while seconds_remaining > 0:
#     clock.tick(1)
#     minutes = seconds_remaining // 60
#     seconds = seconds_remaining % 60
#     timer_str = '{:02d}:{:02d}'.format(minutes, seconds)
#     print(timer_str, end='\r')
#     time.sleep(1)
#     seconds_remaining -= 1
seconds_remaining = 30
start_ticks=pygame.time.get_ticks() #starter tick
while seconds_remaining != 0: # mainloop
    seconds=(pygame.time.get_ticks()-start_ticks)/1000 #calculate how many seconds
    if seconds>10: # if more than 10 seconds close the game
        break
    print(seconds)