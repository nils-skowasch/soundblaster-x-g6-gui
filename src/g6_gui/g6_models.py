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


class AudioPhase(Enum):
    FAST_MINIMAL = 0
    SLOW_MINIMAL = 1
    FAST_LINEAR = 2
    SLOW_LINEAR = 3


class MicrophoneEqualizerPreset(Enum):
    PRESET_1 = "Preset 1 - Reduce bass, harshness, improve clarity"
    PRESET_2 = "Preset 2 - Reduce bass, improve vocal clarity"
    PRESET_3 = "Preset 3 - Reduce harshness, improve vocal"
    PRESET_4 = "Preset 4 - Reduce bass, improve vocal"
    PRESET_5 = "Preset 5 - Improve vocal, reduce harshness"
    PRESET_6 = "Preset 6 - Reduce bass, improve clarity"
    PRESET_7 = "Preset 7 - Reduce vocal, improve bass/clarity"
    PRESET_8 = "Preset 8 - Reduce harshness, improve vocal/clarity"
    PRESET_9 = "Preset 9 - Reduce harshness, imrpove clarity"
    PRESET_10 = "Preset 10 - Improve clarity"
    PRESET_DM_1 = "Preset DM-1 - Improve vocal clarity"


class Recording:
    def __init__(self):
        self.__microphone_volume = 0
        self.__microphone_boost = 0
        self.__mic_monitoring_enabled = False
        self.__mic_monitoring_volume = 0
        self.__voice_clarity_enabled = False
        self.__voice_clarity_noise_reduction_enabled = False
        self.__voice_clarity_noise_reduction_value = 0
        self.__voice_clarity_acoustic_echo_cancellation_enabled = False
        self.__voice_clarity_smart_volume_enabled = False
        self.__voice_clarity_microphone_equalizer_enabled = False
        self.__voice_clarity_microphone_equalizer_preset = MicrophoneEqualizerPreset.PRESET_1


class Decoder(Enum):
    NORMAL = 1
    FULL = 2
    NIGHT = 3


class MixerValue:
    def __init__(self, active: bool, value: int):
        self.__active = active
        self.__stereo_left_value = value
        self.__stereo_right_value = value


class Mixer:
    def __init__(self):
        self.__playback_speakers = MixerValue(True, 50)
        self.__monitoring_line_in = MixerValue(True, 50)
        self.__monitoring_external_microphone = MixerValue(True, 50)
        self.__monitoring_spdif_in = MixerValue(True, 50)
        self.__recording_external_microphone = MixerValue(True, 50)
        self.__recording_line_in = MixerValue(True, 50)
        self.__recording_spdif_in = MixerValue(True, 50)
        self.__recording_what_u_hear = MixerValue(True, 50)


class RGB:
    def __init__(self, red: int, green: int, blue: int):
        self.__red = red
        self.__green = green
        self.__blue = blue


class Lighting:
    def __init__(self):
        self.__light_rgb = RGB(255, 0, 0)
