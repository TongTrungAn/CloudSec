# TASK-EVAL-01: Xây dựng Bộ công cụ đo Benchmark Mật mã & Giả lập Tấn công

- **Người phụ trách**: `@sec-evaluator`
- **Độ ưu tiên**: P0 (Thực nghiệm khoa học)
- **Trạng thái**: ACTIVE
- **Ngày tạo**: 2026-10-16

## Mục tiêu
Thiết kế bộ harness tự động đo đạc Throughput, Latency, CPU/RAM footprint và thực thi các kịch bản kiểm thử xâm nhập (Penetration Testing) lên hệ thống CloudSec-Core.

## Các hạng mục công việc
1. [ ] Xây dựng `benchmarks/run_crypto_benchmark.py`:
   - Đo Throughput (MB/s) và Latency ($\mu\text{s}$) với 30 vòng lặp cho các dải kích thước: 1MB, 10MB, 50MB, 100MB.
   - So sánh giữa 3 chế độ: Plaintext (Baseline), AES-256-GCM, ChaCha20-Poly1305.
   - Giám sát CPU/RAM qua `psutil`.
2. [ ] Xây dựng `benchmarks/generate_plots.py`:
   - Vẽ biểu đồ cột Throughput so sánh chuẩn IEEE (`reports/crypto_overhead.png`).
   - Xuất bảng tóm tắt kết quả `reports/benchmark_summary.md`.
3. [ ] Xây dựng bộ scripts giả lập tấn công `scripts/attacks/`:
   - `attack_bruteforce_s3.py`: Gửi request xác thực sai liên tiếp.
   - `attack_data_tampering.py`: Sửa đổi bit dữ liệu đã mã hóa trong S3 bucket.

## Tiêu chí hoàn thành (DoD)
- Số liệu thống kê có đủ giá trị Trung bình (Mean), Độ lệch chuẩn (Std Dev) và Phân vị P95/P99.
- Biểu đồ xuất ra đạt độ phân giải $\ge 300\text{ DPI}$.
