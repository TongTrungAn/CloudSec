# CloudSec-Core: Comprehensive Security Ecosystem for Private Cloud

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-red.svg)](https://pytorch.org/)
[![MinIO S3](https://img.shields.io/badge/Storage-MinIO%20S3-orange.svg)](https://min.io/)

> **Tên đề tài**: Hệ thống bảo mật toàn diện cho đám mây riêng: Tích hợp mã hóa dữ liệu đầu cuối và giám sát an ninh thông minh dựa trên học sâu  
> **Mã dự án**: `CloudSec-Core`  
> **Mục tiêu**: Đồ án tốt nghiệp Kỹ sư An toàn thông tin & Bài báo Nghiên cứu Khoa học (NCKH).

---

## 1. Tổng quan Kiến trúc Hệ thống

CloudSec-Core giải quyết bài toán an toàn dữ liệu trên nền tảng Private Cloud theo mô hình đa lớp (Defense-in-Depth):

1. **Tầng Lưu trữ & Mã hóa đầu cuối (Client-Side E2EE)**:
   - Dữ liệu được mã hóa ngay tại phía Client trước khi truyền tải và lưu trữ trên MinIO S3 bằng **AES-256-GCM** và **ChaCha20-Poly1305**.
   - Cơ chế Envelope Encryption (Master Key / Data Key) bảo vệ khóa dữ liệu độc lập.
   - Xác thực toàn vẹn dữ liệu (AEAD Authenticity Tag) ngăn chặn mọi hình thức Data Tampering trên Object Storage.
2. **Tầng Giám sát & Phát hiện xâm nhập thông minh (AI / Deep Learning IDS)**:
   - Thu thập chuỗi sự kiện truy cập thời gian thực qua Promtail & Loki.
   - Mô hình học sâu **PyTorch LSTM / Bi-LSTM Autoencoder** học phân phối hành vi bình thường và kích hoạt cảnh báo tức thời khi phát hiện tấn công (Brute-force, DDoS request flood, Unauthorized access) với ngưỡng sai số động ($\mu + 3\sigma$).
3. **Môi trường Multi-Agent System (.agents)**:
   - Tự động hóa quá trình R&D, kiểm thử mã hóa, giả lập tấn công, đo lường benchmark và đồng bộ số liệu vào báo cáo luận văn.

---

## 2. Cấu trúc Thư mục Dự án

```
CloudSecu/
├── .agents/                    # Hệ sinh thái Multi-Agent System Lab
│   ├── AGENTS.md               # Hiến chương và quy ước hoạt động của các Agent
│   ├── agents/                 # Hồ sơ 5 Agent chuyên trách (research-lead, crypto, ai, infra, evaluator)
│   ├── rules/                  # Quy chuẩn mật mã, AI, Docker hardening, git mapping
│   ├── skills/                 # Thư viện kỹ năng (MinIO, Benchmark, Deep Learning, Attacks, LaTeX)
│   ├── tasks/                  # Task board theo từng chuyên môn (active/done)
│   └── workflows/              # Kịch bản tự động hóa (/run-benchmark, /train-eval-ids, /thesis-sync)
├── src/                        # Mã nguồn chính
│   ├── crypto/                 # Module mã hóa AES-256-GCM, ChaCha20, Chunked Streaming
│   ├── kms/                    # Quản lý vòng đời khóa (Envelope Encryption, CSPRNG, KDF)
│   └── ai_ids/                 # Mô hình PyTorch LSTM Autoencoder, Pipeline trích xuất đặc trưng
├── deploy/                     # Docker Compose và hạ tầng MinIO, Loki, Promtail
├── config/infra/               # Cấu hình dịch vụ (MinIO policies, Loki config, Promtail config)
├── benchmarks/                 # Bộ đo đạc Throughput, Latency, Overhead, Locust scenarios
├── scripts/
│   ├── infra/                  # Healthcheck, khởi tạo bucket S3
│   └── attacks/                # Giả lập tấn công (Brute-force, Flood, Data Tampering)
├── docs/thesis/                # Bản thảo 5 chương Đồ án tốt nghiệp & Bài báo IEEE
├── reports/                    # Biểu đồ khoa học (300 DPI), bảng LaTeX, CSV dữ liệu thô
├── data/                       # Dữ liệu log huấn luyện và kiểm thử
├── models/checkpoints/         # Trọng số mô hình đã huấn luyện (.pt, .pkl)
├── tests/                      # Unit tests mật mã và AI pipeline
├── requirements.txt            # Thư viện phụ thuộc
└── .env.example                # Cấu hình biến môi trường mẫu
```

---

## 3. Các Lệnh Tự động hóa Nhanh (Workflows)

| Lệnh | File quy trình | Mô tả |
| :--- | :--- | :--- |
| `/run-benchmark` | `.agents/workflows/run-benchmark.md` | Chạy 30 vòng lặp đo Throughput & Latency Plaintext vs AES-GCM trên MinIO $\to$ Xuất biểu đồ `reports/crypto_overhead.png`. |
| `/train-eval-ids` | `.agents/workflows/train-eval-ids.md` | Tiền xử lý log, huấn luyện PyTorch LSTM Autoencoder $\to$ Xuất báo cáo F1-Score & Ma trận nhầm lẫn IEEE. |
| `/thesis-sync` | `.agents/workflows/thesis-sync.md` | Tự động quét số liệu mới nhất trong `reports/` $\to$ Cập nhật vào bản thảo `docs/thesis/chapter4_results.md`. |

---

## 4. Hướng dẫn Khởi động Nhanh

### 4.1. Cài đặt Môi trường Python
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 4.2. Khởi chạy Cụm Hạ tầng Private Cloud (Docker)
```powershell
docker-compose -f deploy/docker-compose.yml up -d
python scripts/infra/healthcheck.py
```
