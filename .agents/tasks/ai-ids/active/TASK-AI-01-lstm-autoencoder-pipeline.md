# TASK-AI-01: Xây dựng Pipeline tiền xử lý log và Mô hình PyTorch LSTM Autoencoder

- **Người phụ trách**: `@ai-ids`
- **Độ ưu tiên**: P0 (Trọng tâm ĐATN)
- **Trạng thái**: ACTIVE
- **Ngày tạo**: 2026-10-16

## Mục tiêu
Xây dựng pipeline tiền xử lý chuỗi thời gian từ log truy cập MinIO/mạng và huấn luyện mô hình PyTorch LSTM Autoencoder để phát hiện bất thường và tấn công không xác định.

## Các hạng mục công việc
1. [ ] Xây dựng `src/ai_ids/preprocess.py`:
   - Trích xuất đặc trưng log (status code, request interval, payload size, method).
   - Chia tập dữ liệu theo thứ tự thời gian: Train (70%), Val (15%), Test (15%).
   - Fit Scaler chỉ trên tập Train (chống rò rỉ dữ liệu).
2. [ ] Xây dựng `src/ai_ids/model.py`:
   - Kiến trúc LSTM Autoencoder với PyTorch (2 tầng LSTM Encoder, 2 tầng LSTM Decoder).
3. [ ] Xây dựng `src/ai_ids/train.py`:
   - Cố định random seed (42).
   - Huấn luyện với MSE Loss, Adam Optimizer.
   - Cơ chế Early Stopping dựa trên Validation Loss.
4. [ ] Xây dựng `src/ai_ids/evaluate.py`:
   - Xác định Dynamic Threshold ($\mu + 3\sigma$).
   - Tính toán Precision, Recall, F1-Score, FPR và vẽ Confusion Matrix.

## Tiêu chí hoàn thành (DoD)
- Không có rò rỉ dữ liệu (tuân thủ `ai-pipeline-rules.md`).
- F1-Score $\ge 0.94$, False Positive Rate $< 1.5\%$.
- Checkpoint được lưu tại `models/checkpoints/ids_lstm_autoencoder_best.pt`.
