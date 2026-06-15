"""
train_model.py
AI Nutritionist - Model Training Script
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error
import joblib
import warnings
warnings.filterwarnings('ignore')

def main():
    print("="*60)
    print("AI NUTRITIONIST - TRAINING MODEL")
    print("="*60)
    
    # Step 1: Create dataset
    print("\n[1/5] Creating dataset...")
    np.random.seed(42)
    
    # Create 2000 food items
    data = {
        'protein': np.random.uniform(0, 50, 2000),
        'carbs': np.random.uniform(0, 100, 2000),
        'fat': np.random.uniform(0, 60, 2000),
        'fiber': np.random.uniform(0, 20, 2000)
    }
    
    df = pd.DataFrame(data)
    
    # Calculate calories (protein=4, carbs=4, fat=9 calories per gram)
    df['calories'] = (df['protein'] * 4 + df['carbs'] * 4 + df['fat'] * 9)
    print(f"   Created {len(df)} food items")
    
    # Step 2: Split features and target
    print("\n[2/5] Preparing features...")
    X = df[['protein', 'carbs', 'fat', 'fiber']]
    y = df['calories']
    print(f"   Features: {X.shape[1]} columns")
    
    # Step 3: Train-test split
    print("\n[3/5] Splitting data (80-20)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"   Training: {len(X_train)} samples")
    print(f"   Testing: {len(X_test)} samples")
    
    # Step 4: Train model
    print("\n[4/5] Training Random Forest...")
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=15,
        random_state=42
    )
    model.fit(X_train, y_train)
    print("   Training complete!")
    
    # Step 5: Evaluate
    print("\n[5/5] Evaluating model...")
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    
    print(f"\n   R2 Score: {r2:.4f}")
    print(f"   MAE: {mae:.2f} calories")
    
    # Save model
    joblib.dump(model, 'best_model.pkl')
    print("\n✅ Model saved as 'best_model.pkl'")
    
    print("\n" + "="*60)
    print("TRAINING COMPLETE!")
    print("="*60)

if __name__ == "__main__":
    main()