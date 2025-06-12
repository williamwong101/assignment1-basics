
import numpy as np
import sys
print(f"Python version: {sys.version}, executable: {sys.executable}, path: {sys.path}")
def print_string_encoding(string, encoding):
    """
    Prints the byte representation of a string in the specified encoding.
    
    :param string: The input string to be encoded.
    :param encoding: The encoding format (e.g., 'utf-8', 'utf-16', 'utf-32').
    """
    encoded_bytes = string.encode(encoding)
    print(f"=== Encoding in {encoding} ===")
    print(f"Bytes len: {len(encoded_bytes)}, {encoded_bytes}")
    print(f"Bytes list: {list(encoded_bytes)}")

def decode_utf8_bytes_to_str_wrong(bytestring: bytes):
    return "".join([bytes([b]).decode("utf-8") for b in bytestring])

if __name__ == "__main__":
    # Problem (unicode2): Unicode Encodings
    string = "Hello, world! 这是一个 test string."
    print("Original String:", string)
    print_string_encoding(string, 'utf-8')
    print_string_encoding(string, 'utf-16')
    print_string_encoding(string, 'utf-32')
    
    # print("\n=== Decoding UTF-8 Bytes to String (Wrong Method) ===")
    # test_string = chr(666)
    # print(f"Original string: {test_string}, encoded: {test_string.encode('utf-8')}")
    # print("Decoded String: ", decode_utf8_bytes_to_str_wrong(test_string.encode('utf-8')))  # This will not work correctly
    