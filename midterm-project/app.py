from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import pandas as pd
import joblib
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

# Mount a static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load the model at startup
try:
    model = joblib.load('models/wine_quality_model.joblib')
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Error loading model: {str(e)}")
    raise

class WineFeatures(BaseModel):
    fixed_acidity: float
    volatile_acidity: float
    citric_acid: float
    residual_sugar: float
    chlorides: float
    free_sulfur_dioxide: float
    total_sulfur_dioxide: float
    density: float
    ph: float
    sulphates: float
    alcohol: float

@app.post("/predict")
async def predict(features: WineFeatures):
    try:
        # Convert input features to DataFrame
        df = pd.DataFrame([features.dict()])
        logger.debug(f"Input features: {df.to_dict()}")
        
        # Make prediction
        prediction = model.predict(df)
        logger.debug(f"Prediction made: {prediction}")
        
        return {"predicted_quality": float(prediction[0])}
    
    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Wine Quality Predictor</title>
        <link rel="stylesheet" href="/static/styles.css">
    </head>
    <body>
        <div class="container">
            <header>
                <h1>🍷 Wine Quality Predictor</h1>
                <p>Predict wine quality based on physicochemical properties</p>
            </header>
            
            <div class="form-container">
                <form id="prediction-form">
                    <div class="form-grid">
                        <div class="form-group">
                            <label for="fixed_acidity">Fixed Acidity</label>
                            <input type="number" step="0.1" id="fixed_acidity" name="fixed_acidity" required>
                        </div>
                        <div class="form-group">
                            <label for="volatile_acidity">Volatile Acidity</label>
                            <input type="number" step="0.01" id="volatile_acidity" name="volatile_acidity" required>
                        </div>
                        <div class="form-group">
                            <label for="citric_acid">Citric Acid</label>
                            <input type="number" step="0.01" id="citric_acid" name="citric_acid" required>
                        </div>
                        <div class="form-group">
                            <label for="residual_sugar">Residual Sugar</label>
                            <input type="number" step="0.1" id="residual_sugar" name="residual_sugar" required>
                        </div>
                        <div class="form-group">
                            <label for="chlorides">Chlorides</label>
                            <input type="number" step="0.001" id="chlorides" name="chlorides" required>
                        </div>
                        <div class="form-group">
                            <label for="free_sulfur_dioxide">Free Sulfur Dioxide</label>
                            <input type="number" step="1" id="free_sulfur_dioxide" name="free_sulfur_dioxide" required>
                        </div>
                        <div class="form-group">
                            <label for="total_sulfur_dioxide">Total Sulfur Dioxide</label>
                            <input type="number" step="1" id="total_sulfur_dioxide" name="total_sulfur_dioxide" required>
                        </div>
                        <div class="form-group">
                            <label for="density">Density</label>
                            <input type="number" step="0.0001" id="density" name="density" required>
                        </div>
                        <div class="form-group">
                            <label for="ph">pH</label>
                            <input type="number" step="0.01" id="ph" name="ph" required>
                        </div>
                        <div class="form-group">
                            <label for="sulphates">Sulphates</label>
                            <input type="number" step="0.01" id="sulphates" name="sulphates" required>
                        </div>
                        <div class="form-group">
                            <label for="alcohol">Alcohol</label>
                            <input type="number" step="0.1" id="alcohol" name="alcohol" required>
                        </div>
                    </div>
                    <button type="submit" class="submit-btn">Predict Quality</button>
                </form>
                <div id="result" class="result-container"></div>
            </div>
        </div>
        <script src="/static/script.js"></script>
    </body>
    </html>
    """