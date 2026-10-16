# TASK-CRYPTO-01: Phát triển Module mã hóa đầu cuối AES-256-GCM Streaming

- **Người phụ trách**: `@crypto-sec`
- **Độ ưu tiên**: P0 (Trọng tâm NCKH)
- **Trạng thái**: ACTIVE
- **Ngày tạo**: 2026-10-16

## Mục tiêu
Triển khai module mã hóa đầu cuối (Client-side Encryption) sử dụng thuật toán AES-256-GCM kết hợp kỹ thuật Envelope Encryption và Chunked Streaming tải trực tiếp lên MinIO S3.

## Các hạng mục công việc
1. [ ] Xây dựng `src/crypto/aes_gcm.py`:
   - Sinh Nonce ngẫu nhiên 96-bit (CSPRNG) cho mỗi payload/chunk.
   - Mã hóa và sinh 128-bit Authentication Tag.
   - Cơ chế AAD (Additional Authenticated Data) xác thực metadata người dùng.
2. [ ] Xây dựng `src/crypto/stream_cipher.py`:
   - Phân mảnh stream (Chunk size 5MB/10MB) hỗ trợ file lớn 100MB - 1GB không gây tràn RAM.
3. [ ] Xây dựng `src/kms/envelope.py`:
   - Cơ chế Master Key (KEK) và Data Key (DEK).
4. [ ] Viết bộ test `tests/crypto/test_aes_gcm.py`:
   - Kiểm thử Known Answer Test (KAT).
   - Kiểm thử phát hiện can thiệp dữ liệu (Data tampering).

## Tiêu chí hoàn thành (DoD)
- Vượt qua 100% unit tests.
- Tuân thủ chặt chẽ `crypto-standards.md` (Không lặp Nonce, không hardcode khóa).
