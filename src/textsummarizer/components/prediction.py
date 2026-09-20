# import torch
# from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# from textsummarizer.logging import logger


# class PredictionPipeline:

#     def __init__(self):
#         self.device = "cuda" if torch.cuda.is_available() else "cpu"

#         self.model = AutoModelForSeq2SeqLM.from_pretrained(
#             "artifacts/model_trainer/pegasus-samsum-model"
#         ).to(self.device)

#         self.tokenizer = AutoTokenizer.from_pretrained(
#             "artifacts/model_trainer/pegasus-samsum-model"
#         )

#     def predict(self, text):

#         inputs = self.tokenizer(
#             text,
#             max_length=1024,
#             truncation=True,
#             padding="max_length",
#             return_tensors="pt"
#         )

#         input_ids = inputs["input_ids"].to(self.device)
#         attention_mask = inputs["attention_mask"].to(self.device)

#         with torch.no_grad():

#             summary_ids = self.model.generate(
#                 input_ids=input_ids,
#                 attention_mask=attention_mask,
#                 length_penalty=0.8,
#                 num_beams=8,
#                 max_length=128
#             )

#         summary = self.tokenizer.decode(
#             summary_ids[0],
#             skip_special_tokens=True,
#             clean_up_tokenization_spaces=True
#         )

#         return summary.strip()


import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from textsummarizer.logging import logger


class PredictionPipeline:

    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            "kvk2005/pegasus-samsum-kv"
        ).to(self.device)

        self.tokenizer = AutoTokenizer.from_pretrained(
            "kvk2005/pegasus-samsum-kv"
        )

    def predict(self, text):

        inputs = self.tokenizer(
            text,
            max_length=1024,
            truncation=True,
            padding="max_length",
            return_tensors="pt"
        )

        input_ids = inputs["input_ids"].to(self.device)
        attention_mask = inputs["attention_mask"].to(self.device)

        with torch.no_grad():

            summary_ids = self.model.generate(
                input_ids=input_ids,
                attention_mask=attention_mask,
                length_penalty=0.8,
                num_beams=8,
                max_length=128
            )

        summary = self.tokenizer.decode(
            summary_ids[0],
            skip_special_tokens=True,
            clean_up_tokenization_spaces=True
        )

        return summary.strip()