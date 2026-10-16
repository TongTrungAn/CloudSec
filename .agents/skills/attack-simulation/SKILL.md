---
name: attack-simulation
description: >-
  Use this skill when simulating penetration testing scenarios, including S3 credential
  brute-forcing, HTTP DDoS request flooding via Locust or multi-threading, unauthorized
  data tampering on object storage, and generating red-team logs for IDS evaluation.
---

# Attack Simulation & Penetration Testing Guide

Kỹ năng này hướng dẫn `@sec-evaluator` thực hiện các kịch bản tấn công giả lập có kiểm soát trong môi trường Lab cục bộ.

## 1. Kịch bản 1: Giả mạo dữ liệu lưu trữ (Data Tampering Attack)

Mục tiêu: Đánh giá khả năng của thuật toán AEAD (AES-256-GCM / Poly1305) trong việc phát hiện can thiệp dữ liệu trái phép ở tầng lưu trữ.

```python
import random

def tamper_encrypted_payload(ciphertext_bytes: bytes, tamper_bytes_count: int = 1) -> bytes:
    """Đảo ngẫu nhiên một số bit/byte trong ciphertext trước khi giải mã."""
    payload_array = bytearray(ciphertext_bytes)
    # Chọn vị trí ngẫu nhiên không trùng header magic
    start_pos = 16
    end_pos = len(payload_array) - 16 # Tránh đè trực tiếp tag nếu muốn test payload
    
    for _ in range(tamper_bytes_count):
        idx = random.randint(start_pos, end_pos)
        payload_array[idx] ^= 0xFF # Đảo bit byte
        
    return bytes(payload_array)
```

## 2. Kịch bản 2: Tấn công Brute-force & Dò quét Endpoint S3

Mục tiêu: Sinh chuỗi truy cập bất thường chứa mã lỗi `403 Forbidden` hoặc `401 Unauthorized` dồn dập trong khoảng thời gian ngắn để kiểm tra độ nhạy phát hiện của `@ai-ids`.

```python
import time
import requests

def simulate_bruteforce_s3(endpoint: str, attempts: int = 50, delay_sec: float = 0.05):
    """Gửi liên tiếp các request sai authentication header."""
    results = []
    for i in range(attempts):
        headers = {
            "Authorization": f"AWS4-HMAC-SHA256 Credential=fake_user_{i}/test/s3/aws4_request",
        }
        try:
            res = requests.get(f"{endpoint}/cloudsec-encrypted-vault/secret-doc-{i}.bin", headers=headers, timeout=2)
            results.append({"status_code": res.status_code, "timestamp": time.time()})
        except Exception as e:
            results.append({"error": str(e), "timestamp": time.time()})
        time.sleep(delay_sec)
    return results
```

## 3. Kịch bản 3: Tấn công Flood Tải (DDoS Request Flooding) qua Locust

File kịch bản `benchmarks/locust_flood.py`:

```python
from locust import HttpUser, task, between

class S3FloodUser(HttpUser):
    wait_time = between(0.01, 0.05) # Tần suất cực cao
    
    @task(3)
    def flood_unauthorized_get(self):
        self.client.get("/cloudsec-encrypted-vault/probe", headers={"User-Agent": "AttackBot/1.0"})
        
    @task(1)
    def flood_malformed_post(self):
        self.client.post("/cloudsec-encrypted-vault/upload", data=b"MALFORMED_GARBAGE_PAYLOAD")
```

Lệnh thực thi Locust không cần giao diện (Headless mode):
```powershell
locust -f benchmarks/locust_flood.py --headless -u 100 -r 20 --run-time 1m --host http://localhost:9000
```

## 4. Ghi nhận log & Đánh giá
- Sau khi chạy xong kịch bản, kích hoạt `@ai-ids` để kiểm tra:
  1. Mô hình có kích hoạt cảnh báo bất thường không?
  2. Thời gian từ lúc bắt đầu tấn công đến lúc cảnh báo (Detection Time) là bao nhiêu giây?
