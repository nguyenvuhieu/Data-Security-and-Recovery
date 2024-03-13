import struct, hashlib, os, time, random, string,sys
from dulieumau import *
from mahoa import *
import pandas as pd



LEN_MA_GV = 10
LEN_MA_SV = 10
LEN_HO_TEN = 30
LEN_NGAY_SINH = 15
LEN_NGAY_THAM_GIA = 15
LEN_SO_DT = 50
LEN_CCCD = 50
LEN_KEY = 50
SUM_LEN = LEN_MA_SV + LEN_HO_TEN + LEN_NGAY_SINH + LEN_NGAY_THAM_GIA + LEN_SO_DT + LEN_CCCD + LEN_KEY 

SIZE_T = 10
SIZE_S = 10
POS_START_S = 10
START_T = SIZE_T + SIZE_S + POS_START_S


def sinh_mat_khau():
    mat_khau = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

    with open('matkhau.txt', 'w') as file:
        file.write(mat_khau)
    return mat_khau



def chon_kich_thuoc_file():
    print("Lựa chọn kích thước file:")
    print("1. 0,1MB")
    print("2. 0,2MB")
    print("3. 0,5MB")
    print("4. Nhập kích thước từ bàn phím")
    
    choice = input("Chọn: ")

    if choice == '1':
        return int(0.1 * 1024 * 1024)
    elif choice == '2':
        return int(0.2 * 1024 * 1024)
    elif choice == '3':
        return int(0.5 * 1024 * 1024)
    elif choice == '4':
        custom_size = int(input("Nhập kích thước (MB): "))
        return custom_size
    else:
        print("Lựa chọn không hợp lệ. Chọn từ 1 đến 4.")
        return chon_kich_thuoc_file()


def tinh_so_luong_toi_da(file_size):
    byte_per_teacher = 1 + SUM_LEN  # Số byte cho mỗi phần giáo viên
    byte_per_student = 1 + SUM_LEN  # Số byte cho mỗi phần sinh viên

    file_size -= (32 + SIZE_T + SIZE_S + POS_START_S) #-32 byte cuối để lưu mật khẩu và 10 byte đầu lưu max_teacher_count và 10 byte của max_student_count
    total_byte_teacher = 0.2 * file_size  # Tổng số byte cho cả phần giáo viên và sinh viên
    total_byte_student = 0.8 * file_size  # Tổng số byte cho cả phần giáo viên và sinh viên
    # Số lượng phần giáo viên và sinh viên tối đa có thể chứa trong file
    max_teacher_count = int(total_byte_teacher / byte_per_teacher)
    max_student_count = int(total_byte_student / byte_per_student)

    return max_teacher_count, max_student_count


        
def tao_file_trong(file_name):
    # Tính toán kích thước file trong byte dựa trên kích thước đầu vào (file_size_mb)
    file_size = chon_kich_thuoc_file()

    # Tính toán số lượng tối đa giáo viên và sinh viên dựa trên kích thước file
    max_teacher_count, max_student_count = tinh_so_luong_toi_da(file_size)
    START_S = START_T + (SUM_LEN + 1) * max_teacher_count
    with open(file_name, 'wb') as file:
        # Ghi số lượng tối đa giáo viên và sinh viên vào 20 byte đầu tiên của file
        file.write(str(max_teacher_count).encode('utf-8').ljust(SIZE_T)[:SIZE_T])
        file.write(str(max_student_count).encode('utf-8').ljust(SIZE_S)[:SIZE_S])
        file.write(str(START_S).encode('utf-8').ljust(POS_START_S)[:POS_START_S])
        # Ghi mảng trạng thái của giáo viên vào vị trí thích hợp trong file
        file.seek(START_T)
        for i in range(max_teacher_count):
            file.write(struct.pack('<B', 0))  # Ghi trạng thái mặc định cho từng phần tử giáo viên


        # Tính toán và ghi dữ liệu cần thiết để đạt kích thước file mong muốn
        current_position = file.tell()
        remaining_bytes = file_size - current_position

        # Ghi các byte còn thiếu với giá trị mặc định (ở đây là 0)
        file.write(b'\0' * remaining_bytes)
        file.seek(START_S)
        for i in range(max_student_count):
            file.write(struct.pack('<B', 0))  # Ghi trạng thái mặc định cho từng phần tử sinh viên
        
        
        mat_khau = input("Nhập mật khẩu: ")
        hashed_password = hashlib.sha256(mat_khau.encode()).digest()   
        # Ghi chuỗi băm mật khẩu vào những bit cuối của file
        file.seek(-len(hashed_password), 2)
        file.write(hashed_password)
        
        return max_teacher_count,max_student_count, START_S

def tao_file_voi_du_lieu_mau(file_name, danh_sach_giao_vien, danh_sach_sinh_vien):
    # Tính toán kích thước file trong byte dựa trên kích thước đầu vào (file_size_mb)
    file_size = chon_kich_thuoc_file()

    # Tính toán số lượng tối đa giáo viên và sinh viên dựa trên kích thước file
    max_teacher_count, max_student_count = tinh_so_luong_toi_da(file_size)
    START_S = START_T + (SUM_LEN + 1) * max_teacher_count

    with open(file_name, 'wb') as file:
        # Ghi số lượng tối đa giáo viên và sinh viên vào 20 byte đầu tiên của file
        file.write(str(max_teacher_count).encode('utf-8').ljust(SIZE_T)[:SIZE_T])
        file.write(str(max_student_count).encode('utf-8').ljust(SIZE_S)[:SIZE_S])
        file.write(str(START_S).encode('utf-8').ljust(POS_START_S)[:POS_START_S])

        # Tính toán và ghi dữ liệu cần thiết để đạt kích thước file mong muốn
        current_position = file.tell()
        remaining_bytes = file_size - current_position
        # Ghi các byte còn thiếu với giá trị mặc định (ở đây là 0)
        file.write(b'\0' * remaining_bytes)

        # Ghi mảng trạng thái của giáo viên vào vị trí thích hợp trong file
        file.seek(START_T)
        for i in range(max_teacher_count):
            file.write(struct.pack('<B', 0))  # Ghi trạng thái mặc định cho từng phần tử giáo viên

        # Ghi dữ liệu mẫu giáo viên vào file
        for i,giao_vien in enumerate(danh_sach_giao_vien):
            file.seek(START_T + max_teacher_count + i * SUM_LEN)
            file.write(giao_vien['Ma'].encode('utf-8').ljust(LEN_MA_GV)[:LEN_MA_GV])
            file.write(giao_vien['HoTen'].encode('utf-8').ljust(LEN_HO_TEN)[:LEN_HO_TEN])
            file.write(giao_vien['NgaySinh'].encode('utf-8').ljust(LEN_NGAY_SINH)[:LEN_NGAY_SINH])
            file.write(giao_vien['NgayThamGia'].encode('utf-8').ljust(LEN_NGAY_THAM_GIA)[:LEN_NGAY_THAM_GIA])
            file.write(struct.pack('<Q', int(giao_vien['SoDT'])).ljust(LEN_SO_DT)[:LEN_SO_DT])
            file.write(struct.pack('<Q', int(giao_vien['CCCD'])).ljust(LEN_CCCD)[:LEN_CCCD])
            file.write(giao_vien['Key'].encode('utf-8').ljust(LEN_KEY)[:LEN_KEY])
            file.seek(START_T + i)  # Đi đến vị trí trạng thái của giáo viên thứ i
            file.write(struct.pack('<B', 1))  # Ghi lại trạng thái

        # Ghi mảng trạng thái của sinh viên vào vị trí thích hợp trong file
        file.seek(START_S)
        for i in range(max_student_count):
            file.write(struct.pack('<B', 0))  # Ghi trạng thái mặc định cho từng phần tử sinh viên
        
        # Ghi dữ liệu mẫu sinh viên vào file
        for i,sinh_vien in enumerate(danh_sach_sinh_vien):
            file.seek(START_S + max_student_count + i * SUM_LEN)
            file.write(sinh_vien['Ma'].encode('utf-8').ljust(LEN_MA_SV)[:LEN_MA_SV])
            file.write(sinh_vien['HoTen'].encode('utf-8').ljust(LEN_HO_TEN)[:LEN_HO_TEN])
            file.write(sinh_vien['NgaySinh'].encode('utf-8').ljust(LEN_NGAY_SINH)[:LEN_NGAY_SINH])
            file.write(sinh_vien['NgayThamGia'].encode('utf-8').ljust(LEN_NGAY_THAM_GIA)[:LEN_NGAY_THAM_GIA])
            file.write(struct.pack('<Q', int(sinh_vien['SoDT'])).ljust(LEN_SO_DT)[:LEN_SO_DT])
            file.write(struct.pack('<Q', int(sinh_vien['CCCD'])).ljust(LEN_CCCD)[:LEN_CCCD])
            file.write(sinh_vien['Key'].encode('utf-8').ljust(LEN_KEY)[:LEN_KEY])
            file.seek(START_S + i)  # Đi đến vị trí trạng thái của giáo viên thứ i
            file.write(struct.pack('<B', 1))  # Ghi lại trạng thái
            
        mat_khau = input("Nhập mật khẩu: ")
        hashed_password = hashlib.sha256(mat_khau.encode()).digest()   
        # Ghi chuỗi băm mật khẩu vào những bit cuối của file
        file.seek(-len(hashed_password), 2)
        file.write(hashed_password)
    return max_teacher_count, max_student_count, START_S

