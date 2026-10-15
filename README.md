# HỆ THỐNG PHÁT HIỆN XÂM NHẬP (IDS) 2 GIAI ĐOẠN CHO MICROSERVICES SỬ DỤNG DEEP LEARNING

> **Đồ án 3:** Nghiên cứu, thiết kế và xây dựng giải pháp giám sát an ninh mạng, phát hiện xâm nhập/bất thường thời gian thực cho hạ tầng Microservices cục bộ sử dụng mô hình Deep Learning lai 2 giai đoạn.  
> **Tên đề tài tiếng Anh:** *A Two-Stage Intelligent Intrusion Detection System for Microservices: Combining Unsupervised Anomaly Detection and Supervised Hybrid Deep Learning for Automated Threat Classification*.

---

## 1. TỔNG QUAN VỀ KIẾN TRÚC TOÀN BỘ HỆ THỐNG (SYSTEM ARCHITECTURE)

Hệ thống được thiết kế theo mô hình **Pipeline 4 tầng (4-Tier Closed-Loop Architecture)** hoạt động khép kín và tự động hóa:

```text
+-----------------------------------------------------------------------------+
| TẦNG 1: ỨNG DỤNG NGUỒN (CONTAINERIZED MICROSERVICES TIER)                   |
|  - Web API Service (Node.js/Express)                                        |
|  - Log Driver: Docker stdout/stderr (JSON format)                           |
+-----------------------------------------------------------------------------+
                                      │
                                      ▼ (Mount /var/run/docker.sock)
+-----------------------------------------------------------------------------+
| TẦNG 2: THU THẬP VÀ VẬN CHUYỂN DỮ LIỆU (DATA COLLECTION TIER)                |
|  - Promtail Agent (Docker Service Discovery)                                |
|  - Tự động bắt dòng log, gán nhãn container metadata                        |
+-----------------------------------------------------------------------------+
                                      │
                                      ▼ (HTTP Push: Cổng 3100)
+-----------------------------------------------------------------------------+
| TẦNG 3: LƯU TRỮ VÀ QUẢN TRỊ TẬP TRUNG (STORAGE & OBSERVABILITY TIER)         |
|  - Grafana Loki: Lưu trữ log dạng nén, đánh chỉ mục theo nhãn               |
|  - Mở LogQL Engine & HTTP API cho các dịch vụ bên ngoài truy vấn             |
+-----------------------------------------------------------------------------+
                                      │
                                      ▼ (Fetch Stream Log / LogQL API)
+-----------------------------------------------------------------------------+
| TẦNG 4: ĐỘNG CƠ TRÍ TUỆ NHÂN TẠO 2 GIAI ĐOẠN (AI/DL INTRUSION ENGINE TIER)   |
|                                                                             |
|  [Giai đoạn 1: Unsupervised Anomaly Detection]                              |
|   - Mô hình: LSTM Autoencoder                                               |
|   - Nhiệm vụ: Lọc hành vi bình thường, tính Reconstruction Error            |
|       ├─ Error < Threshold  ──> Ghi nhận Normal                             |
|       └─ Error >= Threshold ──> Kích hoạt Giai đoạn 2                       |
|                                     │                                       |
|                                     ▼                                       |
|  [Giai đoạn 2: Supervised Threat Classification & Alerting]                 |
|   - Mô hình: Hybrid CNN-BiLSTM with Attention Mechanism                     |
|   - Nhiệm vụ: Phân loại tấn công (DDoS, Brute-force, Injection...)           |
|   - Xuất cảnh báo (Alert) & Ghi vết điều tra (Investigation Log)            |
+-----------------------------------------------------------------------------+
