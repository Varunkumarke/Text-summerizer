# from textsummarizer.logging import logger

# logger.info("Welcome to our custom logging")


from textsummarizer.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline

from textsummarizer.logging import logger


STAGE_NAME = "Data Ingestion Stage"

try:
    logger.info(f">>>>> stage {STAGE_NAME} started <<<<<")
    obj = DataIngestionTrainingPipeline()
    obj.main()
    logger.info(f">>>>> stage {STAGE_NAME} completed <<<<<\n\nx==========x")

except Exception as e:
    logger.exception(e)
    raise e

