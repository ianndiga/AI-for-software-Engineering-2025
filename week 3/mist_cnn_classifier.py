import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers # type: ignore
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report

print("TensorFlow version:", tf.__version__)

print("\n=== Loading MNIST Dataset ===")
(X_train, y_train), (X_test, y_test) = keras.datasets.mnist.load_data()

print(f"Training data shape: {X_train.shape}")
print(f"Training labels shape: {y_train.shape}")
print(f"Test data shape: {X_test.shape}")
print(f"Test labels shape: {y_test.shape}")

X_train = X_train.astype('float32') / 255.0
X_test = X_test.astype('float32') / 255.0
X_train = X_train.reshape(-1, 28, 28, 1)
X_test = X_test.reshape(-1, 28, 28, 1)

y_train_categorical = keras.utils.to_categorical(y_train, 10)
y_test_categorical = keras.utils.to_categorical(y_test, 10)

print(f"Reshaped training data: {X_train.shape}")
print(f"One-hot encoded labels: {y_train_categorical.shape}")
print("\n=== Visualizing Sample Images ===")
plt.figure(figsize=(12, 6))
for i in range(10):
    plt.subplot(2, 5, i + 1)
    plt.imshow(X_train[i].reshape(28, 28), cmap='gray')
    plt.title(f'Label: {y_train[i]}')
    plt.axis('off')
plt.tight_layout()
plt.savefig('mnist_samples.png')
plt.show()

print("\n=== Building CNN Model ===")
model = keras.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(10, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

print("\nModel Architecture:")
model.summary()

print("\n=== Training CNN Model ===")
history = model.fit(
    X_train, y_train_categorical,
    batch_size=128,
    epochs=10,
    validation_split=0.1,
    verbose=1
)

print("\n=== Model Evaluation ===")
test_loss, test_accuracy = model.evaluate(X_test, y_test_categorical, verbose=0)
print(f"Test Accuracy: {test_accuracy:.4f}")
print(f"Test Loss: {test_loss:.4f}")

plt.figure(figsize=(15, 5))
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Model Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

plt.tight_layout()
plt.savefig('training_history.png')
plt.show()

y_pred_proba = model.predict(X_test)
y_pred = np.argmax(y_pred_proba, axis=1)

cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', square=True)
plt.title('Confusion Matrix - MNIST CNN Classifier')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.savefig('mnist_confusion_matrix.png')
plt.show()

print("\nClassification Report:")
print(classification_report(y_test, y_pred))
print("\n=== Visualizing Predictions on Sample Test Images ===")
sample_indices = np.random.choice(len(X_test), 5, replace=False)

plt.figure(figsize=(15, 8))
for i, idx in enumerate(sample_indices):
    plt.subplot(2, 5, i + 1)
    plt.imshow(X_test[idx].reshape(28, 28), cmap='gray')
    true_label = y_test[idx]
    pred_label = y_pred[idx]
    confidence = y_pred_proba[idx][pred_label]
    
    color = 'green' if true_label == pred_label else 'red'
    plt.title(f'True: {true_label}, Pred: {pred_label}\nConf: {confidence:.2f}', color=color)
    plt.axis('off')

misclassified_indices = np.where(y_pred != y_test)[0]
if len(misclassified_indices) > 0:
    misclassified_samples = np.random.choice(misclassified_indices, min(5, len(misclassified_indices)), replace=False)
    
    for i, idx in enumerate(misclassified_samples):
        plt.subplot(2, 5, i + 6)
        plt.imshow(X_test[idx].reshape(28, 28), cmap='gray')
        true_label = y_test[idx]
        pred_label = y_pred[idx]
        confidence = y_pred_proba[idx][pred_label]
        
        plt.title(f'True: {true_label}, Pred: {pred_label}\nConf: {confidence:.2f}', color='red')
        plt.axis('off')

plt.tight_layout()
plt.savefig('prediction_samples.png')
plt.show()

print(f"\n=== Training Complete ===")
print(f"Final Test Accuracy: {test_accuracy:.4f} (>95% target: {'✓ ACHIEVED' if test_accuracy > 0.95 else '✗ NOT ACHIEVED'})")

model.save('mnist_cnn_model.h5')
print("Model saved as 'mnist_cnn_model.h5'")