# Ánh xạ Danh tính Git Author theo Vai trò (Git User Mapping)

> **Mục tiêu**: Khi các Agent làm việc hoặc khi chạy tự động hóa, danh tính Git author được thiết lập tương ứng với vai trò của Agent đó để lịch sử git phản ánh trung thực quá trình phát triển đa tác nhân (Multi-Agent collaboration) và tránh xung đột khi rà soát commit.

---

## 1. Bảng Ánh xạ Danh tính (Author Identity Matrix)

| Vai trò / Agent | Git Name | Git Email | Phạm vi commit chính |
| :--- | :--- | :--- | :--- |
| **Research Lead** (`@research-lead`) | `CloudSec Research Lead` | `cloudsec-lead@lab.local` | `docs/thesis/`, `docs/architecture/`, `.agents/tasks/thesis-drafting/` |
| **Cloud & Infra** (`@cloud-infra`) | `CloudSec Infra Engineer` | `cloud-infra-dev@lab.local` | `deploy/`, `config/infra/`, `scripts/infra/`, `.agents/tasks/cloud-infra/` |
| **Crypto Engineer** (`@crypto-sec`) | `CloudSec Crypto Dev` | `crypto-dev@lab.local` | `src/crypto/`, `src/kms/`, `tests/crypto/`, `.agents/tasks/crypto-sec/` |
| **AI IDS Engineer** (`@ai-ids`) | `CloudSec AI Researcher` | `ai-researcher@lab.local` | `src/ai_ids/`, `models/`, `data/`, `tests/ai_ids/`, `.agents/tasks/ai-ids/` |
| **Security Evaluator** (`@sec-evaluator`) | `CloudSec Security Tester` | `sec-tester@lab.local` | `benchmarks/`, `scripts/attacks/`, `reports/`, `.agents/tasks/sec-evaluator/` |

---

## 2. Quy ước Thông điệp Commit (Conventional Commits for Lab)

Mọi commit phải tuân theo tiền tố định dạng:

- `feat(crypto): ...` (Phát triển module mật mã mới)
- `feat(ids): ...` (Thêm model kiến trúc hoặc pipeline tiền xử lý mới)
- `feat(infra): ...` (Cập nhật docker-compose hoặc log router)
- `test(bench): ...` (Thực thi chuỗi benchmark hiệu năng)
- `sec(pentest): ...` (Chạy kịch bản tấn công giả lập)
- `docs(thesis): ...` (Cập nhật bản thảo chương luận văn / paper)
- `fix(vuln): ...` (Vá lỗ hổng bảo mật hoặc false-positive)

---

## 3. Lệnh Git hỗ trợ chuyển đổi tác nhân nhanh (Quick Commands)

Khi Agent thực hiện commit, có thể cấu hình author tạm thời cho commit đó bằng cờ `--author`:

```bash
# Ví dụ commit của Crypto Dev:
git commit --author="CloudSec Crypto Dev <crypto-dev@lab.local>" -m "feat(crypto): implement chunked AES-256-GCM streaming for MinIO"

# Ví dụ commit của AI Researcher:
git commit --author="CloudSec AI Researcher <ai-researcher@lab.local>" -m "feat(ids): train PyTorch Bi-LSTM Autoencoder on S3 access logs"

# Ví dụ commit của Evaluator:
git commit --author="CloudSec Security Tester <sec-tester@lab.local>" -m "test(bench): execute 30-run throughput benchmark comparing plaintext vs AES-GCM"
```
