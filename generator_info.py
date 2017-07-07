import sys


def generator_info_from_command_line_args():
    info = GeneratorInfo()
    if len(sys.argv) < 3:
        print('Two arguments required: STORAGE_PATH TRIP_TITLE')
        exit(1)

    info.storage_path = sys.argv[1]
    info.trip_title = sys.argv[2]

    return info


class GeneratorInfo:
    def __init__(self):
        self.storage_path = None
        self.trip_title = None
