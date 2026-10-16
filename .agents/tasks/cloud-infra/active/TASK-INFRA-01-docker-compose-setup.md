# TASK-INFRA-01: Thiết lập cụm Docker Compose (MinIO, Loki, Promtail)

- **Người phụ trách**: `@cloud-infra`
- **Độ ưu tiên**: P0 (Blocker)
- **Trạng thái**: ACTIVE
- **Ngày tạo**: 2026-10-16

## Mục tiêu
Dựng môi trường hạ tầng Private Cloud thu nhỏ cho dự án `CloudSec-Core` bao gồm MinIO Object Storage và hệ thống thu thập log thời gian thực.

## Các hạng mục công việc
1. [ ] Viết file `deploy/docker-compose.yml`:
   - Dịch vụ `minio`: port 9000 (API), port 9001 (Console UI), cgroups limits (2 CPU, 2GB RAM).
   - Dịch vụ `loki`: port 3100.
   - Dịch vụ `promtail`: giám sát file log truy cập của MinIO.
2. [ ] Tạo file cấu hình `config/infra/promtail-config.yml` và `config/infra/loki-config.yml`.
3. [ ] Viết script `scripts/infra/healthcheck.py` để kiểm tra kết nối MinIO và Loki.
4. [ ] Tạo bucket mặc định `cloudsec-encrypted-vault`.

## Tiêu chí hoàn thành (DoD)
- Container khởi động không chạy quyền root.
- MinIO và Loki trả về HTTP 200 khi chạy healthcheck script.