def doc_file(file_name, max_teacher_count, max_student_count, START_S, is_student=True):
    trang_thai_ban_dau = []
    with open(file_name, 'rb') as file:
        if is_student:
            danh_sach_sinh_vien = []
            file.seek(START_S)
            for _ in range(max_student_count):
                byte = file.read(1)
                if not byte:
                    break
                trang_thai = struct.unpack('<B', byte)[0]  # Đọc trạng thái từ file (little endian)
                trang_thai_ban_dau.append(trang_thai)
                
            for i, trang_thai in enumerate(trang_thai_ban_dau):
                if trang_thai == 1:  # Nếu trạng thái là 1, có sinh viên, thì đọc dữ liệu của sinh viên
                    file.seek(START_S + max_student_count + i * SUM_LEN)

                    data = file.read(SUM_LEN)
                    ma = data[:LEN_MA_SV].decode('utf-8').strip()
                    ho_ten = data[LEN_MA_SV:LEN_MA_SV + LEN_HO_TEN].decode('utf-8').strip()
                    ngay_sinh = data[LEN_MA_SV + LEN_HO_TEN:LEN_MA_SV + LEN_HO_TEN + LEN_NGAY_SINH].decode('utf-8').strip()
                    ngay_tham_gia = data[LEN_MA_SV + LEN_HO_TEN + LEN_NGAY_SINH:LEN_MA_SV + LEN_HO_TEN + LEN_NGAY_SINH + LEN_NGAY_THAM_GIA].decode('utf-8').strip()
                    so_dien_thoai = str(struct.unpack('<Q', data[LEN_MA_SV + LEN_HO_TEN + LEN_NGAY_SINH + LEN_NGAY_THAM_GIA:LEN_MA_SV + LEN_HO_TEN + LEN_NGAY_SINH + LEN_NGAY_THAM_GIA + 8])[0])
                    cccd = str(struct.unpack('<Q', data[SUM_LEN - LEN_KEY - LEN_CCCD:SUM_LEN - LEN_KEY - LEN_CCCD + 8 ])[0])
                    so_dien_thoai = so_dien_thoai.zfill(10)
                    cccd = cccd.zfill(15)
                elif trang_thai == 2:  # Nếu trạng thái là 2, có sinh viên mã hóa, thì đọc dữ liệu của sinh viên
                    file.seek(START_S + max_student_count + i * SUM_LEN)

                    data = file.read(SUM_LEN)

                    ma = data[:LEN_MA_SV].decode('utf-8').strip()
                    ho_ten = data[LEN_MA_SV:LEN_MA_SV + LEN_HO_TEN].decode('utf-8').strip()
                    ngay_sinh = data[LEN_MA_SV + LEN_HO_TEN:LEN_MA_SV + LEN_HO_TEN + LEN_NGAY_SINH].decode('utf-8').strip()
                    ngay_tham_gia = data[LEN_MA_SV + LEN_HO_TEN + LEN_NGAY_SINH:LEN_MA_SV + LEN_HO_TEN + LEN_NGAY_SINH + LEN_NGAY_THAM_GIA].decode('utf-8').strip()
                    so_dien_thoai = data[LEN_MA_SV + LEN_HO_TEN + LEN_NGAY_SINH + LEN_NGAY_THAM_GIA:LEN_MA_SV + LEN_HO_TEN + LEN_NGAY_SINH + LEN_NGAY_THAM_GIA + LEN_SO_DT].strip()
                    cccd = data[LEN_MA_SV + LEN_HO_TEN + LEN_NGAY_SINH + LEN_NGAY_THAM_GIA + LEN_SO_DT:SUM_LEN-LEN_KEY].strip()

                    
                else: continue    
                    
                sinh_vien = {
                        'Ma': ma,
                        'HoTen': ho_ten,
                        'NgaySinh': ngay_sinh,
                        'NgayThamGia': ngay_tham_gia,
                        'SoDT': so_dien_thoai,
                        'CCCD': cccd
                    }
                danh_sach_sinh_vien.append(sinh_vien)
            print(pd.DataFrame(danh_sach_sinh_vien))
            return 
        else:
            danh_sach_giao_vien = []
            file.seek(START_T)
            for _ in range(max_teacher_count):
                byte = file.read(1)
                if not byte:
                    break
                trang_thai = struct.unpack('<B', byte)[0]  # Đọc trạng thái từ file (little endian)
                trang_thai_ban_dau.append(trang_thai)
                
            for i, trang_thai in enumerate(trang_thai_ban_dau):
                if trang_thai == 1:  # Nếu trạng thái là 1, có sinh viên, thì đọc dữ liệu của sinh viên
                    file.seek(START_T + max_teacher_count + i * SUM_LEN)

                    data = file.read(SUM_LEN)

                    ma = data[:LEN_MA_GV].decode('utf-8').strip()
                    ho_ten = data[LEN_MA_SV:LEN_MA_SV + LEN_HO_TEN].decode('utf-8').strip()
                    ngay_sinh = data[LEN_MA_SV + LEN_HO_TEN:LEN_MA_SV + LEN_HO_TEN + LEN_NGAY_SINH].decode('utf-8').strip()
                    ngay_tham_gia = data[LEN_MA_SV + LEN_HO_TEN + LEN_NGAY_SINH:LEN_MA_SV + LEN_HO_TEN + LEN_NGAY_SINH + LEN_NGAY_THAM_GIA].decode('utf-8').strip()
                    so_dien_thoai = str(struct.unpack('<Q', data[LEN_MA_SV + LEN_HO_TEN + LEN_NGAY_SINH + LEN_NGAY_THAM_GIA:LEN_MA_SV + LEN_HO_TEN + LEN_NGAY_SINH + LEN_NGAY_THAM_GIA + 8])[0])
                    cccd = str(struct.unpack('<Q', data[SUM_LEN - LEN_KEY - LEN_CCCD:SUM_LEN - LEN_KEY - LEN_CCCD + 8 ])[0])
                    so_dien_thoai = so_dien_thoai.zfill(10)
                    cccd = cccd.zfill(15)
                    
                elif trang_thai == 2:  # Nếu trạng thái là 2, có sinh viên mã hóa, thì đọc dữ liệu của sinh viên
                    file.seek(START_T + max_teacher_count + i * SUM_LEN)

                    data = file.read(SUM_LEN)

                    ma = data[:LEN_MA_SV].decode('utf-8').strip()
                    ho_ten = data[LEN_MA_SV:LEN_MA_SV + LEN_HO_TEN].decode('utf-8').strip()
                    ngay_sinh = data[LEN_MA_SV + LEN_HO_TEN:LEN_MA_SV + LEN_HO_TEN + LEN_NGAY_SINH].decode('utf-8').strip()
                    ngay_tham_gia = data[LEN_MA_SV + LEN_HO_TEN + LEN_NGAY_SINH:LEN_MA_SV + LEN_HO_TEN + LEN_NGAY_SINH + LEN_NGAY_THAM_GIA].decode('utf-8').strip()
                    so_dien_thoai = data[LEN_MA_SV + LEN_HO_TEN + LEN_NGAY_SINH + LEN_NGAY_THAM_GIA:LEN_MA_SV + LEN_HO_TEN + LEN_NGAY_SINH + LEN_NGAY_THAM_GIA + LEN_SO_DT].strip()
                    cccd = data[LEN_MA_SV + LEN_HO_TEN + LEN_NGAY_SINH + LEN_NGAY_THAM_GIA + LEN_SO_DT:].strip()
                    
                    
                else: continue    
                    
                giao_vien = {
                        'Ma': ma,
                        'HoTen': ho_ten,
                        'NgaySinh': ngay_sinh,
                        'NgayThamGia': ngay_tham_gia,
                        'SoDT': so_dien_thoai,
                        'CCCD': cccd
                    }
                danh_sach_giao_vien.append(giao_vien)
            print(pd.DataFrame(danh_sach_giao_vien))
            return 
        
    return


def ma_hoa_tat_ca(file_name, max_teacher_count, max_student_count, START_S, is_student=True):
    
    key = input("Nhập mật khẩu chung: ")

    # Đọc trạng thái ban đầu từ file
    trang_thai_ban_dau = []
    with open(file_name, 'rb+') as file:
        if is_student:
            file.seek(START_S)
            for _ in range(max_student_count):  # Đọc 100 phần tử trạng thái
                byte = file.read(1)
                if not byte:
                    break
                trang_thai = struct.unpack('<B', byte)[0]  # Đọc trạng thái từ file (little endian)
                trang_thai_ban_dau.append(trang_thai)

            # Đọc dữ liệu sinh viên từ file
            for i, trang_thai in enumerate(trang_thai_ban_dau):
                if trang_thai == 1:
                    file.seek(START_S + max_student_count + i * SUM_LEN)  # Đi đến vị trí dữ liệu của sinh viên thứ i

                    data = file.read(SUM_LEN)  # Đọc tổng kích thước của trường thông tin

                    # Mã hóa số điện thoại và CCCD
                    so_dien_thoai_mahoa = ma_hoa_thong_tin_2_chieu(str(struct.unpack('<Q', data[SUM_LEN - LEN_SO_DT - LEN_CCCD - LEN_KEY:SUM_LEN - LEN_SO_DT - LEN_CCCD - LEN_KEY + 8])[0]), key)
                    cccd_mahoa = ma_hoa_thong_tin_2_chieu(str(struct.unpack('<Q', data[SUM_LEN - LEN_CCCD - LEN_KEY:SUM_LEN - LEN_CCCD - LEN_KEY + 8])[0]), key)

                    # Điều chỉnh con trỏ để ghi dữ liệu đã mã hóa vào file
                    file.seek(START_S + max_student_count + i * SUM_LEN + LEN_MA_SV + LEN_HO_TEN + LEN_NGAY_SINH + LEN_NGAY_THAM_GIA)  # Đi đến vị trí số điện thoại đã mã hóa
                    file.write(so_dien_thoai_mahoa.ljust(LEN_SO_DT)[:LEN_SO_DT])  # Ghi lại số điện thoại đã mã hóa
                    file.write(cccd_mahoa.ljust(LEN_CCCD)[:LEN_CCCD])  # Ghi lại CCCD đã mã hóa

                    key_mahoa = hashlib.sha256(key.encode()).digest()

                    # Điều chỉnh con trỏ để ghi dữ liệu đã mã hóa vào file
                    file.seek(START_S + max_student_count + i * SUM_LEN + SUM_LEN - LEN_KEY)  # Đi đến vị trí thông tin key đã mã hóa
                    file.write(key_mahoa)  # Ghi lại thông tin key đã mã hóa

                    file.seek(START_S + i)  # Đi đến vị trí trạng thái của sinh viên thứ i
                    file.write(b'\x02')  # Ghi lại trạng thái đã mã hóa (2 là trạng thái đã mã hóa)
        else:
            file.seek(START_T)
            for _ in range(max_teacher_count):  # Đọc 100 phần tử trạng thái
                byte = file.read(1)
                if not byte:
                    break
                trang_thai = struct.unpack('<B', byte)[0]  # Đọc trạng thái từ file (little endian)
                trang_thai_ban_dau.append(trang_thai)

            # Đọc dữ liệu sinh viên từ file
            for i, trang_thai in enumerate(trang_thai_ban_dau):
                if trang_thai == 1:
                    file.seek(START_T + max_teacher_count + i * SUM_LEN)  # Đi đến vị trí dữ liệu của sinh viên thứ i

                    data = file.read(SUM_LEN)  # Đọc tổng kích thước của trường thông tin

                    # Mã hóa số điện thoại và CCCD
                    so_dien_thoai_mahoa = ma_hoa_thong_tin_2_chieu(str(struct.unpack('<Q', data[SUM_LEN - LEN_SO_DT - LEN_CCCD - LEN_KEY:SUM_LEN - LEN_SO_DT - LEN_CCCD - LEN_KEY + 8])[0]), key)
                    cccd_mahoa = ma_hoa_thong_tin_2_chieu(str(struct.unpack('<Q', data[SUM_LEN - LEN_CCCD - LEN_KEY:SUM_LEN - LEN_CCCD - LEN_KEY + 8])[0]), key)

                    # Điều chỉnh con trỏ để ghi dữ liệu đã mã hóa vào file
                    file.seek(START_T + max_teacher_count + i * SUM_LEN + LEN_MA_GV + LEN_HO_TEN + LEN_NGAY_SINH + LEN_NGAY_THAM_GIA)  # Đi đến vị trí số điện thoại đã mã hóa
                    file.write(so_dien_thoai_mahoa.ljust(LEN_SO_DT)[:LEN_SO_DT])  # Ghi lại số điện thoại đã mã hóa
                    file.write(cccd_mahoa.ljust(LEN_CCCD)[:LEN_CCCD])  # Ghi lại CCCD đã mã hóa

                    key_mahoa = hashlib.sha256(key.encode()).digest()

                    # Điều chỉnh con trỏ để ghi dữ liệu đã mã hóa vào file
                    file.seek(START_T + max_teacher_count + i * SUM_LEN + SUM_LEN - LEN_KEY)  # Đi đến vị trí thông tin key đã mã hóa
                    file.write(key_mahoa)  # Ghi lại thông tin key đã mã hóa

                    file.seek(START_T + i)  # Đi đến vị trí trạng thái của sinh viên thứ i
                    file.write(b'\x02')  # Ghi lại trạng thái đã mã hóa (2 là trạng thái đã mã hóa)
                
                    

