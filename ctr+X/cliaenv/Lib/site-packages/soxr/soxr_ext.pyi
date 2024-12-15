import enum
from typing import Annotated

from numpy.typing import ArrayLike


class CSoxr:
    def __init__(self, arg0: float, arg1: float, arg2: int, arg3: soxr_datatype_t, arg4: int, /) -> None: ...

    @property
    def in_rate(self) -> float: ...

    @property
    def out_rate(self) -> float: ...

    @property
    def ntype(self) -> soxr_datatype_t: ...

    @property
    def channels(self) -> int: ...

    @property
    def ended(self) -> bool: ...

    def process_float32(self, arg0: Annotated[ArrayLike, dict(dtype='float32', writable=False, shape=(None, None), order='C', device='cpu')], arg1: bool, /) -> Annotated[ArrayLike, dict(dtype='float32')]: ...

    def process_float64(self, arg0: Annotated[ArrayLike, dict(dtype='float64', writable=False, shape=(None, None), order='C', device='cpu')], arg1: bool, /) -> Annotated[ArrayLike, dict(dtype='float64')]: ...

    def process_int32(self, arg0: Annotated[ArrayLike, dict(dtype='int32', writable=False, shape=(None, None), order='C', device='cpu')], arg1: bool, /) -> Annotated[ArrayLike, dict(dtype='int32')]: ...

    def process_int16(self, arg0: Annotated[ArrayLike, dict(dtype='int16', writable=False, shape=(None, None), order='C', device='cpu')], arg1: bool, /) -> Annotated[ArrayLike, dict(dtype='int16')]: ...

    def num_clips(self) -> int: ...

    def delay(self) -> float: ...

    def engine(self) -> str: ...

    def clear(self) -> None: ...

HQ: int = 4

LQ: int = 1

MQ: int = 2

QQ: int = 0

SOXR_FLOAT32_I: soxr_datatype_t = soxr_datatype_t.SOXR_FLOAT32_I

SOXR_FLOAT64_I: soxr_datatype_t = soxr_datatype_t.SOXR_FLOAT64_I

SOXR_INT16_I: soxr_datatype_t = soxr_datatype_t.SOXR_INT16_I

SOXR_INT32_I: soxr_datatype_t = soxr_datatype_t.SOXR_INT32_I

VHQ: int = 6

def csoxr_divide_proc_float32(arg0: float, arg1: float, arg2: Annotated[ArrayLike, dict(dtype='float32', writable=False, shape=(None, None), order='C', device='cpu')], arg3: int, /) -> Annotated[ArrayLike, dict(dtype='float32')]: ...

def csoxr_divide_proc_float64(arg0: float, arg1: float, arg2: Annotated[ArrayLike, dict(dtype='float64', writable=False, shape=(None, None), order='C', device='cpu')], arg3: int, /) -> Annotated[ArrayLike, dict(dtype='float64')]: ...

def csoxr_divide_proc_int16(arg0: float, arg1: float, arg2: Annotated[ArrayLike, dict(dtype='int16', writable=False, shape=(None, None), order='C', device='cpu')], arg3: int, /) -> Annotated[ArrayLike, dict(dtype='int16')]: ...

def csoxr_divide_proc_int32(arg0: float, arg1: float, arg2: Annotated[ArrayLike, dict(dtype='int32', writable=False, shape=(None, None), order='C', device='cpu')], arg3: int, /) -> Annotated[ArrayLike, dict(dtype='int32')]: ...

def csoxr_oneshot_float32(arg0: float, arg1: float, arg2: Annotated[ArrayLike, dict(dtype='float32', writable=False, shape=(None, None), order='C', device='cpu')], arg3: int, /) -> Annotated[ArrayLike, dict(dtype='float32')]: ...

def csoxr_oneshot_float64(arg0: float, arg1: float, arg2: Annotated[ArrayLike, dict(dtype='float64', writable=False, shape=(None, None), order='C', device='cpu')], arg3: int, /) -> Annotated[ArrayLike, dict(dtype='float64')]: ...

def csoxr_oneshot_int16(arg0: float, arg1: float, arg2: Annotated[ArrayLike, dict(dtype='int16', writable=False, shape=(None, None), order='C', device='cpu')], arg3: int, /) -> Annotated[ArrayLike, dict(dtype='int16')]: ...

def csoxr_oneshot_int32(arg0: float, arg1: float, arg2: Annotated[ArrayLike, dict(dtype='int32', writable=False, shape=(None, None), order='C', device='cpu')], arg3: int, /) -> Annotated[ArrayLike, dict(dtype='int32')]: ...

def csoxr_split_ch_float32(arg0: float, arg1: float, arg2: Annotated[ArrayLike, dict(dtype='float32', writable=False, shape=(None, None), device='cpu')], arg3: int, /) -> Annotated[ArrayLike, dict(dtype='float32')]: ...

def csoxr_split_ch_float64(arg0: float, arg1: float, arg2: Annotated[ArrayLike, dict(dtype='float64', writable=False, shape=(None, None), device='cpu')], arg3: int, /) -> Annotated[ArrayLike, dict(dtype='float64')]: ...

def csoxr_split_ch_int16(arg0: float, arg1: float, arg2: Annotated[ArrayLike, dict(dtype='int16', writable=False, shape=(None, None), device='cpu')], arg3: int, /) -> Annotated[ArrayLike, dict(dtype='int16')]: ...

def csoxr_split_ch_int32(arg0: float, arg1: float, arg2: Annotated[ArrayLike, dict(dtype='int32', writable=False, shape=(None, None), device='cpu')], arg3: int, /) -> Annotated[ArrayLike, dict(dtype='int32')]: ...

def libsoxr_version() -> str: ...

class soxr_datatype_t(enum.Enum):
    SOXR_FLOAT32_I = 0

    SOXR_FLOAT64_I = 1

    SOXR_INT32_I = 2

    SOXR_INT16_I = 3
