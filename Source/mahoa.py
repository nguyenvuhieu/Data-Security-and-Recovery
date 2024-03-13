from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import hashlib
import os
import struct




# Hàm mã hóa thông tin nhạy cảm
def ma_hoa_thong_tin(text):
    # Ví dụ: mã hóa thông tin bằng hàm băm SHA-256
    hashed_text = hashlib.sha256(text.encode()).hexdigest()
    return hashed_text

import hashlib
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

def ma_hoa_thong_tin_2_chieu(text, mat_khau):
    # Tạo khóa từ mật khẩu
    key = hashlib.sha256(mat_khau.encode()).digest()

    # Mã hóa dữ liệu với AES-256-CBC mode
    iv = os.urandom(16)  # Initialization Vector
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Chuẩn bị dữ liệu và thêm padding nếu cần
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(text.encode()) + padder.finalize()

    # Mã hóa dữ liệu
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    return iv + encrypted_data

def giai_ma_thong_tin_2_chieu(encrypted_data, mat_khau):
    # Tạo khóa từ mật khẩu
    key = hashlib.sha256(mat_khau.encode()).digest()

    # Lấy Initialization Vector và dữ liệu đã mã hóa
    iv = encrypted_data[:16]
    encrypted_data = encrypted_data[16:]

    # Giải mã dữ liệu với AES-256-CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # Giải mã dữ liệu
    decrypted_data = decryptor.update(encrypted_data)

    # Loại bỏ padding thủ công
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    unpadded_data = unpadder.update(decrypted_data)

    # Loại bỏ padding thủ công và decode dữ liệu
    try:
        unpadded_data += unpadder.finalize()
        return unpadded_data.decode()
    except ValueError:
        return False


        


