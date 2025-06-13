
from tests.adapters import run_train_bpe
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def train_bpe():
    input_path = "data/TinyStoriesV2-GPT4-valid.txt"
    logging.info(f"Call run_train_bpe on input file: {input_path}")
    vocab, merges = run_train_bpe(
        input_path=input_path,
        vocab_size=500,
        special_tokens=["<|endoftext|>"],
        pre_tokenize_processes=1,
    )
    logger.info("=== Vocabulary and Merges ===")
    logger.info(f"Vocabulary: {vocab}")
    logger.info(f"Merges: {merges}")
    
if __name__ == "__main__":
    train_bpe()