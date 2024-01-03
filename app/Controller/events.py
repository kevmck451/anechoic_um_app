
from enum import Enum, auto


# Define the events
class Event(Enum):
    TDT_CONNECT = auto()
    VR_CONNECT = auto()
    LOAD_EXPERIMENT = auto()
    START_WARMUP = auto()
    END_WARMUP = auto()
    START_EXPERIMENT = auto()
    END_EXPERIMENT = auto()
    RESET_EXPERIMENT = auto()
    PAUSE = auto()
    RESUME = auto()
    SETTINGS = auto()
    STIM_NUMBER = auto()
    CHANNEL_NUMBER = auto()
    CHANNEL_SEL_NUMBER = auto()
    SETTINGS_CLOSE = auto()
    SET_STIM_NUMBER = auto()
    SET_DEFAULT_BW_TIME = auto()
    VR_INPUT = auto()