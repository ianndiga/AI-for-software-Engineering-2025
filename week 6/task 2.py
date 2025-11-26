# smart_agriculture.py
class SmartAgricultureSystem:
    def __init__(self):
        self.sensors = self.initialize_sensors()
        self.ai_model = self.initialize_ai_model()
        
    def initialize_sensors(self):
        """Define required sensors for smart agriculture"""
        return {
            'soil_moisture': {
                'type': 'capacitive soil moisture sensor',
                'units': '% VWC',
                'range': '0-100%'
            },
            'temperature': {
                'type': 'DS18B20 waterproof sensor',
                'units': '°C',
                'range': '-55°C to +125°C'
            },
            'humidity': {
                'type': 'DHT22',
                'units': '% RH',
                'range': '0-100%'
            },
            'light_intensity': {
                'type': 'BH1750',
                'units': 'lux',
                'range': '0-65535 lux'
            },
            'npk_sensor': {
                'type': 'JXCT soil NPK sensor',
                'units': 'mg/kg',
                'range': '0-1999 mg/kg'
            },
            'ph_sensor': {
                'type': 'analog pH sensor',
                'units': 'pH',
                'range': '0-14'
            }
        }
    
    def initialize_ai_model(self):
        """Initialize AI model for crop yield prediction"""
        import tensorflow as tf
        
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(64, activation='relu', input_shape=(6,)),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(16, activation='relu'),
            tf.keras.layers.Dense(1, activation='linear')  # Yield prediction
        ])
        
        model.compile(
            optimizer='adam',
            loss='mse',
            metrics=['mae']
        )
        
        return model
    
    def collect_sensor_data(self):
        """Simulate sensor data collection"""
        import random
        import time
        
        sensor_readings = {
            'timestamp': time.time(),
            'soil_moisture': random.uniform(15, 45),
            'temperature': random.uniform(15, 35),
            'humidity': random.uniform(30, 80),
            'light_intensity': random.uniform(1000, 10000),
            'nitrogen': random.uniform(50, 200),
            'phosphorus': random.uniform(30, 150),
            'potassium': random.uniform(100, 300),
            'ph_level': random.uniform(5.5, 7.5)
        }
        
        return sensor_readings
    
    def predict_yield(self, sensor_data):
        """Predict crop yield based on sensor data"""
        # Preprocess sensor data
        features = [
            sensor_data['soil_moisture'],
            sensor_data['temperature'],
            sensor_data['humidity'],
            sensor_data['light_intensity'],
            sensor_data['nitrogen'],
            sensor_data['ph_level']
        ]
        
        # Make prediction (in a real scenario, the model would be trained)
        prediction = self.ai_model.predict([features])
        return prediction[0][0]
    
    def generate_recommendations(self, sensor_data, yield_prediction):
        """Generate farming recommendations based on AI analysis"""
        recommendations = []
        
        if sensor_data['soil_moisture'] < 25:
            recommendations.append("Irrigation needed - soil moisture low")
        
        if sensor_data['nitrogen'] < 100:
            recommendations.append("Apply nitrogen-rich fertilizer")
            
        if sensor_data['ph_level'] < 6.0:
            recommendations.append("Consider soil pH adjustment")
            
        if yield_prediction < 0.7:  # Assuming normalized yield
            recommendations.append("Review crop management practices")
            
        return recommendations

# System demonstration
def demonstrate_smart_agriculture():
    system = SmartAgricultureSystem()
    
    print("=== Smart Agriculture IoT System ===")
    print("Sensors deployed:")
    for sensor, details in system.sensors.items():
        print(f"- {sensor}: {details['type']}")
    
    print("\nCollecting sensor data...")
    data = system.collect_sensor_data()
    print("Current sensor readings:")
    for key, value in data.items():
        if key != 'timestamp':
            print(f"- {key}: {value:.2f}")
    
    print("\nAI Analysis in progress...")
    yield_pred = system.predict_yield(data)
    recommendations = system.generate_recommendations(data, yield_pred)
    
    print(f"Predicted yield: {yield_pred:.2f}")
    print("Recommendations:")
    for rec in recommendations:
        print(f"- {rec}")

if __name__ == "__main__":
    demonstrate_smart_agriculture()