---
name: deep-learning-ids
description: >-
  Use this skill when developing, training, evaluating, and fine-tuning Deep Learning
  models (LSTM, Bi-LSTM, Autoencoder) for intrusion detection and anomaly detection
  on cloud access logs and network time-series data.
---

# Deep Learning Intrusion Detection System (PyTorch)

Kỹ năng này hướng dẫn `@ai-ids` xây dựng mạng hồi quy và học không giám sát/bán giám sát để phát hiện hành vi xâm nhập, bất thường trên Cloud Storage MinIO.

## 1. Kiến trúc LSTM Autoencoder cho Anomaly Detection

Mô hình học biểu diễn hành vi truy cập hợp lệ (Normal behavior). Khi gặp chuỗi request tấn công (Brute-force, Flood, Tampering), sai số tái tạo (Reconstruction Error - MSE) sẽ tăng đột biến.

```python
import torch
import torch.nn as nn

class LSTMEncoder(nn.Module):
    def __init__(self, seq_len: int, num_features: int, embedding_dim: int = 64):
        super(LSTMEncoder, self).__init__()
        self.seq_len = seq_len
        self.num_features = num_features
        self.lstm = nn.LSTM(
            input_size=num_features,
            hidden_size=embedding_dim,
            num_layers=2,
            batch_first=True,
            dropout=0.2
        )

    def forward(self, x):
        _, (hidden, _) = self.lstm(x)
        return hidden[-1] # Lấy hidden state tầng cuối cùng

class LSTMDecoder(nn.Module):
    def __init__(self, seq_len: int, num_features: int, embedding_dim: int = 64):
        super(LSTMDecoder, self).__init__()
        self.seq_len = seq_len
        self.num_features = num_features
        self.lstm = nn.LSTM(
            input_size=embedding_dim,
            hidden_size=embedding_dim,
            num_layers=2,
            batch_first=True,
            dropout=0.2
        )
        self.output_layer = nn.Linear(embedding_dim, num_features)

    def forward(self, x):
        x = x.unsqueeze(1).repeat(1, self.seq_len, 1) # Lặp lại vector đặc trưng cho seq_len
        out, _ = self.lstm(x)
        return self.output_layer(out)

class LSTMAutoencoder(nn.Module):
    def __init__(self, seq_len: int, num_features: int, embedding_dim: int = 64):
        super(LSTMAutoencoder, self).__init__()
        self.encoder = LSTMEncoder(seq_len, num_features, embedding_dim)
        self.decoder = LSTMDecoder(seq_len, num_features, embedding_dim)

    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded
```

## 2. Xác định Ngưỡng Động (Adaptive Dynamic Threshold)

Sau khi huấn luyện trên tập Train (chỉ gồm dữ liệu bình thường):
1. Tính toán Reconstruction Loss (MSE) trên tập Validation:
   $$\mathcal{L}(x, \hat{x}) = \frac{1}{D} \sum_{i=1}^{D} (x_i - \hat{x}_i)^2$$
2. Thiết lập ngưỡng cảnh báo:
   $$\text{Threshold} = \mu_{\text{val}} + k \cdot \sigma_{\text{val}}$$
   *(thông thường $k=3$ tương ứng quy tắc $3\sigma$, hoặc lấy phân vị $99\%$ của tập Validation)*.
3. Khi triển khai: Nếu $\text{Loss}_{\text{realtime}} > \text{Threshold} \implies \text{Phát hiện Tấn công/Bất thường}$.

## 3. Quy trình tính toán chỉ số IEEE

```python
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix

def compute_ids_metrics(y_true, y_pred, y_scores):
    """Tính toán toàn bộ chỉ số đánh giá phục vụ viết báo cáo."""
    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = cm.ravel()
    
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0
    
    return {
        "Accuracy": round((tp + tn) / (tp + tn + fp + fn), 4),
        "Precision": round(precision_score(y_true, y_pred, zero_division=0), 4),
        "Recall": round(recall_score(y_true, y_pred, zero_division=0), 4),
        "F1_Score": round(f1_score(y_true, y_pred, zero_division=0), 4),
        "False_Positive_Rate": round(fpr, 4),
        "ROC_AUC": round(roc_auc_score(y_true, y_scores), 4),
        "Confusion_Matrix": {"TN": int(tn), "FP": int(fp), "FN": int(fn), "TP": int(tp)}
    }
```
