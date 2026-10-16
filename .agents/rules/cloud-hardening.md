# Quy chuẩn Bảo mật Hạ tầng & Container (Cloud Hardening Rules)

> **Phạm vi áp dụng**: Mọi cấu hình Docker, Docker Compose, mạng nội bộ, MinIO Object Storage và các dịch vụ phụ trợ trong `CloudSec-Core`.  
> **Người thực hiện chính**: `@cloud-infra` | **Người kiểm toán**: `@sec-evaluator`, `@research-lead`.

---

## 1. Nguyên tắc An toàn Container (Docker Container Security)

1. **Quy tắc Phi-Root (Non-Root Execution)**:
   - Tất cả các container trong môi trường Lab (MinIO, Loki, Prometheus, App services) **CẤM** chạy dưới user `root` (UID 0).
   - Thiết lập `user: "10001:10001"` hoặc định nghĩa user chuyên dụng trong Dockerfile.
2. **Quyền hạn tối thiểu (Principle of Least Privilege)**:
   - Sử dụng cờ:
     ```yaml
     security_opt:
       - no-new-privileges:true
     cap_drop:
       - ALL
     ```
   - Chỉ cấp lại những capabilities tối thiểu cần thiết (ví dụ: `NET_BIND_SERVICE` nếu bắt buộc).
3. **Read-Only Root Filesystem**:
   - Nếu khả thi, mount root filesystem của container ở chế độ `read_only: true`.
   - Các thư mục cần ghi tạm thời (logs, tmp) sử dụng volume `tmpfs` có giới hạn kích thước (`size=128m`).

---

## 2. Cách ly Mạng (Network Segmentation & Isolation)

1. **Kiến trúc mạng hai lớp (Two-Tier Network)**:
   - `cloudsec-public-net`: Dành cho client bên ngoài kết nối tới Gateway hoặc reverse proxy.
   - `cloudsec-internal-storage-net`: Mạng nội bộ riêng biệt kết nối giữa Gateway/Crypto module và cụm MinIO S3. MinIO **KHÔNG** bind cổng trực tiếp ra `0.0.0.0` trên máy Host trong kịch bản sản xuất/thực nghiệm chuẩn.
2. **DNS & Firewall nội bộ**:
   - Chỉ cho phép các container có nhu cầu ghi nhận log (như MinIO) kết nối tới Promtail/Loki.

---

## 3. Cố định Tài nguyên cgroups để Đảm bảo Giá trị Thực nghiệm (Fair Benchmarking)

Để số liệu đo đạc throughput và độ trễ của `@sec-evaluator` đạt tính nhất quán khoa học và không bị ảnh hưởng bởi biến động CPU máy host:

1. **Giới hạn cứng CPU và Memory trong `docker-compose.yml`**:
   ```yaml
   services:
     minio:
       image: minio/minio:RELEASE.2024-01-01T00-00-00Z
       deploy:
         resources:
           limits:
             cpus: '2.0'
             memory: 2048M
           reservations:
             cpus: '1.0'
             memory: 1024M
   ```
2. **Cấm Swap**: Cấu hình `memswap_limit` tương đương với `memory_limit` để tránh ảnh hưởng độ trễ disk I/O do tráo đổi bộ nhớ ảo.

---

## 4. Quản lý Bí mật & Cấu hình (Secrets Management)

1. **Không lưu trữ Secret trong image**: Cấm dùng `ENV MINIO_ROOT_PASSWORD=...` trong Dockerfile.
2. **Sử dụng file `.env.example`**:
   - File cấu hình mẫu `.env.example` được commit lên Git với các giá trị giả định.
   - File `.env` thực tế nằm trong `.gitignore` và được nạp qua cơ chế biến môi trường Docker Compose.
