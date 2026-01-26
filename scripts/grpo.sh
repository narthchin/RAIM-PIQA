MAX_PIXELS=5120000 \
NPROC_PER_NODE=4 \
CUDA_VISIBLE_DEVICES=0,1,2,3 \
swift rlhf \
    --beta 0.04 \
    --rlhf_type grpo \
    --model /path/to/your/Qwen3-VL-8B-Instruct \
    --model_type qwen3_vl \
    --reward_funcs base_acc format_acc \
    --reward_weights 1.0 0.5 \
    --train_type full \
    --torch_dtype bfloat16 \
    --dataset data/1536/train_grpo_1536.jsonl \
    --load_from_cache_file true \
    --external_plugins plugins/reward_funcs.py \
    --max_completion_length 512 \
    --num_train_epochs 10 \
    --per_device_train_batch_size 1 \
    --learning_rate 1e-6 \
    --gradient_accumulation_steps 2 \
    --split_dataset_ratio 0. \
    --save_steps 25 \
    --logging_steps 1 \
    --max_length 2048 \
    --output_dir output \
    --warmup_ratio 0.05 \
    --dataloader_num_workers 4 \
    --dataset_num_proc 4 \
    --num_generations 4 \
    --temperature 0.9 \
    --deepspeed zero3 \ # could set to zero3_offload if no enough GPU memory
    --log_completions true
