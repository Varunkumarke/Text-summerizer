from textsummarizer.config.configuration import configurationManager
from textsummarizer.components.model_evaluation import ModelEvaluation
from textsummarizer.logging import logger


class ModelEvaluationTrainingPipeline:

    def __init__(self):
        pass

    def main(self):

        config = configurationManager()

        model_evaluation_config = config.get_model_evaluation_config()

        model_evaluation = ModelEvaluation(
            config=model_evaluation_config
        )

        model_evaluation.evaluate()