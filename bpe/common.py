
from dataclasses import dataclass


@dataclass(frozen=True)
class BPETokenizerParams:
    vocab: dict[int, bytes]
    merges: list[tuple[bytes, bytes]]