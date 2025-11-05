from models import Board, Player
import os as os

def read_size(file_path: str):
    with open(file_path, 'r') as file:
        for line in file:
            line_copy = line.strip()
            line_parts = line_copy.split(': ')
            if line_parts[0] == 'size':
                return int(line_parts[1].strip())
            
def read_mod(file_path: str):
    with open(file_path, 'r') as file:
        for line in file:
            line_copy = line.strip()
            line_parts = line_copy.split(': ')
            if line_parts[0] == 'mod':
                return str(line_parts[1].strip())
            
