"""
Script kiểm tra tính sẵn sàng (Healthcheck) của cụm dịch vụ MinIO và Loki.
Được sử dụng bởi @cloud-infra và trong các workflow tự động.
"""
import os
import sys
import requests

def check_service(name: str, url: str) -> bool:
    try:
        res = requests.get(url, timeout=3)
        if res.status_code in [200, 403]:  # MinIO root trả về 403 hoặc 200 khi alive
            print(f"[OK] {name} is alive at {url} (Status: {res.status_code})")
            return True
        else:
            print(f"[WARN] {name} responded with unexpected status: {res.status_code}")
            return False
    except Exception as e:
        print(f"[FAIL] {name} unreachable at {url}: {e}")
        return False

def main():
    minio_url = os.getenv("MINIO_ENDPOINT", "http://localhost:9000") + "/minio/health/live"
    loki_url = os.getenv("LOKI_ENDPOINT", "http://localhost:3100") + "/ready"
    
    print("=" * 50)
    print("CloudSec-Core Infrastructure Healthcheck")
    print("=" * 50)
    
    minio_ok = check_service("MinIO S3", minio_url)
    loki_ok = check_service("Loki Log", loki_url)
    
    if minio_ok and loki_ok:
        print("\nAll infrastructure services are HEALTHY and READY.")
        sys.exit(0)
    else:
        print("\nOne or more services are NOT READY. Please verify Docker containers.")
        sys.exit(1)

if __name__ == "__main__":
    main()
