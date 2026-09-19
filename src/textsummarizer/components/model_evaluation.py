import os

import torch
import pandas as pd
import evaluate

from tqdm import tqdm
from datasets import load_from_disk
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from textsummarizer.entity import ModelEvaluationConfig
from textsummarizer.logging import logger


class ModelEvaluation:

    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    def generate_batch_sized_chunks(self, list_of_elements, batch_size):
        """
        Split the data into smaller batches.
        """

        for i in range(0, len(list_of_elements), batch_size):
            yield list_of_elements[i: i + batch_size]

    def calculate_metric_on_test_ds(
        self,
        dataset,
        metric,
        model,
        tokenizer,
        batch_size=1,
        device="cuda" if torch.cuda.is_available() else "cpu",
        column_text="dialogue",
        column_summary="summary"
    ):

        article_batches = list(
            self.generate_batch_sized_chunks(
                dataset[column_text],
                batch_size
            )
        )

        target_batches = list(
            self.generate_batch_sized_chunks(
                dataset[column_summary],
                batch_size
            )
        )

        for article_batch, target_batch in tqdm(
            zip(article_batches, target_batches),
            total=len(article_batches)
        ):

            inputs = tokenizer(
                article_batch,
                max_length=1024,
                truncation=True,
                padding="max_length",
                return_tensors="pt"
            )

            input_ids = inputs["input_ids"].to(device)
            attention_mask = inputs["attention_mask"].to(device)

            summaries = model.generate(
                input_ids=input_ids,
                attention_mask=attention_mask,
                length_penalty=0.8,
                num_beams=8,
                max_length=128
            )

            decoded_summaries = [
                tokenizer.decode(
                    s,
                    skip_special_tokens=True,
                    clean_up_tokenization_spaces=True
                )
                for s in summaries
            ]

            decoded_summaries = [
                summary.strip()
                for summary in decoded_summaries
            ]

            metric.add_batch(
                predictions=decoded_summaries,
                references=target_batch
            )

        score = metric.compute()

        return score

    def evaluate(self):

        if os.path.exists(self.config.metric_file_name):
            logger.info("Evaluation metrics already exist. Skipping evaluation.")
            return

        device = "cuda" if torch.cuda.is_available() else "cpu"

        tokenizer = AutoTokenizer.from_pretrained(
            self.config.tokenizer_path
        )

        model = AutoModelForSeq2SeqLM.from_pretrained(
            self.config.model_path
        ).to(device)

        dataset_samsum_pt = load_from_disk(
            self.config.data_path
        )

        rouge_metric = evaluate.load("rouge")

        score = self.calculate_metric_on_test_ds(
            dataset_samsum_pt["test"],
            rouge_metric,
            model,
            tokenizer
        )

        score = {
            key: round(value, 4)
            for key, value in score.items()
        }

        score_df = pd.DataFrame([score])

        score_df.to_csv(
            self.config.metric_file_name,
            index=False
        )

        logger.info(f"Evaluation scores: {score}")