import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler


print("Loading Iris dataset...")
iris = load_iris()
X = iris.data  
y = iris.target 

iris_df = pd.DataFrame(X, columns=iris.feature_names)
iris_df['species'] = y
iris_df['species_name'] = [iris.target_names[i] for i in y]

print("Dataset Overview:")
print(f"Shape: {X.shape}")
print(f"Features: {iris.feature_names}")
print(f"Target classes: {iris.target_names}")
print(f"\nMissing values: {iris_df.isnull().sum().sum()}")
print("\n=== Exploratory Data Analysis ===")
print(iris_df.describe())

plt.figure(figsize=(15, 10))
plt.subplot(2, 2, 1)
sns.boxplot(x='species', y='sepal length (cm)', data=iris_df)
plt.title('Sepal Length by Species')
plt.subplot(2, 2, 2)
sns.boxplot(x='species', y='sepal width (cm)', data=iris_df)
plt.title('Sepal Width by Species')
plt.subplot(2, 2, 3)
sns.boxplot(x='species', y='petal length (cm)', data=iris_df)
plt.title('Petal Length by Species')
plt.subplot(2, 2, 4)
sns.boxplot(x='species', y='petal width (cm)', data=iris_df)
plt.title('Petal Width by Species')
plt.tight_layout()
plt.savefig('iris_eda.png')
plt.show()

print("\n=== Data Preprocessing ===")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f"Training set size: {X_train.shape[0]}")
print(f"Test set size: {X_test.shape[0]}")
print("\n=== Training Decision Tree Classifier ===")
dt_classifier = DecisionTreeClassifier(
    max_depth=3, 
    random_state=42
)

dt_classifier.fit(X_train_scaled, y_train)

y_pred = dt_classifier.predict(X_test_scaled)

print("\n=== Model Evaluation ===")
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted')
recall = recall_score(y_test, y_pred, average='weighted')

print(f"Accuracy: {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=iris.target_names))

cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=iris.target_names, 
            yticklabels=iris.target_names)
plt.title('Confusion Matrix - Decision Tree Classifier')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.savefig('confusion_matrix.png')
plt.show()

feature_importance = dt_classifier.feature_importances_
features = iris.feature_names

plt.figure(figsize=(10, 6))
sns.barplot(x=feature_importance, y=features)
plt.title('Feature Importance in Decision Tree')
plt.xlabel('Importance Score')
plt.tight_layout()
plt.savefig('feature_importance.png')
plt.show()

print("\nFeature Importance:")
for feature, importance in zip(features, feature_importance):
    print(f"{feature}: {importance:.4f}")

from sklearn.tree import plot_tree

plt.figure(figsize=(20, 10))
plot_tree(dt_classifier, 
          feature_names=iris.feature_names,
          class_names=iris.target_names,
          filled=True,
          rounded=True,
          fontsize=12)
plt.title('Decision Tree Visualization')
plt.savefig('decision_tree.png', dpi=300, bbox_inches='tight')
plt.show()

print("\n=== Model Training Complete ===")