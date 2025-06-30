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


class AudioPlaybackSampleRate(Enum):
    KHZ_48 = 0
    KHZ_88 = 1
    KHZ_96 = 2


class AudioPlaybackQuality:
    def __init__(self, audio_playback_bit_rate: AudioBitRate, audio_playback_sample_rate: AudioPlaybackSampleRate):
        self.__audio_playback_bit_rate = audio_playback_bit_rate
        self.__audio_playback_sample_rate = audio_playback_sample_rate


class Playback:
    def __init__(self):
        self.__audio_output = AudioOutput.SPEAKERS
        self.__speakers_mode = AudioMode.STEREO
        self.__headphones_mode = AudioMode.STEREO
        self.__direct_mode_enabled = False
        self.__spdif_out_direct_mode_enabled = False
        self.__audio_phase = AudioPhase.FAST_MINIMAL
        self.__audio_quality = AudioPlaybackQuality(AudioBitRate.BIT_32, AudioPlaybackSampleRate.KHZ_96)


class VoiceMorph(Enum):
    NEUTRAL = 0
    MALE = 1
    FEMALE = 2
    CHILD = 3
    GRANDMA = 4
    DARK_VOICE = 5
    NORTHERN_LIGHT = 6
    UNSTABLE = 7
    EMO = 8
    ELF = 9
    DWARF = 10
    INTRUDER = 11
    UR = 12
    ORC = 13
    MARINE = 14
    HAMSTER = 15
    ROBOTER = 16


class AudioRecordingChannels(Enum):
    TWO_CHANNELS = 0


class AudioRecordingSampleRate(Enum):
    KHZ_44 = 0
    KHZ_48 = 1
    KHZ_88 = 2
    KHZ_96 = 3
    KHZ_176 = 4
    KHZ_192 = 5


class AudioRecordingQuality:
    def __init__(self,
                 audio_recording_channels: AudioRecordingChannels,
                 audio_recording_bit_rate: AudioBitRate,
                 audio_recording_sample_rate: AudioRecordingSampleRate):
        self.__audio_recording_channels = audio_recording_channels
        self.__audio_recording_bit_rate = audio_recording_bit_rate
        self.__audio_recording_sample_rate = audio_recording_sample_rate


class Recording:
    def __init__(self):
        self.__microphone_volume = 0
        self.__microphone_boost = 0
        self.__use_device_as_playback_source = False
        self.__voice_clarity_enabled = False
        self.__voice_clarity_noise_reduction_enabled = False
        self.__voice_clarity_noise_reduction_value = 0
        self.__voice_clarity_acoustic_echo_cancellation_enabled = False
        self.__voice_clarity_smart_volume_enabled = False
        self.__voice_clarity_microphone_equalizer_enabled = False
        self.__voice_morph_enabled = False
        self.__voice_morph_value = VoiceMorph.NEUTRAL
        self.__line_in = AudioRecordingQuality(AudioRecordingChannels.TWO_CHANNELS, AudioBitRate.BIT_16,
                                               AudioRecordingSampleRate.KHZ_44)
        self.__spdif_in = AudioRecordingQuality(AudioRecordingChannels.TWO_CHANNELS, AudioBitRate.BIT_16,
                                                AudioRecordingSampleRate.KHZ_44)
        self.__what_u_hear = AudioRecordingQuality(AudioRecordingChannels.TWO_CHANNELS, AudioBitRate.BIT_16,
                                                   AudioRecordingSampleRate.KHZ_44)


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
        self.__light_rgb = RGB(128, 128, 128)


class G6Model:
    def __init__(self):
        self.__sbx_profile = SbxProfile()
        self.__playback = Playback()
        self.__recording = Recording()
        self.__decoder = Decoder.NORMAL
        self.__mixer = Mixer()
        self.__lighting = Lighting()