def ma_hoa(file_name, max_teacher_count, max_student_count, START_S, is_student=True):
    
    
    # Đọc trạng thái ban đầu từ file
    trang_thai_ban_dau = []
    with open(file_name, 'rb+') as file:
        if is_student:
            ma_sv=input("Nhập mã sinh viên cần mã hóa: ")
            file.seek(START_S)
            for _ in range(max_student_count):  # Đọc phần tử trạng thái
                byte = file.read(1)
                if not byte:
                    break
                trang_thai = struct.unpack('<B', byte)[0]  # Đọc trạng thái từ file (little endian)
                trang_thai_ban_dau.append(trang_thai)

            # Đọc dữ liệu sinh viên từ file
            for i, trang_thai in enumerate(trang_thai_ban_dau):
                file.seek(START_S + max_student_count + i * SUM_LEN)  # Đi đến vị trí dữ liệu của sinh viên thứ i
                id=file.read(LEN_MA_SV).decode().strip() #Đọc mã sinh viên trong file
                if ma_sv==id:
                    if trang_thai==2:
                        print("Thông tin sinh viên này đã được mã hóa trước đó!")
                        return None
                    else:
                        key = input("Nhập key: ")
                    
                        file.seek(START_S + max_student_count + i * SUM_LEN)  # Đi đến vị trí dữ liệu của sinh viên thứ i

                        data = file.read(SUM_LEN)  # Đọc tổng kích thước của trường thông tin

                        # Mã hóa số điện thoại và CCCD
                        so_dien_thoai_mahoa = ma_hoa_thong_tin_2_chieu(str(struct.unpack('<Q', data[SUM_LEN - LEN_SO_DT - LEN_CCCD - LEN_KEY:SUM_LEN - LEN_SO_DT - LEN_CCCD - LEN_KEY + 8])[0]), key)
                        cccd_mahoa = ma_hoa_thong_tin_2_chieu(str(struct.unpack('<Q', data[SUM_LEN - LEN_CCCD - LEN_KEY:SUM_LEN - LEN_CCCD - LEN_KEY + 8])[0]), key)

                        # Điều chỉnh con trỏ để ghi dữ liệu đã mã hóa vào file
                        file.seek(START_S + max_student_count + i * SUM_LEN + LEN_MA_SV + LEN_HO_TEN + LEN_NGAY_SINH + LEN_NGAY_THAM_GIA)  # Đi đến vị trí số điện thoại đã mã hóa
                        file.write(so_dien_thoai_mahoa.ljust(LEN_SO_DT)[:LEN_SO_DT])  # Ghi lại số điện thoại đã mã hóa
                        file.write(cccd_mahoa.ljust(LEN_CCCD)[:LEN_CCCD])  # Ghi lại CCCD đã mã hóa

                        key_mahoa = hashlib.sha256(key.encode()).digest()

                        # Điều chỉnh con trỏ để ghi dữ liệu đã mã hóa vào file
                        file.seek(START_S + max_student_count + i * SUM_LEN + SUM_LEN - LEN_KEY)  # Đi đến vị trí thông tin key đã mã hóa
                        file.write(key_mahoa)  # Ghi lại thông tin key đã mã hóa

                        file.seek(START_S + i)  # Đi đến vị trí trạng thái của sinh viên thứ i
                        file.write(b'\x02')  # Ghi lại trạng thái đã mã hóa (2 là trạng thái đã mã hóa)
                        return
            
            print("Không tồn tại sinh viên có mã số ", ma_sv)
        else:
            ma_gv=input("Nhập mã giáo viên cần mã hóa: ")
            file.seek(START_T)
            for _ in range(max_teacher_count):  # Đọc phần tử trạng thái
                byte = file.read(1)
                if not byte:
                    break
                trang_thai = struct.unpack('<B', byte)[0]  # Đọc trạng thái từ file (little endian)
                trang_thai_ban_dau.append(trang_thai)

            # Đọc dữ liệu giáo viên từ file
            for i, trang_thai in enumerate(trang_thai_ban_dau):
                file.seek(START_T + max_teacher_count + i * SUM_LEN)  # Đi đến vị trí dữ liệu của giáo viên thứ i
                id=file.read(LEN_MA_GV).decode().strip() #Đọc mã giáo viên trong file
                if ma_gv==id:
                    if trang_thai==2:
                        print("Thông tin giáo viên này đã được mã hóa trước đó!")
                        return None
                    else:
                        key = input("Nhập key: ")
                    
                        file.seek(START_T + max_teacher_count + i * SUM_LEN)  # Đi đến vị trí dữ liệu của giáo viên thứ i

                        data = file.read(SUM_LEN)  # Đọc tổng kích thước của trường thông tin

                        # Mã hóa số điện thoại và CCCD
                        so_dien_thoai_mahoa = ma_hoa_thong_tin_2_chieu(str(struct.unpack('<Q', data[SUM_LEN - LEN_SO_DT - LEN_CCCD - LEN_KEY:SUM_LEN - LEN_SO_DT - LEN_CCCD - LEN_KEY + 8])[0]), key)
                        cccd_mahoa = ma_hoa_thong_tin_2_chieu(str(struct.unpack('<Q', data[SUM_LEN - LEN_CCCD - LEN_KEY:SUM_LEN - LEN_CCCD - LEN_KEY + 8])[0]), key)

                        # Điều chỉnh con trỏ để ghi dữ liệu đã mã hóa vào file
                        file.seek(START_T + max_teacher_count + i * SUM_LEN + LEN_MA_GV + LEN_HO_TEN + LEN_NGAY_SINH + LEN_NGAY_THAM_GIA)  # Đi đến vị trí số điện thoại đã mã hóa
                        file.write(so_dien_thoai_mahoa.ljust(LEN_SO_DT)[:LEN_SO_DT])  # Ghi lại số điện thoại đã mã hóa
                        file.write(cccd_mahoa.ljust(LEN_CCCD)[:LEN_CCCD])  # Ghi lại CCCD đã mã hóa

                        key_mahoa = hashlib.sha256(key.encode()).digest()

                        # Điều chỉnh con trỏ để ghi dữ liệu đã mã hóa vào file
                        file.seek(START_T + max_teacher_count + i * SUM_LEN + SUM_LEN - LEN_KEY)  # Đi đến vị trí thông tin key đã mã hóa
                        file.write(key_mahoa)  # Ghi lại thông tin key đã mã hóa

                        file.seek(START_T + i)  # Đi đến vị trí trạng thái của giáo viên thứ i
                        file.write(b'\x02')  # Ghi lại trạng thái đã mã hóa (2 là trạng thái đã mã hóa)
                        return
            
            print("Không tồn tại giáo viên có mã số ", ma_gv)


