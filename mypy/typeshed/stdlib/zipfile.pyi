import io
import sys
from _typeshed import Self, StrOrBytesPath, StrPath, _BufferWithLen
from collections.abc import Callable, Iterable, Iterator
from os import PathLike
from types import TracebackType
from typing import IO, Any, Protocol, overload
from typing_extensions import Literal, TypeAlias

__all__ = [
    "BadZipFile",
    "BadZipfile",
    "error",
    "ZIP_STORED",
    "ZIP_DEFLATED",
    "ZIP_BZIP2",
    "ZIP_LZMA",
    "is_zipfile",
    "ZipInfo",
    "ZipFile",
    "PyZipFile",
    "LargeZipFile",
]

if sys.version_info >= (3, 8):
    __all__ += ["Path"]

_DateTuple: TypeAlias = tuple[int, int, int, int, int, int]
_ReadWriteMode: TypeAlias = Literal["r", "w"]
_ReadWriteBinaryMode: TypeAlias = Literal["r", "w", "rb", "wb"]
_ZipFileMode: TypeAlias = Literal["r", "w", "x", "a"]
_CompressionMode: TypeAlias = Literal[0, 8, 12, 14]

class BadZipFile(Exception): ...

BadZipfile = BadZipFile
error = BadZipfile

class LargeZipFile(Exception): ...

class _ZipStream(Protocol):
    def read(self, __n: int) -> bytes: ...
    # The following methods are optional:
    # def seekable(self) -> bool: ...
    # def tell(self) -> int: ...
    # def seek(self, __n: int) -> object: ...

# Stream shape as required by _EndRecData() and _EndRecData64().
class _SupportsReadSeekTell(Protocol):
    def read(self, __n: int = ...) -> bytes: ...
    def seek(self, __cookie: int, __whence: int) -> object: ...
    def tell(self) -> int: ...

class _ClosableZipStream(_ZipStream, Protocol):
    def close(self) -> object: ...

class ZipExtFile(io.BufferedIOBase):
    MAX_N: int
    MIN_READ_SIZE: int
    MAX_SEEK_READ: int
    newlines: list[bytes] | None
    mode: _ReadWriteMode
    name: str
    @overload
    def __init__(
        self, fileobj: _ClosableZipStream, mode: _ReadWriteMode, zipinfo: ZipInfo, pwd: bytes | None, close_fileobj: Literal[True]
    ) -> None: ...
    @overload
    def __init__(
        self,
        fileobj: _ClosableZipStream,
        mode: _ReadWriteMode,
        zipinfo: ZipInfo,
        pwd: bytes | None = ...,
        *,
        close_fileobj: Literal[True],
    ) -> None: ...
    @overload
    def __init__(
        self,
        fileobj: _ZipStream,
        mode: _ReadWriteMode,
        zipinfo: ZipInfo,
        pwd: bytes | None = ...,
        close_fileobj: Literal[False] = ...,
    ) -> None: ...
    def read(self, n: int | None = ...) -> bytes: ...
    def readline(self, limit: int = ...) -> bytes: ...  # type: ignore[override]
    def peek(self, n: int = ...) -> bytes: ...
    def read1(self, n: int | None) -> bytes: ...  # type: ignore[override]
    def seek(self, offset: int, whence: int = ...) -> int: ...

class _Writer(Protocol):
    def write(self, __s: str) -> object: ...

class ZipFile:
    filename: str | None
    debug: int
    comment: bytes
    filelist: list[ZipInfo]
    fp: IO[bytes] | None
    NameToInfo: dict[str, ZipInfo]
    start_dir: int  # undocumented
    compression: _CompressionMode  # undocumented
    compresslevel: int | None  # undocumented
    mode: _ZipFileMode  # undocumented
    pwd: bytes | None  # undocumented
    if sys.version_info >= (3, 11):
        @overload
        def __init__(
            self,
            file: StrPath | IO[bytes],
            mode: Literal["r"] = ...,
            compression: _CompressionMode = ...,
            allowZip64: bool = ...,
            compresslevel: int | None = ...,
            *,
            strict_timestamps: bool = ...,
            metadata_encoding: str | None,
        ) -> None: ...
        @overload
        def __init__(
            self,
            file: StrPath | IO[bytes],
            mode: _ZipFileMode = ...,
            compression: _CompressionMode = ...,
            allowZip64: bool = ...,
            compresslevel: int | None = ...,
            *,
            strict_timestamps: bool = ...,
            metadata_encoding: None = ...,
        ) -> None: ...
    elif sys.version_info >= (3, 8):
        def __init__(
            self,
            file: StrPath | IO[bytes],
            mode: _ZipFileMode = ...,
            compression: _CompressionMode = ...,
            allowZip64: bool = ...,
            compresslevel: int | None = ...,
            *,
            strict_timestamps: bool = ...,
        ) -> None: ...
    else:
        def __init__(
            self,
            file: StrPath | IO[bytes],
            mode: _ZipFileMode = ...,
            compression: _CompressionMode = ...,
            allowZip64: bool = ...,
            compresslevel: int | None = ...,
        ) -> None: ...

    def __enter__(self: Self) -> Self: ...
    def __exit__(
        self, type: type[BaseException] | None, value: BaseException | None, traceback: TracebackType | None
    ) -> None: ...
    def close(self) -> None: ...
    def getinfo(self, name: str) -> ZipInfo: ...
    def infolist(self) -> list[ZipInfo]: ...
    def namelist(self) -> list[str]: ...
    def open(
        self, name: str | ZipInfo, mode: _ReadWriteMode = ..., pwd: bytes | None = ..., *, force_zip64: bool = ...
    ) -> IO[bytes]: ...
    def extract(self, member: str | ZipInfo, path: StrPath | None = ..., pwd: bytes | None = ...) -> str: ...
    def extractall(
        self, path: StrPath | None = ..., members: Iterable[str | ZipInfo] | None = ..., pwd: bytes | None = ...
    ) -> None: ...
    def printdir(self, file: _Writer | None = ...) -> None: ...
    def setpassword(self, pwd: bytes) -> None: ...
    def read(self, name: str | ZipInfo, pwd: bytes | None = ...) -> bytes: ...
    def testzip(self) -> str | None: ...
    def write(
        self, filename: StrPath, arcname: StrPath | None = ..., compress_type: int | None = ..., compresslevel: int | None = ...
    ) -> None: ...
    def writestr(
        self,
        zinfo_or_arcname: str | ZipInfo,
        data: _BufferWithLen | str,
        compress_type: int | None = ...,
        compresslevel: int | None = ...,
    ) -> None: ...
    if sys.version_info >= (3, 11):
        def mkdir(self, zinfo_or_directory_name: str | ZipInfo, mode: int = ...) -> None: ...

