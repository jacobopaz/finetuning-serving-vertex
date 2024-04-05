import os
import logging

from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    GPTQConfig,
    BitsAndBytesConfig
)

from trl import SFTTrainer
from peft import prepare_model_for_kbit_training, get_peft_model, LoraConfig
from datasets import load_dataset
from trainer.params_and_configs import Zephyr7BgptqFineTuningConfig
from trainer.utils import DATASET_ID, save_model


cfg = Zephyr7BgptqFineTuningConfig

def train_model(train_dataset, val_dataset):
    """
    Trains the model on a specified training dataset and validates it on a validation dataset.

    It uses GPTQ and LoRA configurations for model 
    quantization and parameter-efficient fine-tuning.

    Args:
    train_dataset: The dataset to be used for training.
    val_dataset: The dataset to be used for validation.

    Returns:
    SFTTrainer: A trained model wrapped in a SFTTrainer instance.
    """

    tokenizer = AutoTokenizer.from_pretrained(cfg.MODEL_ID)
    tokenizer.pad_token = tokenizer.unk_token
    tokenizer.padding_side = 'right'

    gptq_config =  GPTQConfig(bits=cfg.BITS,
                        disable_exllama=cfg.DISABLE_EXLLAMA,
                        tokenizer=tokenizer
                                )
    
    lora_config = LoraConfig(
                        r=cfg.LORA_R,
                        lora_alpha=cfg.LORA_ALPHA,
                        lora_dropout=cfg.LORA_DROPOUT,
                        bias=cfg.BIAS,
                        task_type=cfg.TASK_TYPE,
                        target_modules=cfg.TARGET_MODULES
                    )
    training_arguments = TrainingArguments(
                        output_dir=os.path.join("/tmp", cfg.MODEL_ID),
                        evaluation_strategy=cfg.EVALUATION_STRATEGY,
                        eval_steps=cfg.EVAL_STEPS,
                        eval_accumulation_steps=cfg.EVAL_ACCUMULATION_STEPS,
                        do_eval=cfg.DO_EVAL,
                        prediction_loss_only=cfg.LOSS_ONLY,
                        per_device_train_batch_size=cfg.BATCH_SIZE,
                        per_device_eval_batch_size=cfg.BATCH_SIZE,
                        gradient_accumulation_steps=cfg.GRAD_ACCUMULATION_STEPS,
                        optim=cfg.OPTIMIZER,
                        learning_rate=cfg.LR,
                        lr_scheduler_type=cfg.LR_SCHEDULER,
                        save_strategy=cfg.SAVE_STRATEGY,
                        logging_steps=cfg.LOGGING_STEPS,
                        num_train_epochs=cfg.NUM_TRAIN_EPOCHS,
                        fp16=cfg.FP16,
                        push_to_hub=cfg.PUSH_TO_HUB
                    )

    model = AutoModelForCausalLM.from_pretrained(
                                            cfg.MODEL_ID,
                                            quantization_config=gptq_config,
                                            device_map="cuda",
                                            use_cache=cfg.USE_CACHE,
                                        )
    
    logging.info("Model loaded succesfully!")

    model.gradient_checkpointing_enable()
    model = prepare_model_for_kbit_training(model)
    model = get_peft_model(model, lora_config)

    logging.info("Starting fine-tuning...")

    trainer = SFTTrainer(
                    model=model,
                    train_dataset=train_dataset,
                    eval_dataset=val_dataset if training_arguments.do_eval else None,
                    peft_config=lora_config,
                    dataset_text_field=cfg.DATASET_TEXT_FIELD,
                    args=training_arguments,
                    tokenizer=tokenizer,
                    packing=cfg.PACKING,
                    max_seq_length=cfg.MAX_SEQ_LENGTH
                )

    trainer.train()

    return trainer



def run(args):
    """
    Main entry point for running the model training pipeline. 
    Loads the training and validation datasets, 
    initiates the model training process, 
    and saves the trained model and the training state.

    Args:
    args: Command line arguments or parameters 
        specifying model configuration and save paths.

    The function does not return anything.
    """

    train_dataset = load_dataset(DATASET_ID, split="train")  
    val_dataset = load_dataset(DATASET_ID, split="val") 
    val_dataset = val_dataset.select(range(cfg.MAX_EVAL_SAMPLES)) if cfg.MAX_EVAL_SAMPLES else val_dataset
    trainer = train_model(train_dataset, val_dataset)
    trainer.model.save_pretrained(os.path.join("/tmp", args.model_name))
    trainer.tokenizer.save_pretrained(os.path.join("/tmp", args.model_name))
    trainer.state.save_to_json(os.path.join("/tmp", args.model_name, "state.json"))
    save_model(args)