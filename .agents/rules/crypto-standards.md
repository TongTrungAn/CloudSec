# Quy chuẩn Mật mã học & Bảo mật Dữ liệu (Cryptographic Standards)

> **Phạm vi áp dụng**: Mọi đoạn mã liên quan đến sinh khóa, lưu trữ, truyền tải và mã hóa/giải mã dữ liệu trong dự án `CloudSec-Core`.  
> **Người thực hiện chính**: `@crypto-sec` | **Người kiểm toán**: `@sec-evaluator`, `@research-lead`.

---

## 1. Thuật toán và Chế độ hoạt động được phép

| Mục đích | Thuật toán bắt buộc | Độ dài khóa / Tham số | Tiêu chuẩn tham chiếu |
| :--- | :--- | :--- | :--- |
| **Mã hóa dữ liệu (Payload Encryption)** | **AES-GCM** (Ưu tiên) | Khóa: 256-bit (`AES-256`), Nonce/IV: 96-bit, Auth Tag: 128-bit | NIST SP 800-38D |
| **Mã hóa thay thế (Thiết bị không có AES-NI)** | **ChaCha20-Poly1305** | Khóa: 256-bit, Nonce: 96-bit, Tag: 128-bit | RFC 8439 / RFC 7539 |
| **Dẫn xuất khóa (Key Derivation - KDF)** | **Argon2id** (hoặc PBKDF2-HMAC-SHA256) | Iterations $\ge 600,000$ (PBKDF2) hoặc $m=64\text{MB}, t=3, p=4$ (Argon2id) | OWASP Key Derivation Guide |
| **Xác thực toàn vẹn độc lập (MAC)** | **HMAC-SHA256** | Key $\ge 256$-bit | FIPS 198-1 |
| **Sinh số ngẫu nhiên an toàn** | **CSPRNG** | `secrets.token_bytes()` hoặc `os.urandom()` trong Python | PEP 506 |

---

## 2. Các quy tắc CẤM TUYỆT ĐỐI (Strict Prohibitions)

1. **CẤM chế độ ECB (Electronic Codebook)**:
   - Tuyệt đối không dùng `AES.MODE_ECB` trong bất kỳ trường hợp nào vì để lộ mô hình cấu trúc dữ liệu (Leakage of data patterns).
2. **CẤM chế độ CBC không có HMAC (Encrypt-then-MAC)**:
   - Không dùng AES-CBC đơn lẻ; nếu dùng CBC bắt buộc phải kèm HMAC theo chuẩn Encrypt-then-MAC để chống tấn công Padding Oracle. Khuyến nghị dùng trực tiếp AEAD (GCM).
3. **CẤM tái sử dụng Nonce/IV (Nonce Reuse)**:
   - Trong AES-GCM, việc dùng trùng cặp `(Key, Nonce)` với hai bản rõ khác nhau sẽ làm lộ khóa xác thực GHASH và phá hủy hoàn toàn tính toàn vẹn của hệ thống.
   - **Quy chuẩn**: Mỗi lần mã hóa một khối/file/stream, BẮT BUỘC sinh mới một Nonce 96-bit (12 bytes) ngẫu nhiên từ CSPRNG.
4. **CẤM tự viết thuật toán mã hóa (No Roll-Your-Own-Crypto)**:
   - Chỉ sử dụng các thư viện đã được kiểm toán nghiêm ngặt: `cryptography` (Python Cryptographic Authority) hoặc `pycryptodome`.
5. **CẤM Hardcode khóa hoặc bí mật trong Git**:
   - Không bao giờ đặt khóa bí mật, passphrases, hoặc API tokens trực tiếp trong code. Tất cả phải được truyền qua biến môi trường (`.env`), Secrets Manager hoặc KMS.

---

## 3. Cấu trúc đóng gói tệp mã hóa (Encrypted File Envelope Format)

Mọi tệp hoặc stream khi lưu trữ lên MinIO S3 phải tuân theo cấu trúc Header chuẩn hóa:

```
+-------------------------------------------------------------------+
| Magic Header (4 bytes): b"CSEC"                                  |
+-------------------------------------------------------------------+
| Version (1 byte): 0x01                                            |
+-------------------------------------------------------------------+
| Cipher Suite (1 byte): 0x01 = AES-256-GCM | 0x02 = ChaCha20-Poly  |
+-------------------------------------------------------------------+
| Key ID / Encrypted DEK Length (2 bytes, unsigned short, big-endian)|
+-------------------------------------------------------------------+
| Encrypted DEK (Khóa dữ liệu mã hóa bằng Master Key - KEK)          |
+-------------------------------------------------------------------+
| Nonce / IV (12 bytes)                                             |
+-------------------------------------------------------------------+
| Payload (Ciphertext stream)                                       |
+-------------------------------------------------------------------+
| Authentication Tag (16 bytes)                                    |
+-------------------------------------------------------------------+
```

---

## 4. Xử lý an toàn bộ nhớ (Zeroization)

- Đối với các biến lưu trữ bản rõ của khóa (`bytes` hoặc `bytearray`), sau khi hoàn thành thao tác mã hóa/giải mã, module phải hỗ trợ ghi đè dữ liệu bằng byte `0x00` trước khi thu hồi bộ nhớ để tránh lưu vết trong memory dumps:
  ```python
  def zeroize_key(key_buffer: bytearray):
      for i in range(len(key_buffer)):
          key_buffer[i] = 0
  ```

---

## 5. Xử lý lỗi giải mã (Timing Attack & Padding Oracle Prevention)

- Khi giải mã thất bại (Auth tag mismatch hoặc header không hợp lệ), hàm giải mã BẮT BUỘC trả về một thông báo lỗi duy nhất:
  `DecryptionFailedException: "Authentication failed or ciphertext corrupted."`
- Tuyệt đối không phân tách thông báo: *"Sai padding"*, *"Sai độ dài"*, hay *"Sai tag"*, nhằm triệt tiêu kênh dẫn rò rỉ thông tin qua thời gian hoặc mã lỗi (Error Oracle).
