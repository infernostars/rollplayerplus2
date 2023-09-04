import pickle
from pathlib import Path


def class_to_file_location(file: Path, class_to_encode):
    with open("data"/file, 'wb') as f:
        pickle.dump(class_to_encode, f)


def file_to_class(file: Path):
    with open("data"/file, 'rb') as f:
        return pickle.load(f)
