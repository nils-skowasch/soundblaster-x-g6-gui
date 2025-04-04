from enum import Enum


class AudioComponent:
    def __init__(self):
        self.__enable = False
        self.__value = 0


class SbxProfile:
    def __init__(self):
        self.__surround = AudioComponent()
        self.__crystalizer = AudioComponent()
        self.__bass = AudioComponent()
        self.__smart_volume = AudioComponent()
        self.__dialog_plus = AudioComponent()


class AudioMode(Enum):
    STEREO = 0
    VIRTUAL_SURROUND_5_1 = 1
    VIRTUAL_SURROUND_7_1 = 2


class AudioOutput(Enum):
    SPEAKERS = 0
    HEADPHONES = 1


class AudioPhase(Enum):
    FAST_MINIMAL = 0
    SLOW_MINIMAL = 1
    FAST_LINEAR = 2
    SLOW_LINEAR = 3


class AudioBitRate(Enum):
    BIT_16 = 0
    BIT_24 = 1
    BIT_32 = 2


class AudioSampleRate(Enum):
    KHZ_48 = 0
    KHZ_88 = 1
    KHZ_96 = 2


class AudioQuality:
    def __init__(self, audio_bit_rate: AudioBitRate, audio_sample_rate: AudioSampleRate):
        self.__audio_bit_rate = audio_bit_rate
        self.__audio_sample_rate = audio_sample_rate


class Playback:
    def __init__(self):
        self.__audio_output = AudioOutput.SPEAKERS
        self.__speakers_mode = AudioMode.STEREO
        self.__headphones_mode = AudioMode.STEREO
        self.__direct_mode_enabled = False
        self.__spdif_out_direct_mode_enabled = False
        self.__audio_phase = AudioPhase.FAST_MINIMAL
        self.__audio_quality = AudioQuality(AudioBitRate.BIT_32, AudioSampleRate.KHZ_96)



class Decoder(Enum):
    NORMAL = 1
    FULL = 2
    NIGHT = 3
