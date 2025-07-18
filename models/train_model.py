import pandas as pd
import os
import joblib

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# --- Step 1: Load Dataset ---
print("\U0001F4C2 Loading dataset...")
df = pd.read_csv("employee_data.csv")

# --- Step 2: Define Features and Target ---
y = df["Salary"]
X = df.drop("Salary", axis=1)

# --- Step 3: Identify Categorical Columns ---
cat_cols = X.select_dtypes(include="object").columns.tolist()

# --- Step 4: Preprocessing Pipeline ---
preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols)
    ],
    remainder="passthrough"  # Keep numerical columns unchanged
)

# --- Step 5: Full Pipeline: Preprocessing + Model ---
model_pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(n_estimators=100, random_state=42))
])

# --- Step 6: Train-Test Split ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- Step 7: Train Model ---
print("✨ Training RandomForest model...")
model_pipeline.fit(X_train, y_train)

# --- Step 8: Evaluate Model ---
r2 = model_pipeline.score(X_test, y_test)
print(f"✅ Model trained. Test R² Score: {r2:.3f}")

# --- Step 9: Save Trained Model ---
os.makedirs("models", exist_ok=True)
model_path = "models/salary_model.pkl"
joblib.dump(model_pipeline, model_path)
print(f"📦 Model saved to: {model_path}")