def giai_ma_tat_ca(file_name, max_teacher_count, max_student_count, START_S, is_student=True):
    key = input("Nhập mật khẩu chung: ")

    with open(file_name, 'r+b') as file:
        trang_thai_ban_dau = []
        if is_student:
            file.seek(START_S)
            for _ in range(max_student_count):
                byte = file.read(1)
                if not byte:
                    break
                trang_thai = struct.unpack('<B', byte)[0]
                trang_thai_ban_dau.append(trang_thai)

            for i, trang_thai in enumerate(trang_thai_ban_dau):
                if trang_thai == 2:  # Kiểm tra trạng thái đã mã hóa (2)
                    file.seek(START_S + max_student_count + i * SUM_LEN + SUM_LEN - LEN_KEY)  # Đến vị trí thông tin key đã mã hóa
                    key_file = file.read(LEN_KEY).strip()  # Đọc thông tin key đã mã hóa

                    # Kiểm tra thông tin key đã mã hóa bằng key chung
                    key_da_mahoa = hashlib.sha256(key.encode()).digest()
                    if key_da_mahoa == key_file:
                        file.seek(START_S + max_student_count + i * SUM_LEN + LEN_MA_SV + LEN_HO_TEN + LEN_NGAY_SINH + LEN_NGAY_THAM_GIA)  # Đến vị trí số điện thoại đã mã hóa
                        so_dien_thoai_mahoa = file.read(LEN_SO_DT).strip()  # Đọc số điện thoại đã mã hóa
                        cccd_mahoa = file.read(LEN_CCCD).strip()  # Đọc CCCD đã mã hóa

                        # Giải mã số điện thoại và CCCD
                        so_dien_thoai_giai_ma = giai_ma_thong_tin_2_chieu(so_dien_thoai_mahoa, key)
                        cccd_giai_ma = giai_ma_thong_tin_2_chieu(cccd_mahoa, key)

                        # Điều chỉnh con trỏ để ghi dữ liệu đã giải mã vào file
                        file.seek(START_S + max_student_count + i * SUM_LEN + LEN_MA_SV + LEN_HO_TEN + LEN_NGAY_SINH + LEN_NGAY_THAM_GIA)  # Đến vị trí số điện thoại đã mã hóa
                        if so_dien_thoai_giai_ma is not False and cccd_giai_ma is not False:
                            file.write(struct.pack('<Q', int(so_dien_thoai_giai_ma)).ljust(LEN_SO_DT)[:LEN_SO_DT])
                            file.write(struct.pack('<Q', int(cccd_giai_ma)).ljust(LEN_CCCD)[:LEN_CCCD])

                            # Điều chỉnh trạng thái thành 1 (chưa mã hóa)
                            file.seek(START_S + i)  # Đến vị trí trạng thái của sinh viên thứ i
                            file.write(b'\x01')  # Ghi lại trạng thái chưa mã hóa (1)
        
        else:
            file.seek(START_T)
            for _ in range(max_teacher_count):
                byte = file.read(1)
                if not byte:
                    break
                trang_thai = struct.unpack('<B', byte)[0]
                trang_thai_ban_dau.append(trang_thai)

            for i, trang_thai in enumerate(trang_thai_ban_dau):
                if trang_thai == 2:  # Kiểm tra trạng thái đã mã hóa (2)
                    file.seek(START_T + max_teacher_count + i * SUM_LEN + SUM_LEN - LEN_KEY)  # Đến vị trí thông tin key đã mã hóa
                    key_file = file.read(LEN_KEY).strip()  # Đọc thông tin key đã mã hóa

                    # Kiểm tra thông tin key đã mã hóa bằng key chung
                    key_da_mahoa = hashlib.sha256(key.encode()).digest()
                    if key_da_mahoa == key_file:
                        file.seek(START_T + max_teacher_count + i * SUM_LEN + LEN_MA_GV + LEN_HO_TEN + LEN_NGAY_SINH + LEN_NGAY_THAM_GIA)  # Đến vị trí số điện thoại đã mã hóa
                        so_dien_thoai_mahoa = file.read(LEN_SO_DT).strip()  # Đọc số điện thoại đã mã hóa
                        cccd_mahoa = file.read(LEN_CCCD).strip()  # Đọc CCCD đã mã hóa

                        # Giải mã số điện thoại và CCCD
                        so_dien_thoai_giai_ma = giai_ma_thong_tin_2_chieu(so_dien_thoai_mahoa, key)
                        cccd_giai_ma = giai_ma_thong_tin_2_chieu(cccd_mahoa, key)

                        # Điều chỉnh con trỏ để ghi dữ liệu đã giải mã vào file
                        file.seek(START_T + max_teacher_count + i * SUM_LEN + LEN_MA_GV + LEN_HO_TEN + LEN_NGAY_SINH + LEN_NGAY_THAM_GIA)  # Đến vị trí số điện thoại đã mã hóa
                        if so_dien_thoai_giai_ma is not False and cccd_giai_ma is not False:
                            file.write(struct.pack('<Q', int(so_dien_thoai_giai_ma)).ljust(LEN_SO_DT)[:LEN_SO_DT])
                            file.write(struct.pack('<Q', int(cccd_giai_ma)).ljust(LEN_CCCD)[:LEN_CCCD])

                            # Điều chỉnh trạng thái thành 1 (chưa mã hóa)
                            file.seek(START_T + i)  # Đến vị trí trạng thái của giáo viên thứ i
                            file.write(b'\x01')  # Ghi lại trạng thái chưa mã hóa (1)


def giai_ma(file_name, max_teacher_count, max_student_count, START_S, is_student=True):

    with open(file_name, 'r+b') as file:
        trang_thai_ban_dau = []
        if is_student:
            ma_sv = input("Nhập mã sinh viên cần giải mã thông tin: ")
            file.seek(START_S)
            for _ in range(max_student_count):
                byte = file.read(1)
                if not byte:
                    break
                trang_thai = struct.unpack('<B', byte)[0]
                trang_thai_ban_dau.append(trang_thai)

            for i, trang_thai in enumerate(trang_thai_ban_dau):
                file.seek(START_S + max_student_count + i * SUM_LEN)  # Đi đến vị trí dữ liệu của sinh viên thứ i
                id=file.read(LEN_MA_SV).decode().strip() #Đọc mã sinh viên trong file

                if ma_sv==id:
                    key=input("Nhập key giải mã: ")
                    key_da_mahoa = hashlib.sha256(key.encode()).digest()
                    file.seek(START_S + max_student_count + i * SUM_LEN + SUM_LEN - LEN_KEY)  # Đi đến vị trí dữ liệu key của sinh viên thứ i
                    key_sv=file.read(LEN_KEY).strip() 
                    
                    if trang_thai==1:
                        print("Thông tin sinh viên này đã được giải mã trước đó!")
                        return
                    elif trang_thai==2 and key_sv !=key_da_mahoa:
                        print("Key giải mã sai! ")
                        return
                    elif trang_thai==2 and key_sv == key_da_mahoa:
                        file.seek(START_S + max_student_count + i * SUM_LEN + LEN_MA_SV + LEN_HO_TEN + LEN_NGAY_SINH + LEN_NGAY_THAM_GIA)  # Đến vị trí số điện thoại đã mã hóa
                        so_dien_thoai_mahoa = file.read(LEN_SO_DT).strip()  # Đọc số điện thoại đã mã hóa
                        cccd_mahoa = file.read(LEN_CCCD).strip()  # Đọc CCCD đã mã hóa

                        # Giải mã số điện thoại và CCCD
                        so_dien_thoai_giai_ma = giai_ma_thong_tin_2_chieu(so_dien_thoai_mahoa, key)
                        cccd_giai_ma = giai_ma_thong_tin_2_chieu(cccd_mahoa, key)

                        # Điều chỉnh con trỏ để ghi dữ liệu đã giải mã vào file
                        file.seek(START_S + max_student_count + i * SUM_LEN + LEN_MA_SV + LEN_HO_TEN + LEN_NGAY_SINH + LEN_NGAY_THAM_GIA)  # Đến vị trí số điện thoại đã mã hóa
                        if so_dien_thoai_giai_ma is not False and cccd_giai_ma is not False:
                            file.write(struct.pack('<Q', int(so_dien_thoai_giai_ma)).ljust(LEN_SO_DT)[:LEN_SO_DT])
                            file.write(struct.pack('<Q', int(cccd_giai_ma)).ljust(LEN_CCCD)[:LEN_CCCD])

                            # Điều chỉnh trạng thái thành 1 (chưa mã hóa)
                            file.seek(START_S + i)  # Đến vị trí trạng thái của sinh viên thứ i
                            file.write(b'\x01')  # Ghi lại trạng thái chưa mã hóa (1)
                            print("Thông tin sinh viên này đã được giải mã thành công!")
                            return
                        else: print("Có lỗi trong quá trình giải mã, xin hãy thử lại!")
        
        else:
            ma_gv = input("Nhập mã giáo viên cần giải mã thông tin: ")
            file.seek(START_T)
            for _ in range(max_teacher_count):
                byte = file.read(1)
                if not byte:
                    break
                trang_thai = struct.unpack('<B', byte)[0]
                trang_thai_ban_dau.append(trang_thai)

            for i, trang_thai in enumerate(trang_thai_ban_dau):
                file.seek(START_T + max_teacher_count + i * SUM_LEN)  # Đi đến vị trí dữ liệu của sinh viên thứ i
                id=file.read(LEN_MA_GV).decode().strip() #Đọc mã sinh viên trong file

                if ma_gv==id:
                    key=input("Nhập key giải mã: ")
                    key_da_mahoa = hashlib.sha256(key.encode()).digest()
                    file.seek(START_T + max_teacher_count + i * SUM_LEN + SUM_LEN - LEN_KEY)  # Đi đến vị trí dữ liệu key của sinh viên thứ i
                    key_sv=file.read(LEN_KEY).strip() 
                    
                    if trang_thai==1:
                        print("Thông tin giáo viên này đã được giải mã trước đó!")
                        return
                    elif trang_thai==2 and key_sv !=key_da_mahoa:
                        print("Key giải mã sai! ")
                        return
                    elif trang_thai==2 and key_sv == key_da_mahoa:
                        file.seek(START_T + max_teacher_count + i * SUM_LEN + LEN_MA_GV + LEN_HO_TEN + LEN_NGAY_SINH + LEN_NGAY_THAM_GIA)  # Đến vị trí số điện thoại đã mã hóa
                        so_dien_thoai_mahoa = file.read(LEN_SO_DT).strip()  # Đọc số điện thoại đã mã hóa
                        cccd_mahoa = file.read(LEN_CCCD).strip()  # Đọc CCCD đã mã hóa

                        # Giải mã số điện thoại và CCCD
                        so_dien_thoai_giai_ma = giai_ma_thong_tin_2_chieu(so_dien_thoai_mahoa, key)
                        cccd_giai_ma = giai_ma_thong_tin_2_chieu(cccd_mahoa, key)

                        # Điều chỉnh con trỏ để ghi dữ liệu đã giải mã vào file
                        file.seek(START_T + max_teacher_count + i * SUM_LEN + LEN_MA_GV + LEN_HO_TEN + LEN_NGAY_SINH + LEN_NGAY_THAM_GIA)  # Đến vị trí số điện thoại đã mã hóa
                        if so_dien_thoai_giai_ma is not False and cccd_giai_ma is not False:
                            file.write(struct.pack('<Q', int(so_dien_thoai_giai_ma)).ljust(LEN_SO_DT)[:LEN_SO_DT])
                            file.write(struct.pack('<Q', int(cccd_giai_ma)).ljust(LEN_CCCD)[:LEN_CCCD])

                            # Điều chỉnh trạng thái thành 1 (chưa mã hóa)
                            file.seek(START_T + i)  # Đến vị trí trạng thái của giáo viên thứ i
                            file.write(b'\x01')  # Ghi lại trạng thái chưa mã hóa (1)
                            print("Thông tin giáo viên này đã được giải mã thành công!")
                            return
                        else: print("Có lỗi trong quá trình giải mã, xin hãy thử lại!")




