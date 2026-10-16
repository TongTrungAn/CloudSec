# Quy trình Bàn giao & Hợp đồng Dữ liệu giữa các Agent (Handoff Rules)

> **Mục tiêu**: Đảm bảo sự phối hợp trơn tru, không chồng chéo, không phụ thuộc ngầm giữa 5 Agent chuyên trách trong quá trình xây dựng `CloudSec-Core`.

---

## 1. Sơ đồ Luồng Bàn giao (Handoff Flowchart)

```
[cloud-infra] ──────> Cung cấp Storage API S3 (MinIO) & Loki Stream ──────> [crypto-sec] & [ai-ids]
                                                                                   │
[crypto-sec] ───────> Bàn giao E2EE Client SDK & Test Vectors ─────────────> [sec-evaluator]
                                                                                   │
[ai-ids] ───────────> Bàn giao Model Checkpoints & Predictor API ──────────> [sec-evaluator]
                                                                                   │
[sec-evaluator] ────> Báo cáo Benchmark, Bảng thống kê CSV & Lỗ hổng ──────> [research-lead]
                                                                                   │
[research-lead] ────> Đề cương, Nhiệm vụ phân rã & Soạn thảo Luận văn ─────> [thesis-drafting]
```

---

## 2. Chi tiết Hợp đồng Bàn giao (Handoff Contracts)

### Handoff 1: `@cloud-infra` $\to$ `@crypto-sec` & `@ai-ids`
- **Sản phẩm bàn giao**:
  - Tệp `deploy/docker-compose.yml` đang hoạt động tốt.
  - Endpoint MinIO: `http://localhost:9000` kèm bucket khởi tạo: `cloudsec-encrypted-vault`.
  - Endpoint Loki: `http://localhost:3100` sẵn sàng nhận query log range.
- **Tiêu chí nghiệm thu (Definition of Done)**:
  - Script `scripts/infra/healthcheck.py` chạy trả về mã HTTP `200` cho cả 2 dịch vụ.
  - Task tương ứng trong `.agents/tasks/cloud-infra/active/` được chuyển sang `done/`.

---

### Handoff 2: `@crypto-sec` $\to$ `@sec-evaluator`
- **Sản phẩm bàn giao**:
  - Module `src/crypto/` hoàn chỉnh hỗ trợ AES-256-GCM và ChaCha20-Poly1305.
  - Client SDK: `CloudSecCryptoClient` với interface upload/download stream mã hóa MinIO.
  - Bộ tài liệu API và tệp test mẫu trong `tests/crypto/`.
- **Tiêu chí nghiệm thu**:
  - $100\%$ unit tests vượt qua (Known Answer Tests, Authenticity validation, Tamper detection).
  - Không có cảnh báo Nonce reuse.

---

### Handoff 3: `@ai-ids` $\to$ `@sec-evaluator`
- **Sản phẩm bàn giao**:
  - Model weights: `models/checkpoints/ids_lstm_autoencoder_best.pt`.
  - Bộ tiền xử lý: `models/checkpoints/preprocessor.pkl`.
  - Inference class: `IDSPredictor` nhận log batch và trả về xác suất bất thường + cờ cảnh báo.
  - Báo cáo huấn luyện: `models/checkpoints/training_manifest.json` ghi nhận F1-Score trên tập Test $> 95\%$.
- **Tiêu chí nghiệm thu**:
  - Độ trễ suy luận (Inference time) đo trên CPU $< 50\text{ms}$ mỗi batch 10 sự kiện.

---

### Handoff 4: `@sec-evaluator` $\to$ `@research-lead`
- **Sản phẩm bàn giao**:
  - File dữ liệu thực nghiệm thô: `reports/benchmark_crypto_raw.csv`.
  - Bảng thống kê tóm tắt: `reports/benchmark_summary.md` (Throughput, Latency P50/P99, CPU/RAM).
  - Biểu đồ khoa học độ phân giải cao: `reports/crypto_overhead.png` (300 DPI, IEEE palette).
  - Ma trận nhầm lẫn và đường cong ROC: `reports/ids_confusion_matrix.png`, `reports/ids_roc_curve.png`.
  - Báo cáo lỗ hổng (nếu có) trong `.agents/tasks/vulnerabilities/`.
- **Tiêu chí nghiệm thu**:
  - Mỗi phép đo thực hiện tối thiểu 30 lần lặp độc lập, có ghi nhận độ lệch chuẩn ($\pm \sigma$).

---

### Handoff 5: `@research-lead` $\to$ Bản thảo Luận văn & Paper
- **Sản phẩm bàn giao**:
  - Nội dung Chương 3 (Thiết kế hệ thống) và Chương 4 (Thực nghiệm & Đánh giá) trong `docs/thesis/`.
  - Bảng số liệu LaTeX tương thích chuẩn bài báo khoa học.
- **Tiêu chí nghiệm thu**:
  - Số liệu trong văn bản khớp $100\%$ với số liệu thô trong `reports/`.
