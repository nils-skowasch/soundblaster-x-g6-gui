from enum import Enum


class AudioComponent:
    def __init__(self):
        self.__available = False
        self.__active = False
        self.__value = 50

    def is_available(self) -> bool:
        return self.__available

    def set_available(self, available: bool):
        self.__available = available

    def is_active(self) -> bool:
        return self.__active

    def set_active(self, active: bool):
        self.__active = active

    def get_value(self) -> int:
        return self.__value

    def set_value(self, value: int):
        self.__value = value


class AudioComponentSmartVolume(AudioComponent):
    def __init__(self):
        super().__init__()
        self.__night_mode = False
        self.__loud_mode = False

    def set_night_mode(self):
        self.__night_mode = True
        self.__loud_mode = False

    def set_loud_mode(self):
        self.__loud_mode = True
        self.__night_mode = False


class AudioMode(Enum):
    STEREO = 0
    VIRTUAL_SURROUND_5_1 = 1
    VIRTUAL_SURROUND_7_1 = 2


class AudioOutput(Enum):
    SPEAKERS = 0
    HEADPHONES = 1