def them(file_name, max_teacher_count, max_student_count, START_S, is_student=True):
    

    with open(file_name, 'r+b') as file:
        if is_student:
            print("Nhập thông tin sinh viên muốn thêm: ")
            trang_thai_ban_dau = []
            for _ in range(max_student_count):  # Đọc 100 phần tử trạng thái
                byte = file.read(1)
                if not byte:
                    break
                trang_thai = struct.unpack('<B', byte)[0]
                trang_thai_ban_dau.append(trang_thai)

            for i, trang_thai in enumerate(trang_thai_ban_dau):
                if trang_thai == 0:  # Tìm vị trí trống để thêm thông tin sinh viên
                    # Nhập thông tin sinh viên từ bàn phím
                    ma_sv = input("Nhập mã sinh viên: ")
                    ho_ten = input("Nhập họ và tên: ")
                    ngay_sinh = input("Nhập ngày sinh: ")
                    ngay_tham_gia = input("Nhập ngày tham gia: ")
                    so_dien_thoai = input("Nhập số điện thoại: ")
                    cccd = input("Nhập số CCCD: ")

                    # Ghi thông tin sinh viên vào file
                    file.seek(START_S + max_student_count + i * SUM_LEN)  # Di chuyển đến vị trí dữ liệu của sinh viên thứ i

                    # Ghi thông tin sinh viên vào file với độ dài cố định cho mỗi trường
                    file.write(ma_sv.encode('utf-8').ljust(LEN_MA_SV)[:LEN_MA_SV])
                    file.write(ho_ten.encode('utf-8').ljust(LEN_HO_TEN)[:LEN_HO_TEN])
                    file.write(ngay_sinh.encode('utf-8').ljust(LEN_NGAY_SINH)[:LEN_NGAY_SINH])
                    file.write(ngay_tham_gia.encode('utf-8').ljust(LEN_NGAY_THAM_GIA)[:LEN_NGAY_THAM_GIA])
                    file.write(struct.pack('<Q', int(so_dien_thoai)).ljust(LEN_SO_DT)[:LEN_SO_DT])
                    file.write(struct.pack('<Q', int(cccd)).ljust(LEN_CCCD)[:LEN_CCCD])

                    # Cập nhật trạng thái thành đã có sinh viên
                    file.seek(START_S + i)  # Di chuyển đến vị trí trạng thái của sinh viên thứ i
                    file.write(b'\x01')  # Ghi lại trạng thái đã có sinh viên (1)
                    print("Thêm sinh viên thành công!")
                    return

            # Trường hợp không có vị trí trống để thêm sinh viên mới
            print("Không có vị trí trống để thêm sinh viên mới.")
        
        else:
            print("Nhập thông tin giáo viên muốn thêm: ")
            trang_thai_ban_dau = []
            for _ in range(max_teacher_count): 
                byte = file.read(1)
                if not byte:
                    break
                trang_thai = struct.unpack('<B', byte)[0]
                trang_thai_ban_dau.append(trang_thai)

            for i, trang_thai in enumerate(trang_thai_ban_dau):
                if trang_thai == 0:  # Tìm vị trí trống để thêm thông tin giáo viên
                    # Nhập thông tin giáo viên từ bàn phím
                    ma_gv = input("Nhập mã giáo viên: ")
                    ho_ten = input("Nhập họ và tên: ")
                    ngay_sinh = input("Nhập ngày sinh: ")
                    ngay_tham_gia = input("Nhập ngày tham gia: ")
                    so_dien_thoai = input("Nhập số điện thoại: ")
                    cccd = input("Nhập số CCCD: ")

                    # Ghi thông tin giáo viên vào file
                    file.seek(START_T + max_teacher_count + i * SUM_LEN)  # Di chuyển đến vị trí dữ liệu của giáo viên thứ i

                    # Ghi thông tin giáo viên vào file với độ dài cố định cho mỗi trường
                    file.write(ma_gv.encode('utf-8').ljust(LEN_MA_SV)[:LEN_MA_SV])
                    file.write(ho_ten.encode('utf-8').ljust(LEN_HO_TEN)[:LEN_HO_TEN])
                    file.write(ngay_sinh.encode('utf-8').ljust(LEN_NGAY_SINH)[:LEN_NGAY_SINH])
                    file.write(ngay_tham_gia.encode('utf-8').ljust(LEN_NGAY_THAM_GIA)[:LEN_NGAY_THAM_GIA])
                    file.write(struct.pack('<Q', int(so_dien_thoai)).ljust(LEN_SO_DT)[:LEN_SO_DT])
                    file.write(struct.pack('<Q', int(cccd)).ljust(LEN_CCCD)[:LEN_CCCD])

                    # Cập nhật trạng thái thành đã có giáo viên
                    file.seek(START_T + i)  # Di chuyển đến vị trí trạng thái của giáo viên thứ i
                    file.write(b'\x01')  # Ghi lại trạng thái đã có giáo viên (1)
                    print("Thêm giáo viên thành công!")
                    return

            # Trường hợp không có vị trí trống để thêm giáo viên mới
            print("Không có vị trí trống để thêm giáo viên mới.")



def sua(file_name, max_teacher_count, max_student_count, START_S, is_student=True):

    with open(file_name, 'r+b') as file:
        if is_student:
            ma_sv = input("Nhập mã sinh viên cần sửa thông tin: ")
            trang_thai_ban_dau = []
            file.seek(START_S)
            for _ in range(max_student_count):  # Đọc phần tử trạng thái
                byte = file.read(1)
                if not byte:
                    break
                trang_thai = struct.unpack('<B', byte)[0]
                trang_thai_ban_dau.append(trang_thai)

            for i, trang_thai in enumerate(trang_thai_ban_dau):
                file.seek(START_S + max_student_count + i * SUM_LEN)  # Đi đến vị trí dữ liệu của sinh viên thứ i
                id = file.read(LEN_MA_SV).decode().strip()  # Đọc mã sinh viên từ file

                if ma_sv == id:
                    print(trang_thai,"-----------------------------------")
                    if trang_thai == 2:
                        print("Không thể sửa thông tin vì sinh viên này đã được mã hóa!")
                        return None
                    elif trang_thai == 1:
                        # Đọc thông tin sinh viên từ file
                        file.seek(START_S + max_student_count + i * SUM_LEN)  # Đi đến vị trí dữ liệu của sinh viên thứ i

                        ma_sv_moi = input("Nhập mã sinh viên mới: ")
                        ho_ten_moi = input("Nhập họ và tên mới: ")
                        ngay_sinh_moi = input("Nhập ngày sinh mới: ")
                        ngay_tham_gia_moi = input("Nhập ngày tham gia mới: ")
                        so_dien_thoai_moi = input("Nhập số điện thoại mới: ")
                        cccd_moi = input("Nhập số CCCD mới: ")

                        # Ghi thông tin sinh viên mới vào file
                        file.write(ma_sv_moi.encode('utf-8').ljust(LEN_MA_SV)[:LEN_MA_SV])
                        file.write(ho_ten_moi.encode('utf-8').ljust(LEN_HO_TEN)[:LEN_HO_TEN])
                        file.write(ngay_sinh_moi.encode('utf-8').ljust(LEN_NGAY_SINH)[:LEN_NGAY_SINH])
                        file.write(ngay_tham_gia_moi.encode('utf-8').ljust(LEN_NGAY_THAM_GIA)[:LEN_NGAY_THAM_GIA])
                        file.write(struct.pack('<Q', int(so_dien_thoai_moi)).ljust(LEN_SO_DT)[:LEN_SO_DT])
                        file.write(struct.pack('<Q', int(cccd_moi)).ljust(LEN_CCCD)[:LEN_CCCD])

                        print("Thông tin sinh viên được cập nhật thành công!")
                        return

            # Nếu không tìm thấy mã sinh viên trong file
            print("Không tìm thấy sinh viên có mã số", ma_sv)
            
        else:
            ma_gv = input("Nhập mã giáo viên cần sửa thông tin: ")
            trang_thai_ban_dau = []
            file.seek(START_T)
            for _ in range(max_teacher_count):  # Đọc phần tử trạng thái
                byte = file.read(1)
                if not byte:
                    break
                trang_thai = struct.unpack('<B', byte)[0]
                trang_thai_ban_dau.append(trang_thai)

            for i, trang_thai in enumerate(trang_thai_ban_dau):
                file.seek(START_T + max_teacher_count + i * SUM_LEN)  # Đi đến vị trí dữ liệu của giáo viên thứ i
                id = file.read(LEN_MA_GV).decode().strip()  # Đọc mã giáo viên từ file

                if ma_gv == id:
                    if trang_thai == 2:
                        print("Không thể sửa thông tin vì giáo viên này đã được mã hóa!")
                        return None
                    elif trang_thai == 1:
                        # Đọc thông tin giáo viên từ file
                        file.seek(START_T + max_teacher_count + i * SUM_LEN)  # Đi đến vị trí dữ liệu của giáo viên thứ i

                        ma_gv_moi = input("Nhập mã giáo viên mới: ")
                        ho_ten_moi = input("Nhập họ và tên mới: ")
                        ngay_sinh_moi = input("Nhập ngày sinh mới: ")
                        ngay_tham_gia_moi = input("Nhập ngày tham gia mới: ")
                        so_dien_thoai_moi = input("Nhập số điện thoại mới: ")
                        cccd_moi = input("Nhập số CCCD mới: ")

                        # Ghi thông tin giáo viên mới vào file
                        file.write(ma_gv_moi.encode('utf-8').ljust(LEN_MA_GV)[:LEN_MA_GV])
                        file.write(ho_ten_moi.encode('utf-8').ljust(LEN_HO_TEN)[:LEN_HO_TEN])
                        file.write(ngay_sinh_moi.encode('utf-8').ljust(LEN_NGAY_SINH)[:LEN_NGAY_SINH])
                        file.write(ngay_tham_gia_moi.encode('utf-8').ljust(LEN_NGAY_THAM_GIA)[:LEN_NGAY_THAM_GIA])
                        file.write(struct.pack('<Q', int(so_dien_thoai_moi)).ljust(LEN_SO_DT)[:LEN_SO_DT])
                        file.write(struct.pack('<Q', int(cccd_moi)).ljust(LEN_CCCD)[:LEN_CCCD])

                        print("Thông tin giáo viên được cập nhật thành công!")
                        return

            # Nếu không tìm thấy mã giáo viên trong file
            print("Không tìm thấy giáo viên có mã số", ma_gv)



