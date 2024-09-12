
import zlib
import base64

def compress_and_encode(text: str) -> str:
    # Nén dữ liệu
    compressed_data = zlib.compress(text.encode())
    # Mã hóa thành base64 để có thể truyền và lưu trữ dễ dàng
    encoded_data = base64.b64encode(compressed_data).decode()
    return encoded_data

def decode_and_decompress(encoded_text: str) -> str:
    # Giải mã từ base64
    compressed_data = base64.b64decode(encoded_text)
    # Giải nén dữ liệu
    decompressed_data = zlib.decompress(compressed_data)
    return decompressed_data.decode()

# Ví dụ sử dụng


