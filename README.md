# HỆ THỐNG PHÁT HIỆN XÂM NHẬP (IDS) 2 GIAI ĐOẠN CHO MICROSERVICES SỬ DỤNG DEEP LEARNING

> **Đồ án 3:** Nghiên cứu, thiết kế và xây dựng giải pháp giám sát an ninh mạng, phát hiện xâm nhập/bất thường thời gian thực cho hạ tầng Microservices cục bộ sử dụng mô hình Deep Learning lai 2 giai đoạn.  
> **Tên đề tài tiếng Anh:** *A Two-Stage Intelligent Intrusion Detection System for Microservices: Combining Unsupervised Anomaly Detection and Supervised Hybrid Deep Learning for Automated Threat Classification*.

---

## 1. TỔNG QUAN VỀ KIẾN TRÚC TOÀN BỘ HỆ THỐNG (SYSTEM ARCHITECTURE)

Hệ thống được thiết kế theo mô hình **Pipeline 4 tầng (4-Tier Closed-Loop Architecture)** hoạt động khép kín và tự động hóa:


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

2. CHI TIẾT TỪNG TẦNG CÔNG NGHỆ (TECH STACK)

Tầng 1: Nguồn dữ liệu (Microservices Tier)

  - Công nghệ: Docker, Docker Compose, Node.js (Express framework).
  - Cơ chế sinh log: Sử dụng chuẩn Docker logging driver dạng json-file. Mọi
    hành động từ người dùng (truy cập hợp lệ, lỗi đăng nhập 401, lỗi máy
    chủ 500) đều được format thành chuỗi JSON và bắn vào stdout/stderr.

Tầng 2: Thu thập log (Collector Agent Tier)

  - Công nghệ: Grafana Promtail.
  - Cơ chế: Kết nối trực tiếp vào docker.sock của hệ điều hành host, lắng nghe
    sự kiện từ các container đang chạy. Khi có log mới, Promtail bóc tách chuỗi,
    tự động gán nhãn (container="web-api-service", stream="stdout") và đẩy qua
    HTTP tới Loki.

Tầng 3: Lưu trữ tập trung (Centralized Storage Tier)

  - Công nghệ: Grafana Loki.
  - Cơ chế: Khác với Elasticsearch tiêu tốn nhiều RAM, Loki chỉ lập chỉ mục
    (index) các metadata/labels thay vì toàn bộ nội dung text, giúp hệ thống
    chạy mượt trên hạ tầng máy chủ cục bộ hoặc laptop cá nhân. Dữ liệu log được
    nén thành các chunk và sẵn sàng cho truy vấn thông qua giao thức HTTP REST
    API.

Tầng 4: Bộ máy AI 2 giai đoạn (Điểm nhấn học thuật của đề tài)

  - Giai đoạn 1 (Lọc bất thường không giám sát):
      - Mô hình: LSTM Autoencoder.
      - Mục tiêu: Được huấn luyện thuần túy trên log hệ thống chạy bình thường.
        Khi gặp các chuỗi log bất thường (tấn công đột ngột, lưu lượng dị biến),
        mô hình không thể tái tạo lại chuỗi này một cách chính xác \rightarrow
        Sai số tái tạo (Reconstruction Error) tăng vọt vượt ngưỡng cho phép
        \rightarrow Đánh dấu Anomaly.
  - Giai đoạn 2 (Phân loại mối đe dọa chuyên sâu):
      - Mô hình: Hybrid 1D-CNN + Bi-LSTM with Attention Layer.
      - Mục tiêu: Chỉ được kích hoạt khi Giai đoạn 1 báo cờ đỏ. Lớp 1D-CNN nhanh
        chóng trích xuất các đặc trưng từ vựng cục bộ độc hại; Bi-LSTM nắm bắt
        ngữ cảnh chuỗi trước/sau; và Attention layer tập trung vào các từ khóa
        trọng yếu (như IP, URL, User-Agent lạ, Status Code) để định danh chính
        xác loại tấn công:
          - Brute-Force Attack
          - DoS / DDoS Attack (Traffic flooding)
          - Unknown Anomaly / Zero-day
      - Kết quả đầu ra: Kích hoạt thông báo cảnh báo và lưu vết điều tra thời
        gian thực.

3. CẤU TRÚC THƯ MỤC DỰ ÁN (PROJECT DIRECTORY)

ids-microservices/
├── README.md                 # Tài liệu hướng dẫn kiến trúc & vận hành
├── docker-compose.yml        # Điều phối toàn bộ dịch vụ (Web, Loki, Promtail)
├── promtail-config.yaml      # Cấu hình Scrape Job cho Promtail Agent
├── backend_app/              # Mã nguồn dịch vụ Microservice mẫu
│   ├── Dockerfile            # Đóng gói Node.js App container
│   ├── package.json          # Quản lý dependencies
│   └── server.js             # API web & cơ chế xuất Structured Logging
└── ai_pipeline/              # Động cơ AI phân tích log (Triển khai giai đoạn tiếp theo)
    ├── model_stage1_ae.py    # Autoencoder phục vụ Anomaly Detection
    ├── model_stage2_clf.py   # Hybrid CNN-LSTM phục vụ Threat Classification
    └── stream_detector.py    # Script lắng nghe Loki API và kích hoạt 2 model

4. HƯỚNG DẪN KHỞI CHẠY HẠ TẦNG (QUICK START)

Yêu cầu môi trường

  - Hệ điều hành: Ubuntu 20.04/22.04 LTS (hoặc Ubuntu chạy trên WSL2 / Cloud
    Server).
  - Đã cài đặt: Docker Engine & Docker Compose Plugin.

Các lệnh vận hành nhanh (Thực thi tại Terminal VS Code)

1.  Khởi chạy toàn bộ hệ thống nền tảng:

    docker compose up -d --build

2.  Kiểm tra trạng thái container:

    docker compose ps

    (Đảm bảo cả 3 dịch vụ web-api-service, loki-server, promtail-agent đều đang
    ở trạng thái running).

3.  Sinh dữ liệu log mẫu:

      - Log bình thường (HTTP 200):
        curl http://localhost:3000/
      - Log lỗi đăng nhập / Giả lập Brute-force (HTTP 401):
        curl -X POST http://localhost:3000/api/login \
             -H "Content-Type: application/json" \
             -d '{"username":"attacker","password":"password123"}'

4.  Kiểm tra luồng log trên Loki:

    curl -G -s "http://localhost:3100/loki/api/v1/query_range" \
      --data-urlencode 'query={container="web-api-service"}'

5.  Dừng hệ thống khi không sử dụng:

    docker compose down