def xoa(file_name, max_teacher_count, max_student_count, START_S, is_student=True):

    with open(file_name, 'r+b') as file:
        if is_student:
            ma_sv = input("Nhập mã sinh viên cần xóa: ")
            lua_chon = input("Bạn muốn xóa hoàn toàn (nhập '1') hay xóa cho phục hồi (nhập '2'): ")
            trang_thai_ban_dau = []
            file.seek(START_S)
            for _ in range(max_student_count):  # Đọc 100 phần tử trạng thái
                byte = file.read(1)
                if not byte:
                    break
                trang_thai = struct.unpack('<B', byte)[0]
                trang_thai_ban_dau.append(trang_thai)

            for i, trang_thai in enumerate(trang_thai_ban_dau):
                file.seek(START_S + max_student_count + i * SUM_LEN)  # Đi đến vị trí dữ liệu của sinh viên thứ i
                id = file.read(LEN_MA_SV).decode().strip()  # Đọc mã sinh viên từ file

                if ma_sv == id:
                    if trang_thai == 2:
                        print("Không thể xóa vì sinh viên này đã được mã hóa!")
                        return None
                    elif trang_thai == 1 and lua_chon == '2':
                        file.seek(START_S + i)  # Đi đến vị trí trạng thái của sinh viên thứ i
                        file.write(b'\x03')  # Xóa cho phục hồi (3 là trạng thái xóa nhưng có thể phục hồi)
                        print("Sinh viên đã được đánh dấu xóa nhưng có thể phục hồi!")
                        return
                    elif trang_thai == 1 and lua_chon == '1':
                        file.seek(START_S + i)  # Đi đến vị trí trạng thái của sinh viên thứ i
                        file.write(b'\x00')  # Set trạng thái về 0 (xóa hoàn toàn)
                        file.seek(START_S + max_student_count + i * SUM_LEN) 
                        # Set các byte thông tin của sinh viên = 0
                        file.write(b'\0' * SUM_LEN)
                        print("Sinh viên đã bị xóa hoàn toàn!")
                        return

            # Nếu không tìm thấy mã sinh viên trong file
            print("Không tìm thấy sinh viên", ma_sv)
            
        else:
            ma_gv = input("Nhập mã giáo viên cần xóa: ")
            lua_chon = input("Bạn muốn xóa hoàn toàn (nhập '1') hay xóa cho phục hồi (nhập '2'): ")
            trang_thai_ban_dau = []
            file.seek(START_T)
            for _ in range(max_teacher_count):  # Đọc 100 phần tử trạng thái
                byte = file.read(1)
                if not byte:
                    break
                trang_thai = struct.unpack('<B', byte)[0]
                trang_thai_ban_dau.append(trang_thai)

            for i, trang_thai in enumerate(trang_thai_ban_dau):
                file.seek(START_T + max_teacher_count + i * SUM_LEN)  # Đi đến vị trí dữ liệu của giáo viên thứ i
                id = file.read(LEN_MA_GV).decode().strip()  # Đọc mã giáo viên từ file

                if ma_gv == id:
                    if trang_thai == 2:
                        print("Không thể xóa vì giáo viên này đã được mã hóa!")
                        return None
                    elif trang_thai == 1 and lua_chon == '2':
                        file.seek(START_T + i)  # Đi đến vị trí trạng thái của giáo viên thứ i
                        file.write(b'\x03')  # Xóa cho phục hồi (3 là trạng thái xóa nhưng có thể phục hồi)
                        print("giáo viên đã được đánh dấu xóa nhưng có thể phục hồi!")
                        return
                    elif trang_thai == 1 and lua_chon == '1':
                        file.seek(START_T + i)  # Đi đến vị trí trạng thái của giáo viên thứ i
                        file.write(b'\x00')  # Set trạng thái về 0 (xóa hoàn toàn)
                        file.seek(START_T + max_teacher_count + i * SUM_LEN) 
                        # Set các byte thông tin của giáo viên = 0
                        file.write(b'\0' * SUM_LEN)
                        print("giáo viên đã bị xóa hoàn toàn!")
                        return

            # Nếu không tìm thấy mã giáo viên trong file
            print("Không tìm thấy giáo viên", ma_gv)


def phuc_hoi(file_name, max_teacher_count, max_student_count, START_S, is_student=True):
    # Đọc trạng thái ban đầu từ file
    trang_thai_ban_dau = []
    with open(file_name, 'r+b') as file:
        if is_student:
            file.seek(START_S)
            for _ in range(max_student_count):  # Đọc phần tử trạng thái
                byte = file.read(1)
                if not byte:
                    break
                trang_thai = struct.unpack('<B', byte)[0]  # Đọc trạng thái từ file (little endian)
                trang_thai_ban_dau.append(trang_thai)

            # Đọc dữ liệu sinh viên từ file
            danh_sach_sinh_vien = []
            count = 0
            for i, trang_thai in enumerate(trang_thai_ban_dau):
                if trang_thai == 3:  # Nếu trạng thái là 1, có sinh viên, thì đọc dữ liệu của sinh viên
                    file.seek(START_S + max_student_count + i * SUM_LEN)  # Di chuyển đến vị trí dữ liệu của sinh viên thứ i

                    data = file.read(SUM_LEN) 

                    ma = data[:LEN_MA_SV].decode('utf-8').strip()
                    ho_ten = data[LEN_MA_SV:LEN_MA_SV + LEN_HO_TEN].decode('utf-8').strip()
                    ngay_sinh = data[LEN_MA_SV + LEN_HO_TEN:LEN_MA_SV + LEN_HO_TEN + LEN_NGAY_SINH].decode('utf-8').strip()
                    ngay_tham_gia = data[LEN_MA_SV + LEN_HO_TEN + LEN_NGAY_SINH:LEN_MA_SV + LEN_HO_TEN + LEN_NGAY_SINH + LEN_NGAY_THAM_GIA].decode('utf-8').strip()
                    so_dien_thoai = str(struct.unpack('<Q', data[LEN_MA_SV + LEN_HO_TEN + LEN_NGAY_SINH + LEN_NGAY_THAM_GIA:LEN_MA_SV + LEN_HO_TEN + LEN_NGAY_SINH + LEN_NGAY_THAM_GIA + 8])[0])
                    cccd = str(struct.unpack('<Q', data[SUM_LEN - LEN_KEY - LEN_CCCD:SUM_LEN - LEN_KEY - LEN_CCCD + 8 ])[0])
                    so_dien_thoai = so_dien_thoai.zfill(10)
                    cccd = cccd.zfill(15)
                    sinh_vien = {
                        'Ma': ma,
                        'HoTen': ho_ten,
                        'NgaySinh': ngay_sinh,
                        'NgayThamGia': ngay_tham_gia,
                        'SoDT': so_dien_thoai,
                        'CCCD': cccd
                    }
                    count += 1
                    danh_sach_sinh_vien.append(sinh_vien)
            
            if count == 0: 
                print("Không có sinh viên nào để phục hồi!")
                return
            else:
                print(pd.DataFrame(danh_sach_sinh_vien))
                
                ma_sv = input("Nhập mã số sinh viên cần phục hồi: ")
                
                for i, trang_thai in enumerate(trang_thai_ban_dau):
                    file.seek(START_S + max_student_count + i * SUM_LEN)  # Đi đến vị trí dữ liệu của sinh viên thứ i
                    id = file.read(LEN_MA_SV).decode().strip()  # Đọc mã sinh viên từ file
                    if ma_sv == id:
                        if trang_thai == 3:
                            file.seek(START_S + i)  # Đi đến vị trí trạng thái của sinh viên thứ i
                            file.write(b'\x01')  # Phục hồi (1 là trạng thái bình thường)
                            print("Phục hồi sinh viên thành công!")
                            return None
                print("Không tìm thấy sinh viên", ma_sv)
                
        else:
            file.seek(START_T)
            for _ in range(max_teacher_count):  # Đọc phần tử trạng thái
                byte = file.read(1)
                if not byte:
                    break
                trang_thai = struct.unpack('<B', byte)[0]  # Đọc trạng thái từ file (little endian)
                trang_thai_ban_dau.append(trang_thai)

            # Đọc dữ liệu giáo viên từ file
            danh_sach_sinh_vien = []
            count = 0
            for i, trang_thai in enumerate(trang_thai_ban_dau):
                if trang_thai == 3:  # Nếu trạng thái là 1, có giáo viên, thì đọc dữ liệu của giáo viên
                    file.seek(START_T + max_teacher_count + i * SUM_LEN)  # Di chuyển đến vị trí dữ liệu của giáo viên thứ i

                    data = file.read(SUM_LEN) 

                    ma = data[:LEN_MA_GV].decode('utf-8').strip()
                    ho_ten = data[LEN_MA_GV:LEN_MA_GV + LEN_HO_TEN].decode('utf-8').strip()
                    ngay_sinh = data[LEN_MA_GV + LEN_HO_TEN:LEN_MA_GV + LEN_HO_TEN + LEN_NGAY_SINH].decode('utf-8').strip()
                    ngay_tham_gia = data[LEN_MA_GV + LEN_HO_TEN + LEN_NGAY_SINH:LEN_MA_GV + LEN_HO_TEN + LEN_NGAY_SINH + LEN_NGAY_THAM_GIA].decode('utf-8').strip()
                    so_dien_thoai = str(struct.unpack('<Q', data[LEN_MA_GV + LEN_HO_TEN + LEN_NGAY_SINH + LEN_NGAY_THAM_GIA:LEN_MA_GV + LEN_HO_TEN + LEN_NGAY_SINH + LEN_NGAY_THAM_GIA + 8])[0])
                    cccd = str(struct.unpack('<Q', data[SUM_LEN - LEN_KEY - LEN_CCCD:SUM_LEN - LEN_KEY - LEN_CCCD + 8 ])[0])
                    so_dien_thoai = so_dien_thoai.zfill(10)
                    cccd = cccd.zfill(15)        
                    sinh_vien = {
                        'Ma': ma,
                        'HoTen': ho_ten,
                        'NgaySinh': ngay_sinh,
                        'NgayThamGia': ngay_tham_gia,
                        'SoDT': so_dien_thoai,
                        'CCCD': cccd
                    }
                    count += 1
                    danh_sach_sinh_vien.append(sinh_vien)
            
            if count == 0: 
                print("Không có giáo viên nào để phục hồi!")
                return
            else:
                print(pd.DataFrame(danh_sach_sinh_vien))
                
                ma_gv = input("Nhập mã số giáo viên cần phục hồi: ")
                
                for i, trang_thai in enumerate(trang_thai_ban_dau):
                    file.seek(START_T + max_teacher_count + i * SUM_LEN)  # Đi đến vị trí dữ liệu của giáo viên thứ i
                    id = file.read(LEN_MA_GV).decode().strip()  # Đọc mã giáo viên từ file
                    if ma_gv == id:
                        if trang_thai == 3:
                            file.seek(START_T + i)  # Đi đến vị trí trạng thái của giáo viên thứ i
                            file.write(b'\x01')  # Phục hồi (1 là trạng thái bình thường)
                            print("Phục hồi giáo viên thành công!")
                            return None
                print("Không tìm thấy giáo viên", ma_gv)


