import os

from .common import BPETokenizerParams
class BPETokenizerTrainer:
    def __init__(
        self, input_path: str | os.PathLike, vocab_size: int, special_tokens: list[str]
    ):
        """
        Initializes the BPE tokenizer trainer with the specified vocabulary size and special tokens.
        :param input_path: The path to the input text file used for training the BPE tokenizer.
        :param vocab_size: The desired size of the vocabulary.
        :param special_tokens: A list of special tokens to be included in the vocabulary.
        """
        self._input_path = input_path
        self._vocab_size = vocab_size
        self._special_tokens = special_tokens

    def train(self) -> BPETokenizerParams:
        ...