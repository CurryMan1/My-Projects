import json
import math

class JsonManager:
    @staticmethod
    def load(file: str) -> dict:
        with open(file, 'r') as f:
            data = json.load(f)
            f.close()
            return data

    @staticmethod
    def write(file: str, content: dict) -> None:
        with open(file, 'w') as f:
            json.dump(content, f, indent=4)
            f.close()


#func to check if hex code is closer to white or black
def white_or_black(hex_) -> str:
    #convert hex to rgb (https://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python)
    hex_ = hex_.lstrip('#')
    lv = len(hex_)
    r, g, b = tuple(int(hex_[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

    #get hsp from rgb (https://awik.io/determine-color-bright-dark-using-javascript/)
    hsp = math.sqrt(
        0.299 * (r * r) +
        0.587 * (g * g) +
        0.114 * (b * b)
    )

    #return white/black
    if hsp > 127.5:
        return 'black'
    return 'white'


#files
options_file = 'data/options.json'
sets_file = 'data/sets.json'

options = JsonManager.load(options_file)
sets = JsonManager.load(sets_file)

#constants
FONT = ('helvetica', 60, 'bold')
SMALL_FONT = ('helvetica', 40, 'bold')
