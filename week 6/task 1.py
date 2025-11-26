# recyclable_classifier.py
import tensorflow as tf
import numpy as np
import os
from tensorflow.keras import layers # type: ignore
import matplotlib.pyplot as plt

class EdgeAIRecyclableClassifier:
    def __init__(self):
        self.model = None
        self.tflite_model = None
        self.class_names = ['plastic', 'paper', 'glass', 'metal']
        
    def create_synthetic_data(self, num_samples=1000):
        """Create synthetic image data for demonstration"""
        # we'll create synthetic data
        X_train = np.random.rand(num_samples, 128, 128, 3).astype(np.float32)
        y_train = np.random.randint(0, 4, num_samples)
        
        X_test = np.random.rand(200, 128, 128, 3).astype(np.float32)
        y_test = np.random.randint(0, 4, 200)
        
        return (X_train, y_train), (X_test, y_test)
    
    def create_model(self):
        """Create a lightweight CNN model for edge deployment"""
        model = tf.keras.Sequential([
            layers.Conv2D(16, 3, activation='relu', input_shape=(128, 128, 3)),
            layers.MaxPooling2D(),
            layers.Conv2D(32, 3, activation='relu'),
            layers.MaxPooling2D(),
            layers.Conv2D(64, 3, activation='relu'),
            layers.MaxPooling2D(),
            layers.Flatten(),
            layers.Dense(128, activation='relu'),
            layers.Dropout(0.2),
            layers.Dense(4, activation='softmax')  # plastic, paper, glass, metal
        ])
        
        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        self.model = model
        print("Model created successfully!")
        model.summary()
        return model
    
    def train_model(self, epochs=10):
        """Train the model with synthetic data"""
        (X_train, y_train), (X_test, y_test) = self.create_synthetic_data()
        
        print("Training model...")
        history = self.model.fit(
            X_train, y_train,
            epochs=epochs,
            validation_data=(X_test, y_test),
            batch_size=32,
            verbose=1
        )
        
        # Evaluate the model
        test_loss, test_accuracy = self.model.evaluate(X_test, y_test)
        print(f"Test Accuracy: {test_accuracy:.4f}")
        
        return history
    
    def convert_to_tflite(self):
        """Convert model to TensorFlow Lite format"""
        if self.model is None:
            raise ValueError("Model must be created and trained first!")
            
        converter = tf.lite.TFLiteConverter.from_keras_model(self.model)
        converter.optimizations = [tf.lite.Optimize.DEFAULT]
        self.tflite_model = converter.convert()
        
        # Save the model
        with open('recyclable_classifier.tflite', 'wb') as f:
            f.write(self.tflite_model)
        
        print("Model converted to TensorFlow Lite successfully!")
        print(f"Model size: {len(self.tflite_model) / 1024 / 1024:.2f} MB")
        
        return self.tflite_model
    
    def test_tflite_model(self, num_tests=5):
        """Test the TFLite model with sample data"""
        if self.tflite_model is None:
            raise ValueError("TFLite model not created! Run convert_to_tflite first.")
            
        interpreter = tf.lite.Interpreter(model_content=self.tflite_model)
        interpreter.allocate_tensors()
        
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        
        print(f"\nTesting TFLite model with {num_tests} samples...")
        print("Input details:", input_details[0]['shape'])
        print("Output details:", output_details[0]['shape'])
        
        # Test with sample images
        test_images = np.random.rand(num_tests, 128, 128, 3).astype(np.float32)
        
        for i, image in enumerate(test_images):
            interpreter.set_tensor(input_details[0]['index'], [image])
            interpreter.invoke()
            output = interpreter.get_tensor(output_details[0]['index'])
            predicted_class = np.argmax(output[0])
            confidence = np.max(output[0])
            
            print(f"Sample {i+1}: Predicted {self.class_names[predicted_class]} "
                  f"with {confidence:.2f} confidence")
        
        return True
    
    def benchmark_model(self):
        """Benchmark the TFLite model performance"""
        if self.tflite_model is None:
            raise ValueError("TFLite model not created!")
            
        import time
        
        interpreter = tf.lite.Interpreter(model_content=self.tflite_model)
        interpreter.allocate_tensors()
        
        input_details = interpreter.get_input_details()
        
        # Warm-up
        test_input = np.random.rand(1, 128, 128, 3).astype(np.float32)
        interpreter.set_tensor(input_details[0]['index'], test_input)
        interpreter.invoke()
        
        # Benchmark
        times = []
        for _ in range(100):
            start_time = time.time()
            interpreter.set_tensor(input_details[0]['index'], test_input)
            interpreter.invoke()
            end_time = time.time()
            times.append((end_time - start_time) * 1000)  # Convert to ms
        
        avg_time = np.mean(times)
        print(f"Average inference time: {avg_time:.2f} ms")
        print(f"FPS: {1000/avg_time:.2f}")
        
        return avg_time

# Usage example
if __name__ == "__main__":
    # Initialize classifier
    classifier = EdgeAIRecyclableClassifier()
    
    # Create and train model
    model = classifier.create_model()
    history = classifier.train_model(epochs=5)
    
    # Convert to TensorFlow Lite
    tflite_model = classifier.convert_to_tflite()
    
    # Test the converted model
    classifier.test_tflite_model()
    
    # Benchmark performance
    classifier.benchmark_model()