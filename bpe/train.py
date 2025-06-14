import os

from bpe.common import BPETokenizerParams
from cs336_basics.pretokenization_example import find_chunk_boundaries
from multiprocessing import Pool
import regex as re
import logging
import itertools
logger = logging.getLogger(__name__)


class BPETokenizerTrainer:
    PRE_TOKENIZE_PAT = r"""'(?:[sdmt]|ll|ve|re)| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+"""
    
    def __init__(
        self,
        input_path: str | os.PathLike,
        vocab_size: int,
        special_tokens: list[str],
        pre_tokenize_processes: int = 1,
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
        self._pre_tokenize_processes = pre_tokenize_processes

        self._vocab: dict[int, bytes] = {}
        self._merges: list[tuple[bytes, bytes]] = []
        self._pre_tokenize_frequency: dict[str, int] = {}

    def _init_vocab(self):
        """
        Initializes the vocabulary with 256 byte values and special tokens and their corresponding byte representations.
        """
        for token in self._special_tokens:
            token_bytes = token.encode("utf-8")
            self._vocab[len(self._vocab)] = token_bytes
        for i in range(256):
            self._vocab[len(self._vocab)] = bytes([i])
        logger.debug(f"Init vocab: {self._vocab}")

    @classmethod
    def pre_tokenize_chunk(
        cls, input_path: str, start: int, end: int, special_tokens: list[str]
    ) -> dict[str, int]:
        """
        Pre-tokenizes a chunk of text from the input file.
        :param input_path: The path to the input text file.
        :param start: The starting byte position of the chunk.
        :param end: The ending byte position of the chunk.
        :param special_tokens: A list of special tokens to be used for pre-tokenization.
        :return: A dictionary mapping pre-tokenized tokens to their frequencies in the chunk.
        """
        docs: list[str] = []
        with open(input_path, "rb") as f:
            f.seek(start)
            chunk_text = f.read(end - start).decode("utf-8", errors="ignore")
            special_tokens_regex = "|".join(
                [re.escape(token) for token in special_tokens]
            )
            docs = re.split(special_tokens_regex, chunk_text)
        pre_tokenize_frequency = {}
        for doc in docs:
            tokens = re.findall(cls.PRE_TOKENIZE_PAT, doc)
            for token in tokens:
                if token not in pre_tokenize_frequency:
                    pre_tokenize_frequency[token] = 0
                pre_tokenize_frequency[token] += 1
        return pre_tokenize_frequency

    def _pre_tokenize(self) -> None:
        """
        Pre-tokenizes the input text file to prepare for BPE training.
        This method should read the input file and perform any necessary pre-tokenization steps.
        """
        with open(self._input_path, "rb") as f:
            boundaries = find_chunk_boundaries(
                f, self._pre_tokenize_processes, self._special_tokens[0].encode("utf-8")
            )

            chunk_indices = list(zip(boundaries[:-1], boundaries[1:]))
            num_processes = min(self._pre_tokenize_processes, len(chunk_indices))
            logger.debug(f"Num chunks: {len(chunk_indices)}, num processes: {num_processes}")

            with Pool(num_processes) as pool:
                chunk_pre_tokenize_results = pool.starmap(
                    self.pre_tokenize_chunk,
                    [
                        (
                            self._input_path,
                            chunk_index[0],
                            chunk_index[1],
                            self._special_tokens,
                        )
                        for chunk_index in chunk_indices
                    ],
                )

            for chunk_result in chunk_pre_tokenize_results:
                for token, count in chunk_result.items():
                    if token in self._pre_tokenize_frequency:
                        self._pre_tokenize_frequency[token] += count
                    else:
                        self._pre_tokenize_frequency[token] = count
        logger.debug(
            f"Pre-tokenization frequency length: {len(self._pre_tokenize_frequency)}, pre-tokenization frequency: {dict(itertools.islice(self._pre_tokenize_frequency.items(), 10))}"
        )

    def train(self) -> BPETokenizerParams:
        """
        Trains the BPE tokenizer on the input text file.
        :return: A BPETokenizerParams object containing the vocabulary and merges.
        """

        # Initialize the vocabulary with byte values and special tokens
        self._init_vocab()
        
        # Pre-tokenize the input text file
        self._pre_tokenize()

        

        # For now, we return an empty set of merges
        return BPETokenizerParams(vocab=self._vocab, merges=self._merges)
