# Mẫu Ghi nhận Lỗ hổng Bảo mật & Sai số Mô hình (Vulnerability & Bug Report)

- **Mã báo cáo**: `VULN-YYYYMMDD-XXX`
- **Người phát hiện**: `@sec-evaluator` (hoặc Agent khác)
- **Đối tượng**: `src/crypto/` | `src/ai_ids/` | `deploy/` | `src/kms/`
- **Mức độ nghiêm trọng**: CRITICAL | HIGH | MEDIUM | LOW
- **Trạng thái**: OPEN | INVESTIGATING | RESOLVED

---

## 1. Mô tả chi tiết vấn đề
Mô tả hiện tượng, điều kiện kích hoạt và rủi ro an toàn thông tin (ví dụ: rò rỉ Nonce, bypass cảnh báo IDS, ngoại lệ giải mã không được bắt).

## 2. Các bước tái hiện (Steps to Reproduce)
1. Chạy lệnh: `python scripts/attacks/...`
2. Quan sát log hoặc exception...

## 3. Bằng chứng thực nghiệm (Proof of Concept)
```
[Dán log hoặc stack trace tại đây]
```

## 4. Đề xuất khắc phục
- `@crypto-sec` hoặc `@ai-ids` cần chỉnh sửa đoạn code nào...
- Tiêu chí xác minh sau khi vá:
