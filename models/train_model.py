import pandas as pd
import os
import joblib
import logging

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# --- Setup basic logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)


class SalaryModelTrainer:
    """
    A class to encapsulate the entire model training workflow.
    """
    def __init__(self, data_path: str, model_dir: str, model_name: str, config: dict):
        """
        Initializes the trainer with paths and configuration.

        Args:
            data_path (str): Path to the training data CSV file.
            model_dir (str): Directory to save the trained model.
            model_name (str): Filename for the saved model.
            config (dict): A dictionary containing model and process parameters.
        """
        self.data_path = data_path
        self.model_path = os.path.join(model_dir, model_name)
        self.config = config
        
        # Initialize state variables
        self.df = None
        self.pipeline = None
        self.r2_score = None

        os.makedirs(model_dir, exist_ok=True)
        logging.info("SalaryModelTrainer initialized.")

    def _load_and_prepare_data(self):
        """Loads data and separates features from the target variable."""
        logging.info(f"Loading dataset from '{self.data_path}'...")
        try:
            self.df = pd.read_csv(self.data_path)
            # Define features (X) and target (y)
            self.y = self.df[self.config["target_column"]]
            self.X = self.df.drop(self.config["target_column"], axis=1)
        except FileNotFoundError:
            logging.error(f"Dataset not found at {self.data_path}. Aborting.")
            raise

    def _build_pipeline(self):
        """Builds the scikit-learn preprocessing and model pipeline."""
        logging.info("Building model pipeline...")
        cat_cols = self.X.select_dtypes(include="object").columns.tolist()
        
        preprocessor = ColumnTransformer(
            transformers=[
                ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols)
            ],
            remainder="passthrough"
        )
        
        self.pipeline = Pipeline([
            ("preprocessor", preprocessor),
            ("regressor", RandomForestRegressor(
                n_estimators=self.config["n_estimators"],
                random_state=self.config["random_state"]
            ))
        ])
        logging.info("Pipeline built successfully.")

    def train(self):
        """Executes the full training and evaluation process."""
        self._load_and_prepare_data()
        self._build_pipeline()
        
        X_train, X_test, y_train, y_test = train_test_split(
            self.X, self.y,
            test_size=self.config["test_size"],
            random_state=self.config["random_state"]
        )
        
        logging.info("✨ Starting model training...")
        self.pipeline.fit(X_train, y_train)
        
        self.r2_score = self.pipeline.score(X_test, y_test)
        logging.info(f"✅ Model training complete. Test R² Score: {self.r2_score:.4f}")

    def save_model(self):
        """Saves the trained pipeline to a file."""
        if self.pipeline is None:
            logging.error("Model has not been trained yet. Cannot save.")
            return

        joblib.dump(self.pipeline, self.model_path)
        logging.info(f"📦 Model saved to: {self.model_path}")


# --- Main execution block ---
if __name__ == "__main__":
    # --- Centralized Configuration Dictionary ---
    TRAINING_CONFIG = {
        "target_column": "Salary",
        "random_state": 42,
        "test_size": 0.2,
        "n_estimators": 100
    }
    
    # --- Instantiate and run the trainer ---
    trainer = SalaryModelTrainer(
        data_path="employee_data.csv",
        model_dir="models",
        model_name="salary_model.pkl",
        config=TRAINING_CONFIG
    )
    
    trainer.train()
    trainer.save_model()