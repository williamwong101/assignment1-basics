# Writeup 1

## Problem (unicode1): Understanding Unicode

1. '\x00'
2. Printed representation is just a empty string, it return human readable version of the object. While `__repr__()` return a string of official representation, it returns '\x00'.
   1. The core difference here is that, repr(chr(x)) is also a string, which is the official string representation, and contains "'" etc.
   2. Directly calling X in python terminal (>>> X) is print(repr(X)).
3. Say x = 'test\x00test', print(x) will be `testtest`, while `>>> x` will be print(repr(x)), which will be `'test\x00test'`, note those single quotes in the beginning and the end of the string.

## Problem (unicode2): Unicode Encodings

1. The result of utf-8 is more compact comparing to utf-16 and utf-32. For the same sentence, the utf-8 encoding results is significantly shorter than that of utf-16 and utf-32, while being equally expressive. see below example:

    ```bash
    Original String: Hello, world! 这是一个 test string.
    === Encoding in utf-8 ===
    Bytes len: 39, b'Hello, world! \xe8\xbf\x99\xe6\x98\xaf\xe4\xb8\x80\xe4\xb8\xaa test string.'
    Bytes list: [72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33, 32, 232, 191, 153, 230, 152, 175, 228, 184, 128, 228, 184, 170, 32, 116, 101, 115, 116, 32, 115, 116, 114, 105, 110, 103, 46]
    === Encoding in utf-16 ===
    Bytes len: 64, b'\xff\xfeH\x00e\x00l\x00l\x00o\x00,\x00 \x00w\x00o\x00r\x00l\x00d\x00!\x00 \x00\xd9\x8f/f\x00N*N \x00t\x00e\x00s\x00t\x00 \x00s\x00t\x00r\x00i\x00n\x00g\x00.\x00'
    Bytes list: [255, 254, 72, 0, 101, 0, 108, 0, 108, 0, 111, 0, 44, 0, 32, 0, 119, 0, 111, 0, 114, 0, 108, 0, 100, 0, 33, 0, 32, 0, 217, 143, 47, 102, 0, 78, 42, 78, 32, 0, 116, 0, 101, 0, 115, 0, 116, 0, 32, 0, 115, 0, 116, 0, 114, 0, 105, 0, 110, 0, 103, 0, 46, 0]
    === Encoding in utf-32 ===
    Bytes len: 128, b'\xff\xfe\x00\x00H\x00\x00\x00e\x00\x00\x00l\x00\x00\x00l\x00\x00\x00o\x00\x00\x00,\x00\x00\x00 \x00\x00\x00w\x00\x00\x00o\x00\x00\x00r\x00\x00\x00l\x00\x00\x00d\x00\x00\x00!\x00\x00\x00 \x00\x00\x00\xd9\x8f\x00\x00/f\x00\x00\x00N\x00\x00*N\x00\x00 \x00\x00\x00t\x00\x00\x00e\x00\x00\x00s\x00\x00\x00t\x00\x00\x00 \x00\x00\x00s\x00\x00\x00t\x00\x00\x00r\x00\x00\x00i\x00\x00\x00n\x00\x00\x00g\x00\x00\x00.\x00\x00\x00'
    Bytes list: [255, 254, 0, 0, 72, 0, 0, 0, 101, 0, 0, 0, 108, 0, 0, 0, 108, 0, 0, 0, 111, 0, 0, 0, 44, 0, 0, 0, 32, 0, 0, 0, 119, 0, 0, 0, 111, 0, 0, 0, 114, 0, 0, 0, 108, 0, 0, 0, 100, 0, 0, 0, 33, 0, 0, 0, 32, 0, 0, 0, 217, 143, 0, 0, 47, 102, 0, 0, 0, 78, 0, 0, 42, 78, 0, 0, 32, 0, 0, 0, 116, 0, 0, 0, 101, 0, 0, 0, 115, 0, 0, 0, 116, 0, 0, 0, 32, 0, 0, 0, 115, 0, 0, 0, 116, 0, 0, 0, 114, 0, 0, 0, 105, 0, 0, 0, 110, 0, 0, 0, 103, 0, 0, 0, 46, 0, 0, 0]
    ```

2. Example bytes: `b'\xca\x9a'`. Running the given function will result in `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xca in position 0: unexpected end of data`. This is because the first few bits are used to indicate how many bytes are in the sequence to represent the current character. In this case, `'\xca'` is `11001010`, in which `110` means it is the starting byte of a 2-bytes character. Then, decoding this byte only will result in error.
3. Invalid 2-bytesL `b\xda\xda'`. This does not follows the rule of utf-8, since `'\xda'` is `11011010`, which indicates it is the first byte of a 2-bytes character. 

