from settings.gamesettings import MAP_SIZE_X, MAP_SIZE_Y


FPS = 100
MS = int(1000 / FPS)
SCREEN_SIZE = 'x'.join(map(str, [MAP_SIZE_X, MAP_SIZE_Y]))
