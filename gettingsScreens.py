from screeninfo import get_monitors

def get_screen_info():
    screen_info = []
    for i, monitor in enumerate(get_monitors(), 1):
        name = monitor.name.replace("\\\\.\\", "")
        width = monitor.width
        height = monitor.height
        screen_info.append((i, name, width, height))
    return screen_info