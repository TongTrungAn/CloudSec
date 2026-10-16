---
name: minio-storage-api
description: >-
  Use this skill when interacting with MinIO Object Storage via Python S3 SDK (boto3),
  configuring bucket policies, uploading or downloading encrypted streams in chunks,
  and handling S3 SSE headers or multipart uploads.
---

# MinIO S3 Storage API Guide

Kỹ năng này hướng dẫn các Agent (`@cloud-infra`, `@crypto-sec`, `@sec-evaluator`) thao tác chuẩn hóa với MinIO Object Storage thông qua thư viện `boto3`.

## 1. Khởi tạo S3 Client tương thích MinIO

```python
import os
import boto3
from botocore.client import Config

def get_minio_s3_client(
    endpoint_url: str = os.getenv("MINIO_ENDPOINT", "http://localhost:9000"),
    access_key: str = os.getenv("MINIO_ROOT_USER", "admin"),
    secret_key: str = os.getenv("MINIO_ROOT_PASSWORD", "cloudsec_password_2026"),
):
    """Khởi tạo boto3 S3 client tối ưu cho MinIO cục bộ."""
    return boto3.client(
        "s3",
        endpoint_url=endpoint_url,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        config=Config(
            signature_version="s3v4",
            s3={"addressing_style": "path"},
            retries={"max_attempts": 3, "mode": "standard"}
        ),
    )
```

## 2. Quản lý Bucket & Thiết lập Chính sách (Bucket Policy)

```python
def ensure_bucket_exists(s3_client, bucket_name: str = "cloudsec-encrypted-vault"):
    """Tạo bucket nếu chưa tồn tại và thiết lập private policy."""
    try:
        s3_client.head_bucket(Bucket=bucket_name)
    except Exception:
        s3_client.create_bucket(Bucket=bucket_name)
        # Thiết lập Private Policy: chỉ cho phép user xác thực
        s3_client.put_bucket_acl(Bucket=bucket_name, ACL="private")
```

## 3. Streaming Upload & Chunking cho Payload lớn

Khi mã hóa file dung lượng lớn (100MB - 1GB), không nạp toàn bộ vào RAM mà đẩy theo stream chunks:

```python
import io

def upload_encrypted_stream(s3_client, bucket_name: str, object_name: str, data_stream: io.BytesIO, metadata: dict = None):
    """Upload stream đã mã hóa lên MinIO với metadata chứa Key ID & Nonce."""
    extra_args = {}
    if metadata:
        extra_args["Metadata"] = metadata
    
    s3_client.upload_fileobj(
        Fileobj=data_stream,
        Bucket=bucket_name,
        Key=object_name,
        ExtraArgs=extra_args
    )

def download_encrypted_stream(s3_client, bucket_name: str, object_name: str, out_stream: io.BytesIO):
    """Download stream từ MinIO để giải mã theo pipeline."""
    s3_client.download_fileobj(
        Bucket=bucket_name,
        Key=object_name,
        Fileobj=out_stream
    )
```

## 4. Xử lý lỗi thường gặp
- **Endpoint Connection Error**: Kiểm tra container MinIO đã bật chưa qua `docker ps` hoặc port `9000`.
- **Invalid Access Key**: Đảm bảo file `.env` đã được load trước khi gọi `boto3`.
- **SignatureDoesNotMatch**: Đảm bảo `signature_version="s3v4"` và `addressing_style="path"`.
