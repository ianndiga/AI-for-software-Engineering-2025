# --- Import Libraries ---
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, classification_report
from sklearn.preprocessing import LabelEncoder

# --- Load and Preprocess Data ---
df = pd.read_csv('data.csv')
# Drop unnecessary column
df = df.drop(columns=['id', 'Unnamed: 32'])
# Encode the target variable 'diagnosis' (M=1, B=0)
le = LabelEncoder()
df['diagnosis'] = le.fit_transform(df['diagnosis'])

# --- Create a Synthetic "Issue Priority" ---
# For this exercise, we map the cancer diagnosis to a software issue priority.
# Malignant (M) -> High Priority (2)
# Benign (B) -> Low Priority (0)
# We'll create a middle tier synthetically for demonstration.
y = df['diagnosis'].map({0: 0, 1: 2}) # B->0, M->2

# --- Split Data ---
X = df.drop(columns=['diagnosis'])
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# --- Train Model ---
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# --- Predict and Evaluate ---
y_pred = model.predict(X_test)

# --- Performance Metrics ---
accuracy = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred, average='weighted')

print(f"Accuracy: {accuracy:.4f}")
print(f"Weighted F1-Score: {f1:.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))