class PyZipFile(ZipFile):
    def __init__(
        self,
        file: str | IO[bytes],
        mode: _ZipFileMode = ...,
        compression: _CompressionMode = ...,
        allowZip64: bool = ...,
        optimize: int = ...,
    ) -> None: ...
    def writepy(self, pathname: str, basename: str = ..., filterfunc: Callable[[str], bool] | None = ...) -> None: ...

class ZipInfo:
    filename: str
    date_time: _DateTuple
    compress_type: _CompressionMode
    comment: bytes
    extra: bytes
    create_system: int
    create_version: int
    extract_version: int
    reserved: int
    flag_bits: int
    volume: int
    internal_attr: int
    external_attr: int
    header_offset: int
    CRC: int
    compress_size: int
    file_size: int
    orig_filename: str  # undocumented
    def __init__(self, filename: str = ..., date_time: _DateTuple = ...) -> None: ...
    if sys.version_info >= (3, 8):
        @classmethod
        def from_file(
            cls: type[Self], filename: StrPath, arcname: StrPath | None = ..., *, strict_timestamps: bool = ...
        ) -> Self: ...
    else:
        @classmethod
        def from_file(cls: type[Self], filename: StrPath, arcname: StrPath | None = ...) -> Self: ...

    def is_dir(self) -> bool: ...
    def FileHeader(self, zip64: bool | None = ...) -> bytes: ...

class _PathOpenProtocol(Protocol):
    def __call__(self, mode: _ReadWriteMode = ..., pwd: bytes | None = ..., *, force_zip64: bool = ...) -> IO[bytes]: ...

if sys.version_info >= (3, 8):
    class Path:
        @property
        def name(self) -> str: ...
        @property
        def parent(self) -> PathLike[str]: ...  # undocumented
        if sys.version_info >= (3, 10):
            @property
            def filename(self) -> PathLike[str]: ...  # undocumented
        if sys.version_info >= (3, 11):
            @property
            def suffix(self) -> str: ...
            @property
            def suffixes(self) -> list[str]: ...
            @property
            def stem(self) -> str: ...

        def __init__(self, root: ZipFile | StrPath | IO[bytes], at: str = ...) -> None: ...
        if sys.version_info >= (3, 9):
            def open(self, mode: _ReadWriteBinaryMode = ..., *args: Any, pwd: bytes | None = ..., **kwargs: Any) -> IO[bytes]: ...
        else:
            @property
            def open(self) -> _PathOpenProtocol: ...

        def iterdir(self) -> Iterator[Path]: ...
        def is_dir(self) -> bool: ...
        def is_file(self) -> bool: ...
        def exists(self) -> bool: ...
        def read_text(
            self,
            encoding: str | None = ...,
            errors: str | None = ...,
            newline: str | None = ...,
            line_buffering: bool = ...,
            write_through: bool = ...,
        ) -> str: ...
        def read_bytes(self) -> bytes: ...
        if sys.version_info >= (3, 10):
            def joinpath(self, *other: StrPath) -> Path: ...
        else:
            def joinpath(self, add: StrPath) -> Path: ...  # undocumented

        def __truediv__(self, add: StrPath) -> Path: ...

def is_zipfile(filename: StrOrBytesPath | _SupportsReadSeekTell) -> bool: ...

ZIP_STORED: Literal[0]
ZIP_DEFLATED: Literal[8]
ZIP64_LIMIT: int
ZIP_FILECOUNT_LIMIT: int
ZIP_MAX_COMMENT: int
ZIP_BZIP2: Literal[12]
ZIP_LZMA: Literal[14]
