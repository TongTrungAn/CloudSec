---
name: cryptographic-benchmarking
description: >-
  Use this skill when measuring cryptographic performance, including encryption/decryption
  throughput (MB/s), latency (microseconds/milliseconds), CPU utilization, memory RSS footprint,
  and calculating statistical confidence intervals for research publications.
---

# Cryptographic Benchmarking & Performance Profiling

Kỹ năng này cung cấp phương pháp đo lường hiệu năng mật mã đạt chuẩn học thuật dành cho `@sec-evaluator` và `@crypto-sec`.

## 1. Phương pháp đo lường khoa học

Để kết quả có ý nghĩa thống kê xuất bản trên kỷ yếu IEEE/Scopus hoặc bảo vệ luận văn:
1. **Warm-up phase**: Chạy 5-10 lượt khởi động trước khi bắt đầu ghi nhận dữ liệu để đưa CPU cache và Python JIT/bytecode vào trạng thái ổn định.
2. **Số vòng lặp ($N \ge 30$)**: Số lượt thử tối thiểu $30$ để áp dụng định lý giới hạn trung tâm (Central Limit Theorem).
3. **Đồng hồ đo độ phân giải cao**: Sử dụng `time.perf_counter_ns()` thay vì `time.time()`.

## 2. Code đo lường Throughput & Latency

```python
import time
import os
import psutil
import numpy as np
import pandas as pd

def benchmark_crypto_operation(cipher_func, payload_bytes: bytes, iterations: int = 30):
    """
    Đo đạc Throughput (MB/s), Latency (us), và CPU/RAM footprint.
    """
    size_mb = len(payload_bytes) / (1024 * 1024)
    latencies_us = []
    
    # 1. Warm-up
    for _ in range(5):
        cipher_func(payload_bytes)
        
    process = psutil.Process(os.getpid())
    cpu_before = process.cpu_percent(interval=None)
    mem_before = process.memory_info().rss / (1024 * 1024) # MB
    
    # 2. Main Measurement Loop
    start_total = time.perf_counter()
    for _ in range(iterations):
        t0 = time.perf_counter_ns()
        _ = cipher_func(payload_bytes)
        t1 = time.perf_counter_ns()
        latencies_us.append((t1 - t0) / 1000.0)
    end_total = time.perf_counter()
    
    total_time_sec = end_total - start_total
    total_data_mb = size_mb * iterations
    throughput_mb_s = total_data_mb / total_time_sec
    
    cpu_after = process.cpu_percent(interval=None)
    mem_after = process.memory_info().rss / (1024 * 1024)
    
    latencies = np.array(latencies_us)
    return {
        "payload_size_mb": size_mb,
        "iterations": iterations,
        "throughput_mb_s": round(throughput_mb_s, 2),
        "latency_mean_us": round(float(np.mean(latencies)), 2),
        "latency_std_us": round(float(np.std(latencies)), 2),
        "latency_p50_us": round(float(np.percentile(latencies, 50)), 2),
        "latency_p95_us": round(float(np.percentile(latencies, 95)), 2),
        "latency_p99_us": round(float(np.percentile(latencies, 99)), 2),
        "mem_delta_mb": round(mem_after - mem_before, 2),
    }
```

## 3. Tính toán Overhead mã hóa (%)

Công thức suy giảm thông lượng (Throughput Degradation) so với bản rõ (Baseline Plaintext):

$$\text{Overhead}_{\text{Throughput}} (\%) = \frac{\text{Throughput}_{\text{Plaintext}} - \text{Throughput}_{\text{Encrypted}}}{\text{Throughput}_{\text{Plaintext}}} \times 100\%$$

Thời gian trễ bổ sung (Latency Overhead):

$$\Delta \text{Latency} = \text{Latency}_{\text{Encrypted}} - \text{Latency}_{\text{Plaintext}}$$

## 4. Xuất dữ liệu sang CSV
Tất cả kết quả phải được xuất ra `reports/benchmark_crypto_raw.csv` và `reports/benchmark_summary.md`.