def liet_ke(file_name, max_teacher_count, max_student_count, START_S, is_student=True):

    danh_sach_sinh_vien = []
    with open(file_name, 'rb') as file:
        if is_student:
            ma_sv_bat_dau = input("Nhập mã sinh viên bắt đầu: ")
            do_dai_doan = int(input("Nhập độ dài đoạn cần liệt kê: "))
            trang_thai_ban_dau = []
            danh_sach_sinh_vien = []
            file.seek(START_S)
            for _ in range(max_student_count):  # Đọc 100 phần tử trạng thái
                byte = file.read(1)
                if not byte:
                    break
                trang_thai = struct.unpack('<B', byte)[0]
                trang_thai_ban_dau.append(trang_thai)

            found_start = False  # Biến để xác định đã tìm thấy mã SV bắt đầu hay chưa
            count = 0  # Biến đếm để kiểm soát độ dài đoạn cần liệt kê
            for i, trang_thai in enumerate(trang_thai_ban_dau):
                file.seek(START_S + max_student_count + i * SUM_LEN)  # Đi đến vị trí dữ liệu của sinh viên thứ i
                id = file.read(LEN_MA_SV).decode().strip()  # Đọc mã sinh viên từ file

                if id == ma_sv_bat_dau and (trang_thai == 1 or trang_thai == 2):
                    found_start = True  # Đã tìm thấy mã SV bắt đầu

                if found_start:
                    if trang_thai == 1 or trang_thai == 2:  # Nếu trạng thái là 1 hoặc 2, có sinh viên, thì đọc dữ liệu của sinh viên
                        file.seek(START_S + max_student_count + i * SUM_LEN)  # Di chuyển đến vị trí dữ liệu của sinh viên thứ i

                        data = file.read(SUM_LEN)  # Đọc 6 trường thông tin cho một sinh viên

                        ma = data[:LEN_MA_SV].decode('utf-8').strip()
                        ho_ten = data[LEN_MA_SV:LEN_MA_SV + LEN_HO_TEN].decode('utf-8').strip()
                        ngay_sinh = data[LEN_MA_SV + LEN_HO_TEN:LEN_MA_SV + LEN_HO_TEN + LEN_NGAY_SINH].decode('utf-8').strip()
                        ngay_tham_gia = data[LEN_MA_SV + LEN_HO_TEN + LEN_NGAY_SINH:LEN_MA_SV + LEN_HO_TEN + LEN_NGAY_SINH + LEN_NGAY_THAM_GIA].decode('utf-8').strip()
                        so_dien_thoai = str(struct.unpack('<Q', data[LEN_MA_SV + LEN_HO_TEN + LEN_NGAY_SINH + LEN_NGAY_THAM_GIA:LEN_MA_SV + LEN_HO_TEN + LEN_NGAY_SINH + LEN_NGAY_THAM_GIA + 8])[0])
                        cccd = str(struct.unpack('<Q', data[SUM_LEN - LEN_KEY - LEN_CCCD:SUM_LEN - LEN_KEY - LEN_CCCD + 8 ])[0])
                        so_dien_thoai = so_dien_thoai.zfill(10)
                        cccd = cccd.zfill(15)
                        
                        sinh_vien = {
                            'Ma': ma,
                            'HoTen': ho_ten,
                            'NgaySinh': ngay_sinh,
                            'NgayThamGia': ngay_tham_gia,
                            'SoDT': so_dien_thoai,
                            'CCCD': cccd
                        }
                        danh_sach_sinh_vien.append(sinh_vien)
                        count += 1  # Tăng biến đếm               
                        
                        if count == do_dai_doan:  # Kiểm tra nếu đã liệt kê đủ độ dài đoạn cần tìm
                            print(pd.DataFrame(danh_sach_sinh_vien))    
                            return
            if(START_S + i == START_S + max_student_count - 1 and found_start):
                print(pd.DataFrame(danh_sach_sinh_vien))    
                return    
            if not found_start:  # Nếu không tìm thấy mã SV bắt đầu
                print("Không tìm thấy mã sinh viên bắt đầu:", ma_sv_bat_dau)
                
        else:
            ma_gv_bat_dau = input("Nhập mã giáo viên bắt đầu: ")
            do_dai_doan = int(input("Nhập độ dài đoạn cần liệt kê: "))
            trang_thai_ban_dau = []
            danh_sach_giao_vien = []
            file.seek(START_T)
            for _ in range(max_teacher_count):  # Đọc 100 phần tử trạng thái
                byte = file.read(1)
                if not byte:
                    break
                trang_thai = struct.unpack('<B', byte)[0]
                trang_thai_ban_dau.append(trang_thai)

            found_start = False  # Biến để xác định đã tìm thấy mã SV bắt đầu hay chưa
            count = 0  # Biến đếm để kiểm soát độ dài đoạn cần liệt kê
            for i, trang_thai in enumerate(trang_thai_ban_dau):
                file.seek(START_T + max_teacher_count + i * SUM_LEN)  # Đi đến vị trí dữ liệu của giáo viên thứ i
                id = file.read(LEN_MA_GV).decode().strip()  # Đọc mã giáo viên từ file

                if id == ma_gv_bat_dau and (trang_thai == 1 or trang_thai == 2):
                    found_start = True  # Đã tìm thấy mã SV bắt đầu

                if found_start:
                    if trang_thai == 1 or trang_thai == 2:  # Nếu trạng thái là 1 hoặc 2, có giáo viên, thì đọc dữ liệu của giáo viên
                        file.seek(START_T + max_teacher_count + i * SUM_LEN)  # Di chuyển đến vị trí dữ liệu của giáo viên thứ i

                        data = file.read(SUM_LEN)  # Đọc 6 trường thông tin cho một giáo viên

                        ma = data[:LEN_MA_GV].decode('utf-8').strip()
                        ho_ten = data[LEN_MA_GV:LEN_MA_GV + LEN_HO_TEN].decode('utf-8').strip()
                        ngay_sinh = data[LEN_MA_GV + LEN_HO_TEN:LEN_MA_GV + LEN_HO_TEN + LEN_NGAY_SINH].decode('utf-8').strip()
                        ngay_tham_gia = data[LEN_MA_GV + LEN_HO_TEN + LEN_NGAY_SINH:LEN_MA_GV + LEN_HO_TEN + LEN_NGAY_SINH + LEN_NGAY_THAM_GIA].decode('utf-8').strip()
                        so_dien_thoai = str(struct.unpack('<Q', data[LEN_MA_GV + LEN_HO_TEN + LEN_NGAY_SINH + LEN_NGAY_THAM_GIA:LEN_MA_GV + LEN_HO_TEN + LEN_NGAY_SINH + LEN_NGAY_THAM_GIA + 8])[0])
                        cccd = str(struct.unpack('<Q', data[SUM_LEN - LEN_KEY - LEN_CCCD:SUM_LEN - LEN_KEY - LEN_CCCD + 8 ])[0])
                        so_dien_thoai = so_dien_thoai.zfill(10)
                        cccd = cccd.zfill(15)
                        
                        giao_vien = {
                            'Ma': ma,
                            'HoTen': ho_ten,
                            'NgaySinh': ngay_sinh,
                            'NgayThamGia': ngay_tham_gia,
                            'SoDT': so_dien_thoai,
                            'CCCD': cccd
                        }
                        danh_sach_giao_vien.append(giao_vien)
                        count += 1  # Tăng biến đếm               
                        
                        if count == do_dai_doan:  # Kiểm tra nếu đã liệt kê đủ độ dài đoạn cần tìm
                            print(pd.DataFrame(danh_sach_giao_vien))    
                            return
            if(START_T + i == START_T + max_teacher_count - 1 and found_start):
                print(pd.DataFrame(danh_sach_giao_vien))    
                return    
            if not found_start:  # Nếu không tìm thấy mã SV bắt đầu
                print("Không tìm thấy mã giáo viên bắt đầu:", ma_gv_bat_dau)


