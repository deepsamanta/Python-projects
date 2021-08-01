from enum import Enum


class Status(Enum):
    ONLINE = 'online'
    OFFLINE = 'offline'
    IS_WRITING = 'typing…'
    NOT_DEFINED = 'not defined'