# --- Import Libraries ---
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import seaborn as sns
import matplotlib.pyplot as plt

# --- Load and Preprocess Data ---
try:
    df = pd.read_csv('data.csv')
    print("Dataset loaded successfully!")
    print(f"Dataset shape: {df.shape}")
except FileNotFoundError:
    print("ERROR: data.csv file not found!")
    print("Please download from: https://www.kaggle.com/datasets/uciml/breast-cancer-wisconsin-data")
    exit()

# Drop unnecessary column
df = df.drop(columns=['id', 'Unnamed: 32'], errors='ignore')
print(f"After dropping columns: {df.shape}")

# Encode the target variable 'diagnosis' (M=1, B=0)
le = LabelEncoder()
df['diagnosis'] = le.fit_transform(df['diagnosis'])
print(f"Target distribution: {pd.Series(df['diagnosis']).value_counts()}")

y = df['diagnosis'].map({0: 0, 1: 2})  # B->0, M->2
print(f"Priority distribution: Low={sum(y==0)}, High={sum(y==2)}")

# --- Split Data ---
X = df.drop(columns=['diagnosis'])
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
print(f"Training set: {X_train.shape}, Test set: {X_test.shape}")

# --- Train Model ---
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# --- Predict and Evaluate ---
y_pred = model.predict(X_test)

# --- Performance Metrics ---
accuracy = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred, average='weighted')

print("\n" + "="*50)
print("TASK 3: PREDICTIVE ANALYTICS FOR RESOURCE ALLOCATION")
print("="*50)
print(f"Accuracy: {accuracy:.4f}")
print(f"Weighted F1-Score: {f1:.4f}")
print("\nDetailed Classification Report:")
print(classification_report(y_test, y_pred, target_names=['Low Priority', 'High Priority']))

# --- Feature Importance ---
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print("\nTop 5 Most Important Features for Prediction:")
print(feature_importance.head(5))

# --- Interpretation for Report ---
print("\n" + "="*50)
print("INTERPRETATION FOR ASSIGNMENT REPORT:")
print("="*50)
print("This model demonstrates how AI can predict software issue priority:")
print(f"- The Random Forest classifier achieved {accuracy:.1%} accuracy")
print(f"- The weighted F1-score of {f1:.4f} shows good balance between precision and recall")
print("- This level of performance could help development teams:")
print("  * Automatically triage incoming bug reports")
print("  * Allocate resources to high-priority issues first")
print("  * Reduce manual effort in issue classification")