def mo_file(file_name, count=0):
    if not os.path.exists(file_name):
        print("File không tồn tại!")
        return 0,0,0

    mat_khau_input = input("Nhập mật khẩu: ")

    with open(file_name, 'rb') as file:
        file.seek(-32, 2)  # Đọc 32 byte cuối cùng (mã hóa của mật khẩu)
        hashed_password = file.read()

        # So sánh mật khẩu đã mã hóa trong file và mật khẩu bạn nhập
        mat_khau_input_hashed = hashlib.sha256(mat_khau_input.encode()).digest()
        if mat_khau_input_hashed == hashed_password:
            print("Mật khẩu đúng!")

            c = 0
            while True:
                mk_dong = sinh_mat_khau()
                mk_dong_input = input('Nhập mật khẩu động: ')
                if mk_dong == mk_dong_input:
                    break
                c += 1
                if c == 3: 
                    print('Bạn đã nhập sai 3 lần, thoát chương trình!')
                    sys.exit()
                print('Mật khẩu động sai, vui lòng nhập lại!')
                
            file.seek(0)
            data = file.read(30)
            max_t_c = int(data[:SIZE_T].decode('utf-8').strip())
            max_s_c = int(data[SIZE_T:SIZE_T + SIZE_S].decode('utf-8').strip())
            start_s = int(data[SIZE_T + SIZE_S:SIZE_T + SIZE_S + POS_START_S].decode('utf-8').strip())
            return max_t_c, max_s_c, start_s

        else:
            # Mật khẩu không chính xác, thông báo hoặc xử lý theo ý muốn
            print("Mật khẩu không đúng!")
            a = input("Nhập 0 để thoát, nếu không thì tiếp tục nhập mật khẩu: ")
            if a == "0": 
                return 0,0,0
            count += 1
            if count >= 5:
                print("Bạn đã nhập sai mật khẩu quá nhiều lần. Vui lòng thử lại sau",2 * count, "giây nữa!")
                time.sleep(2 * count)  # Chờ nhiều hơn nếu nhập sai nhiều lần

            mo_file(file_name, count)


def menu():
    loop = True
    while True:
        
        print("Chọn một trong các lựa chọn sau:")
        print("1. Tạo file trống")
        print("2. Tạo file với dữ liệu mẫu")
        print("3. Mở file có sẵn")
        print("0. Thoát")

        choice = input("Nhập lựa chọn của bạn: ")
        
        if choice == '1':
            file_name = input("Nhap ten file cần tạo: ")
            m, n, s = tao_file_trong(file_name)
            while True:                             
                print("Chọn danh sách để thực hiện các thao tác:")
                print("1.Danh sách giáo viên")
                print("2.Danh sách sinh viên")
                print("0.Thoát")
                choice = input("Nhập lựa chọn của bạn: ")
                if choice == '1':
                    is_student = False
                elif choice == '2':
                    is_student = True
                elif choice == '0':
                    break
                while True:
                    print("Chọn một trong các lựa chọn sau:")
                    print("1. Hiển thị danh sách")
                    print("2. Mã hóa tất cả danh sách")
                    print("3. Giải mã tất cả danh sách")
                    print("4. Mã hóa từng phần tử")
                    print("5. Giải mã từng phần tử")
                    print("6. Thêm phần tử")
                    print("7. Xóa phần tử")
                    print("8. Sửa phần tử")
                    print("9. Liệt kê 1 đoạn")
                    print("10. Phục hồi phần tử")       
                    print("0. Thoát")
                    choice = input("Nhập lựa chọn của bạn: ")
                    if choice == '1':
                        doc_file(file_name, m, n, s, is_student)
                    elif choice == '2':
                        ma_hoa_tat_ca(file_name, m, n, s, is_student)
                    elif choice == '3':
                        giai_ma_tat_ca(file_name, m, n, s, is_student)
                    elif choice == '4':
                        ma_hoa(file_name, m, n, s, is_student)
                    elif choice == '5':
                        giai_ma(file_name, m, n, s, is_student)
                    elif choice == '6':
                        them(file_name, m, n, s, is_student)
                    elif choice == '7':
                        xoa(file_name, m, n, s, is_student)
                    elif choice == '8':
                        sua(file_name, m, n, s, is_student)
                    elif choice == '9':
                        liet_ke(file_name, m, n, s, is_student)
                    elif choice == '10':
                        phuc_hoi(file_name, m, n, s, is_student)
                    elif choice == '0':
                        break
                    else:
                        print("Lựa chọn không hợp lệ!")
                    
        elif choice == '2':
            file_name = input("Nhap ten file cần tạo: ")
            m, n, s = tao_file_voi_du_lieu_mau(file_name, danh_sach_giao_vien, danh_sach_sinh_vien)
            while True:        
                print("Chọn danh sách để thực hiện các thao tác:")
                print("1.Danh sách giáo viên")
                print("2.Danh sách sinh viên")
                print("3. Thoát")
                choice = input("Nhập lựa chọn của bạn: ")
                if choice == '1':
                    is_student = False
                elif choice == '2':
                    is_student = True
                elif choice == '3':
                    break
                while True:
                    print("Chọn một trong các lựa chọn sau:")
                    print("1. Hiển thị danh sách")
                    print("2. Mã hóa tất cả danh sách")
                    print("3. Giải mã tất cả danh sách")
                    print("4. Mã hóa từng phần tử")
                    print("5. Giải mã từng phần tử")
                    print("6. Thêm phần tử")
                    print("7. Xóa phần tử")
                    print("8. Sửa phần tử")
                    print("9. Liệt kê 1 đoạn")
                    print("10. Phục hồi phần tử")                    
                    print("0. Thoát")
                    choice = input("Nhập lựa chọn của bạn: ")
                    if choice == '1':
                        doc_file(file_name, m, n, s, is_student)
                    elif choice == '2':
                        ma_hoa_tat_ca(file_name, m, n, s, is_student)
                    elif choice == '3':
                        giai_ma_tat_ca(file_name, m, n, s, is_student)
                    elif choice == '4':
                        ma_hoa(file_name, m, n, s, is_student)
                    elif choice == '5':
                        giai_ma(file_name, m, n, s, is_student)
                    elif choice == '6':
                        them(file_name, m, n, s, is_student)
                    elif choice == '7':
                        xoa(file_name, m, n, s, is_student)
                    elif choice == '8':
                        sua(file_name, m, n, s, is_student)
                    elif choice == '9':
                        liet_ke(file_name, m, n, s, is_student)
                    elif choice == '10':
                        phuc_hoi(file_name, m, n, s, is_student)
                    elif choice == '0':
                        break
                    else:
                        print("Lựa chọn không hợp lệ!")
        elif choice == '3':
            file_name = input("Nhap ten file cần mở: ")
            m, n, s = mo_file(file_name)
            if m!=0:
                while True:            
                    print("Chọn danh sách để thực hiện các thao tác:")
                    print("1.Danh sách giáo viên")
                    print("2.Danh sách sinh viên")
                    print("3. Thoát")
                    choice = input("Nhập lựa chọn của bạn: ")
                    if choice == '1':
                        is_student = False
                    elif choice == '2':
                        is_student = True
                    elif choice == '3':
                        break
                    while True:
                        print("Chọn một trong các lựa chọn sau:")
                        print("1. Hiển thị danh sách")
                        print("2. Mã hóa tất cả danh sách")
                        print("3. Giải mã tất cả danh sách")
                        print("4. Mã hóa từng phần tử")
                        print("5. Giải mã từng phần tử")
                        print("6. Thêm phần tử")
                        print("7. Xóa phần tử")
                        print("8. Sửa phần tử")
                        print("9. Liệt kê 1 đoạn")
                        print("10. Phục hồi phần tử")       
                        print("0. Thoát")
                        choice = input("Nhập lựa chọn của bạn: ")
                        if choice == '1':
                            doc_file(file_name, m, n, s, is_student)
                        elif choice == '2':
                            ma_hoa_tat_ca(file_name, m, n, s, is_student)
                        elif choice == '3':
                            giai_ma_tat_ca(file_name, m, n, s, is_student)
                        elif choice == '4':
                            ma_hoa(file_name, m, n, s, is_student)
                        elif choice == '5':
                            giai_ma(file_name, m, n, s, is_student)
                        elif choice == '6':
                            them(file_name, m, n, s, is_student)
                        elif choice == '7':
                            xoa(file_name, m, n, s, is_student)
                        elif choice == '8':
                            sua(file_name, m, n, s, is_student)
                        elif choice == '9':
                            liet_ke(file_name, m, n, s, is_student)
                        elif choice == '10':
                            phuc_hoi(file_name, m, n, s, is_student)
                        elif choice == '0':
                            break
                        else:
                            print("Lựa chọn không hợp lệ!")
        elif choice == '0':
            print("Đã thoát.")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")


menu()
#file_name = input("Nhap ten file: ")
#m,n,s=mo_file(file_name, 0)

#m,n,s=tao_file_voi_du_lieu_mau("S1.dat", danh_sach_giao_vien, danh_sach_sinh_vien)
#m,n,s=tao_file_trong("S1.dat")
#ma_hoa_tat_ca(m,n,s,True)
#ma_hoa_tat_ca(m,n,s,False)
#giai_ma_tat_ca(m,n,s,True)
#giai_ma_tat_ca(m,n,s,False)
##ma_hoa(m,n,s,False)
#giai_ma(m,n,s,True)
#them(m,n,s,False)
#xoa(m,n,s,True)
#sua(m,n,s,False)
#liet_ke(m,n,s,True)



