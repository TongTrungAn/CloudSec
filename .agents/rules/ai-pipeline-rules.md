# Tiêu chuẩn Xây dựng Pipeline AI & Thực nghiệm NCKH (AI Pipeline Rules)

> **Phạm vi áp dụng**: Mọi quy trình tiền xử lý dữ liệu, huấn luyện mô hình học sâu, đánh giá và xuất báo cáo metrics trong module IDS của `CloudSec-Core`.  
> **Người thực hiện chính**: `@ai-ids` | **Người kiểm toán**: `@research-lead`, `@sec-evaluator`.

---

## 1. Nguyên tắc cốt lõi: Chống Rò rỉ Dữ liệu (Strict Zero Data Leakage)

1. **Thứ tự phân chia tập dữ liệu (Dataset Splitting Order)**:
   - **TẬP DỮ LIỆU PHẢI ĐƯỢC CHIA TRƯỚC TIÊN**: Chia thành `Train` ($70\%$), `Validation` ($15\%$), `Test` ($15\%$) **TRƯỚC KHI** thực hiện bất kỳ phép chuẩn hóa (Scaling), mã hóa (Encoding) hay gán nhãn nào.
   - Đối với dữ liệu chuỗi thời gian (Log sequence / Network timeseries), **CẤM** dùng Random K-Fold Cross Validation. Bắt buộc dùng **Temporal Split** (Phân chia theo thứ tự thời gian tuyến tính) để tránh việc mô hình "học trước tương lai" (Look-ahead bias).
2. **Quy tắc Fit/Transform**:
   - `scaler.fit()`, `encoder.fit()` **CHỈ ĐƯỢC PHÉP CHẠY TRÊN TẬP TRAIN**.
   - Tập `Validation` và `Test` chỉ được phép dùng `scaler.transform()` và `encoder.transform()`.
   - Lưu trữ artifacts tiền xử lý (`preprocessor.pkl` hoặc `scaler_params.json`) kèm theo checkpoint của model.

---

## 2. Tính Tái Lập Khoa Học (Scientific Reproducibility)

1. **Cố định Random Seed**:
   - Đầu mọi file thực nghiệm và huấn luyện (`train.py`, `eval.py`), bắt buộc gọi hàm cố định seed:
     ```python
     def seed_everything(seed: int = 42):
         import random, os, numpy as np, torch
         random.seed(seed)
         os.environ['PYTHONHASHSEED'] = str(seed)
         np.random.seed(seed)
         torch.manual_seed(seed)
         torch.cuda.manual_seed_all(seed)
         torch.backends.cudnn.deterministic = True
         torch.backends.cudnn.benchmark = False
     ```
2. **Lưu trữ Siêu tham số & Môi trường**:
   - Mỗi lần chạy huấn luyện phải tự động sinh tệp `run_manifest_<timestamp>.json` chứa:
     - Tên mô hình, kiến trúc layer, số chiều hidden state.
     - Learning rate, Batch size, Optimizer, Loss function, Epochs.
     - Phiên bản PyTorch, CUDA (nếu có), CPU/GPU model.

---

## 3. Chuẩn mực Đánh giá Mô hình theo Chuẩn Học thuật (IEEE Standards)

1. **Các chỉ số bắt buộc đo lường**:
   - **Accuracy**: Chỉ dùng để tham khảo, **CẤM** dùng làm thước đo chính khi dữ liệu bị mất cân bằng (Imbalanced dataset).
   - **Precision**: $\frac{TP}{TP + FP}$ (Độ chính xác của cảnh báo, tránh báo động giả gây mệt mỏi cho SOC analyst).
   - **Recall (Sensitivity / Detection Rate)**: $\frac{TP}{TP + FN}$ (Tỷ lệ bắt trúng cuộc tấn công, tối quan trọng trong an toàn thông tin).
   - **F1-Score / Macro F1**: $2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}$ (Thước đo tổng hòa chính).
   - **False Positive Rate (FPR)**: $\frac{FP}{FP + TN}$ (Phải $< 1\%$ trong các hệ thống thực tế).
   - **ROC-AUC**: Diện tích dưới đường cong ROC đánh giá khả năng phân tách của ngưỡng.
2. **Ma trận nhầm lẫn (Confusion Matrix)**:
   - Bắt buộc chuẩn hóa cả dạng số đếm tuyệt đối (Counts) và tỷ lệ phần trăm (Normalized by True Class) theo chuẩn đồ họa IEEE:
     - Trục tung: True Label (Thực tế).
     - Trục hoành: Predicted Label (Dự đoán).
3. **Đo lường độ trễ suy luận (Inference Latency)**:
   - Bắt buộc đo thời gian xử lý trung bình cho 1 log event / 1 sequence (đơn vị mili-giây: $\text{ms}$).
   - Đo phân vị P50, P95, P99 trên tập Test để chứng minh khả năng bảo vệ thời gian thực (Real-time IDS).
