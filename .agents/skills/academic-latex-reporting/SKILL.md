---
name: academic-latex-reporting
description: >-
  Use this skill when converting raw experimental CSV data and benchmark metrics
  into IEEE-compliant LaTeX tables, generating high-resolution publication charts
  using matplotlib/seaborn, and preparing figures for thesis chapters or research papers.
---

# Academic LaTeX Reporting & Data Visualization (IEEE Format)

Kỹ năng này hướng dẫn `@research-lead` và `@sec-evaluator` chuẩn hóa toàn bộ kết quả thực nghiệm thành định dạng sẵn sàng chèn vào bản thảo luận văn hoặc bài báo khoa học.

## 1. Xuất bảng dữ liệu sang LaTeX (IEEE Trans Style)

Bảng học thuật cần tuân thủ quy tắc:
- Sử dụng gói `booktabs` (`\toprule`, `\midrule`, `\bottomrule`).
- Không dùng đường kẻ dọc (`|`).
- Căn lề số theo dấu phẩy hoặc căn phải.

```python
import pandas as pd

def export_to_ieee_latex_table(df: pd.DataFrame, caption: str, label: str) -> str:
    """Chuyển DataFrame thành bảng LaTeX chuẩn IEEE."""
    latex_code = [
        "\\begin{table}[htbp]",
        "\\centering",
        f"\\caption{{{caption}}}",
        f"\\label{{{label}}}",
        "\\begin{tabular}{l" + "r" * (len(df.columns) - 1) + "}",
        "\\toprule",
        " & ".join(f"\\textbf{{{col}}}" for col in df.columns) + " \\\\",
        "\\midrule",
    ]
    
    for _, row in df.iterrows():
        formatted_row = [str(val) for val in row.values]
        latex_code.append(" & ".join(formatted_row) + " \\\\")
        
    latex_code.extend([
        "\\bottomrule",
        "\\end{tabular}",
        "\\end{table}"
    ])
    return "\n".join(latex_code)
```

## 2. Vẽ biểu đồ chất lượng cao (300 DPI, Vector PDF / PNG)

Quy chuẩn đồ họa IEEE:
- Font chữ: Serif hoặc Times New Roman / DejaVu Serif đồng bộ với văn bản LaTeX.
- Bảng màu: Chuẩn Colorblind-safe (ví dụ palette `deep` hoặc `colorblind` của Seaborn).
- Độ phân giải: 300 DPI cho PNG, hoặc xuất trực tiếp định dạng Vector `.pdf`.

```python
import matplotlib.pyplot as plt
import seaborn as sns

def plot_crypto_throughput_comparison(df_results, output_path: str = "reports/crypto_overhead.png"):
    """Vẽ biểu đồ cột kép so sánh Throughput: Plaintext vs AES-256-GCM vs ChaCha20."""
    plt.figure(figsize=(7, 4.5), dpi=300)
    sns.set_theme(style="whitegrid", font="DejaVu Serif")
    
    ax = sns.barplot(
        data=df_results,
        x="Payload_Size",
        y="Throughput_MB_s",
        hue="Algorithm",
        palette=["#2b5c8f", "#d95f02", "#7570b3"]
    )
    
    plt.title("Comparison of S3 Read/Write Throughput under End-to-End Encryption", fontsize=12, pad=10, weight='bold')
    plt.xlabel("File Payload Size", fontsize=10, labelpad=8)
    plt.ylabel("Throughput (MB/s)", fontsize=10, labelpad=8)
    plt.legend(title="Security Mode", frameon=True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
```

## 3. Vẽ ma trận nhầm lẫn (Confusion Matrix)

```python
def plot_ids_confusion_matrix(cm, labels, output_path: str = "reports/ids_confusion_matrix.png"):
    """Vẽ ma trận nhầm lẫn tỷ lệ chuẩn hóa cho mô hình IDS."""
    plt.figure(figsize=(6, 5), dpi=300)
    sns.set_theme(style="white", font="DejaVu Serif")
    
    cm_norm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    sns.heatmap(cm_norm, annot=True, fmt=".2%", cmap="Blues", xticklabels=labels, yticklabels=labels, cbar=False)
    
    plt.title("Normalized Confusion Matrix - Deep Learning IDS", fontsize=12, weight='bold')
    plt.ylabel("True Attack Class", fontsize=10)
    plt.xlabel("Predicted Class", fontsize=10)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
```
