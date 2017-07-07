import sys


def parser_info_from_command_line_args():
    info = ParserInfo()
    if len(sys.argv) < 3:
        print('Two arguments required: STORAGE_PATH TRIP')
        exit(1)

    info.storage_path = sys.argv[1]
    info.trip = sys.argv[2]

    return info


class ParserInfo:
    def __init__(self):
        self.storage_path = None
        self.trip = None