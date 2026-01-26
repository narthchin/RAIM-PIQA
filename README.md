# Professional IQA Challenge Baseline 🏆

This repository provides the official baseline for the **Professional IQA (Image Quality Assessment) Competition** hosted on [CodaBench](https://www.codabench.org/competitions/12789/).

It supports training large multimodal models (specifically **Qwen3-VL-Instruct**) using **GRPO (Group Relative Policy Optimization)** and **SFT (Supervised Fine-Tuning)** on custom datasets. The training pipeline is built upon the robust [ms-swift](https://www.google.com/search?q=https://github.com/modelscope/swift) framework.

## 🚀 Features

* **Competition Ready**: Pre-configured scripts for the Professional IQA challenge.
* **GRPO Support**: Optimized for Chain-of-Thought (CoT) reasoning with `<thinking>` and `<answer>` format.
* **Multi-Backend Download**: Scripts to fetch models from **ModelScope** (CN) or **HuggingFace** (Global).
* **Custom Data Pipeline**: Easily ingest comparison-based IQA datasets.

## 🛠️ Installation

This repository contains `ms-swift` as a submodule/directory.

1. **Clone and Install Dependencies**:

```bash
# Enter the ms-swift directory
cd ms-swift

# Install all requirements
chmod u+x ./requirements/install_all.sh
./requirements/install_all.sh

# Return to project root
cd ..

```

## 📥 Model Preparation

We use **Qwen3-VL-Instruct** as the base model. Please download the model checkpoints into the `models/` directory.

```bash
cd models
```

**Option 1: From ModelScope (Recommended for users in China)**

```bash
pip install modelscope
modelscope Qwen/Qwen3-VL-8B-Instruct --local-dir ./Qwen3-VL-8B-Instruct
```

**Option 2: From HuggingFace**

```bash
pip install huggingface_hub
hf download Qwen/Qwen3-VL-8B-Instruct --local-dir ./Qwen3-VL-8B-Instruct
```

## 📂 Data Preparation

### 1. Data Format

The dataset utilizes a specific JSONL format designed for GRPO training. It includes image pairs, a reasoning process, and a final conclusion.

**Example entry (`data/1536/train_grpo_1536.jsonl`):**

```json
{
  "images": [
    "data/1536/images/p_000_merged_c0.jpg",
    "data/1536/images/p_000_merged_c1.jpg"
  ],
  "messages": [
    {
      "role": "system",
      "content": "You are an expert in Image Quality Assessment (IQA). Compare the two images..."
    },
    {
      "role": "user",
      "content": "<image><image>\nPlease compare the following image pairs..."
    }
  ],
  "solution": "<thinking>\nClothing (White Shirt) Sharpness: Both images show similar levels...\nGlobal Overall: Image A (Left) has an advantage...\n</thinking>\n<answer>A</answer>"
}

```

### 2. Path Correction

Ensure that image paths in your JSONL file are relative to the repository root.
If your raw data uses `./images`, you must update it to `data/1536/images`.

```bash
# Example command to fix paths in your jsonl file
sed -i 's|\./images|data/1536/images|g' data/1536/train_grpo_1536.jsonl

```

## 🏃 Training

### Group Relative Policy Optimization (GRPO)

This is the recommended method for the competition to encourage the model to follow the `<thinking>` process before outputting the `<answer>`.

1. **Configure the script**: Ensure `scripts/grpo.sh` points to your model path and dataset.
2. **Run the training**:

```bash
bash scripts/grpo.sh

```

**Configuration Reference (`scripts/grpo.sh`):**

```bash
# Ensure your dataset path and model path are correct
dataset="data/1536/train_grpo_1536.jsonl"
model_path="models/Qwen3-vl-ins"

# MS-Swift command (simplified example)
swift rlhf \
    --rlhf_type grpo \
    --model_type $model_path \
    --dataset $dataset \
    ...

```

### Supervised Fine-Tuning (SFT)

If you prefer standard fine-tuning or want to pre-train before GRPO, you can use the `messages` list from the JSONL `data/1536/train_sft_1536.jsonl`.

## 🏆 CodaBench Submission

This repo serves as the starting point for the **Professional IQA** competition.
Participants are encouraged to:

1. Improve the base model using the provided training scripts.
2. Optimize the GRPO reward functions or data quality.
3. Submit your results to [CodaBench Competition #12789](https://www.codabench.org/competitions/12789/).

## 📜 License

This project follows the license of the underlying `ms-swift` framework and the competition rules.

---

### Need Help?

For issues related to the `ms-swift` framework, please visit the [official repository](https://www.google.com/search?q=https://github.com/modelscope/swift).
For competition inquiries, please check the CodaBench forum.
