#import pygame
import json


class JsonManager:
    @staticmethod
    def load(file: str) -> dict:
        with open(file, 'r') as f:
            data = json.load(f)
            return data

    @staticmethod
    def write(file: str, content: dict) -> None:
        with open(file, 'w') as f:
            json.dump(content, f, indent=4)

def pop_multiple(start: int, end: int, target: list):
    if start > end:
        raise ValueError("Start cannot be greater than the end")
        
    sublist = target[start:end]
    target = target[:start]+target[end:]
    
    return sublist
