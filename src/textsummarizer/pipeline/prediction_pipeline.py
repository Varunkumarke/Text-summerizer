from textsummarizer.components.prediction import PredictionPipeline
pipeline = PredictionPipeline()

def predict(text):
   
    summary = pipeline.predict(text)

    return summary