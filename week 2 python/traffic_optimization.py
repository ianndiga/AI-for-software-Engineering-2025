import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.cluster import KMeans
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class UrbanTrafficOptimizer:
    """
    Machine Learning solution for urban traffic optimization
    addressing SDG 11: Sustainable Cities and Communities
    """
    
    def __init__(self):
        self.regression_model = None
        self.clustering_model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        
    def generate_sample_data(self, n_samples=1000):
        """
        Generate synthetic urban traffic data simulating real-world scenarios
        """
        np.random.seed(42)
        
        data = {
            'hour_of_day': np.random.randint(0, 24, n_samples),
            'day_of_week': np.random.randint(0, 7, n_samples),
            'is_weekend': np.random.choice([0, 1], n_samples, p=[0.7, 0.3]),
            'population_density': np.random.normal(5000, 2000, n_samples),
            'public_transport_coverage': np.random.uniform(0.1, 1.0, n_samples),
            'number_intersections': np.random.randint(5, 50, n_samples),
            'weather_condition': np.random.choice([0, 1, 2], n_samples, p=[0.6, 0.3, 0.1]),
            'special_event': np.random.choice([0, 1], n_samples, p=[0.9, 0.1]),
            'previous_traffic_flow': np.random.normal(1000, 300, n_samples)
        }
        
        df = pd.DataFrame(data)
        
        # Generate target variable: traffic_flow
        traffic_flow = (
            1000 + 
            df['hour_of_day'] * 15 +
            df['day_of_week'] * 10 +
            df['is_weekend'] * -200 +
            df['population_density'] * 0.05 +
            df['public_transport_coverage'] * -300 +
            df['number_intersections'] * 8 +
            df['weather_condition'] * 50 +
            df['special_event'] * 400 +
            df['previous_traffic_flow'] * 0.3 +
            np.random.normal(0, 50, n_samples)
        )
        
        df['traffic_flow'] = np.maximum(traffic_flow, 0)
        
        # Generate congestion level (0: Low, 1: Medium, 2: High)
        conditions = [
            df['traffic_flow'] < 800,
            (df['traffic_flow'] >= 800) & (df['traffic_flow'] < 1200),
            df['traffic_flow'] >= 1200
        ]
        choices = [0, 1, 2]
        df['congestion_level'] = np.select(conditions, choices)
        
        return df
    
    def preprocess_data(self, df):
        """
        Preprocess the data for machine learning
        """
        # Select features for modeling
        features = [
            'hour_of_day', 'day_of_week', 'is_weekend', 'population_density',
            'public_transport_coverage', 'number_intersections', 
            'weather_condition', 'special_event', 'previous_traffic_flow'
        ]
        
        X = df[features]
        y_flow = df['traffic_flow']
        y_congestion = df['congestion_level']
        
        return X, y_flow, y_congestion
    
    def train_regression_model(self, X, y):
        """
        Train Random Forest model to predict traffic flow
        """
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        self.regression_model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        
        self.regression_model.fit(X_train_scaled, y_train)
        
        # Evaluate model
        y_pred = self.regression_model.predict(X_test_scaled)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        
        print(f"Regression Model Performance:")
        print(f"MAE: {mae:.2f}")
        print(f"RMSE: {rmse:.2f}")
        
        return X_test_scaled, y_test, y_pred
    
    def train_clustering_model(self, X):
        """
        Use K-means to cluster urban areas based on traffic patterns
        """
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Determine optimal number of clusters using elbow method
        wcss = []
        for i in range(1, 11):
            kmeans = KMeans(n_clusters=i, random_state=42)
            kmeans.fit(X_scaled)
            wcss.append(kmeans.inertia_)
        
        # Choose optimal clusters (simplified - in practice use elbow point)
        optimal_clusters = 3
        self.clustering_model = KMeans(n_clusters=optimal_clusters, random_state=42)
        clusters = self.clustering_model.fit_predict(X_scaled)
        
        print(f"Clustering completed with {optimal_clusters} clusters")
        return clusters
    
    def predict_traffic_flow(self, input_features):
        """
        Predict traffic flow for new input
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")
        
        input_scaled = self.scaler.transform([input_features])
        prediction = self.regression_model.predict(input_scaled)
        return prediction[0]
    
    def analyze_traffic_patterns(self, df, clusters):
        """
        Analyze and visualize traffic patterns across different clusters
        """
        df['cluster'] = clusters
        
        # Cluster analysis
        cluster_summary = df.groupby('cluster').agg({
            'traffic_flow': ['mean', 'std'],
            'congestion_level': 'mean',
            'public_transport_coverage': 'mean',
            'population_density': 'mean'
        }).round(2)
        
        print("\nCluster Analysis Summary:")
        print(cluster_summary)
        
        return cluster_summary
    
    def visualize_results(self, df, clusters, y_test, y_pred):
        """
        Create comprehensive visualizations of the results
        """
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Plot 1: Actual vs Predicted traffic flow
        axes[0, 0].scatter(y_test, y_pred, alpha=0.6)
        axes[0, 0].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
        axes[0, 0].set_xlabel('Actual Traffic Flow')
        axes[0, 0].set_ylabel('Predicted Traffic Flow')
        axes[0, 0].set_title('Actual vs Predicted Traffic Flow')
        
        # Plot 2: Traffic flow by hour of day
        hourly_traffic = df.groupby('hour_of_day')['traffic_flow'].mean()
        axes[0, 1].plot(hourly_traffic.index, hourly_traffic.values, marker='o')
        axes[0, 1].set_xlabel('Hour of Day')
        axes[0, 1].set_ylabel('Average Traffic Flow')
        axes[0, 1].set_title('Traffic Flow Patterns by Hour')
        axes[0, 1].grid(True)
        
        # Plot 3: Cluster distribution
        cluster_counts = pd.Series(clusters).value_counts().sort_index()
        axes[1, 0].bar(cluster_counts.index, cluster_counts.values)
        axes[1, 0].set_xlabel('Cluster')
        axes[1, 0].set_ylabel('Number of Areas')
        axes[1, 0].set_title('Distribution of Urban Areas Across Clusters')
        
        # Plot 4: Impact of public transport on traffic
        sns.scatterplot(data=df, x='public_transport_coverage', y='traffic_flow', 
                       hue='congestion_level', ax=axes[1, 1])
        axes[1, 1].set_xlabel('Public Transport Coverage')
        axes[1, 1].set_ylabel('Traffic Flow')
        axes[1, 1].set_title('Impact of Public Transport on Traffic Flow')
        
        plt.tight_layout()
        plt.savefig('assets/results_visualization.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def generate_recommendations(self, cluster_summary):
        """
        Generate data-driven recommendations for urban planning
        """
        print("\n" + "="*50)
        print("DATA-DRIVEN URBAN PLANNING RECOMMENDATIONS")
        print("="*50)
        
        recommendations = []
        
        for cluster in cluster_summary.index:
            avg_traffic = cluster_summary.loc[cluster, ('traffic_flow', 'mean')]
            avg_congestion = cluster_summary.loc[cluster, ('congestion_level', 'mean')]
            transport_coverage = cluster_summary.loc[cluster, ('public_transport_coverage', 'mean')]
            
            print(f"\nCluster {cluster} Analysis:")
            print(f"  - Average Traffic Flow: {avg_traffic:.0f} vehicles/hour")
            print(f"  - Average Congestion Level: {avg_congestion:.1f}/2")
            print(f"  - Public Transport Coverage: {transport_coverage:.2f}")
            
            if avg_congestion > 1.5:
                rec = "HIGH PRIORITY: Implement congestion pricing, expand public transport, and promote alternative routes"
            elif avg_congestion > 1.0:
                rec = "MEDIUM PRIORITY: Optimize traffic signals, improve bus lanes, and encourage carpooling"
            else:
                rec = "LOW PRIORITY: Maintain current infrastructure with focus on preventive measures"
            
            if transport_coverage < 0.5:
                rec += " | URGENT: Significantly expand public transport network"
            
            recommendations.append(rec)
            print(f"  Recommendation: {rec}")
        
        return recommendations

def main():
    """
    Main execution function for the Urban Traffic Optimization system
    """
    print("🚦 Urban Traffic Optimization for SDG 11")
    print("="*50)
    
    # Initialize the optimizer
    optimizer = UrbanTrafficOptimizer()
    
    # Generate and explore sample data
    print("1. Generating urban traffic data...")
    df = optimizer.generate_sample_data(2000)
    print(f"   Generated {len(df)} data points")
    print(f"   Data columns: {list(df.columns)}")
    
    # Preprocess data
    print("\n2. Preprocessing data...")
    X, y_flow, y_congestion = optimizer.preprocess_data(df)
    
    # Train regression model
    print("\n3. Training traffic flow prediction model...")
    X_test, y_test, y_pred = optimizer.train_regression_model(X, y_flow)
    
    # Train clustering model
    print("\n4. Clustering urban areas...")
    clusters = optimizer.train_clustering_model(X)
    
    # Analyze patterns
    print("\n5. Analyzing traffic patterns...")
    cluster_summary = optimizer.analyze_traffic_patterns(df, clusters)
    
    # Mark as trained
    optimizer.is_trained = True
    
    # Visualize results
    print("\n6. Generating visualizations...")
    optimizer.visualize_results(df, clusters, y_test, y_pred)
    
    # Generate recommendations
    print("\n7. Generating urban planning recommendations...")
    recommendations = optimizer.generate_recommendations(cluster_summary)
    
    # Save models
    print("\n8. Saving trained models...")
    joblib.dump(optimizer.regression_model, 'models/traffic_model.pkl')
    joblib.dump(optimizer.clustering_model, 'models/clustering_model.pkl')
    joblib.dump(optimizer.scaler, 'models/scaler.pkl')
    
    # Demo prediction
    print("\n9. Demonstration prediction...")
    sample_input = [8, 1, 0, 6000, 0.7, 25, 1, 0, 950]  # Monday 8 AM, moderate conditions
    predicted_flow = optimizer.predict_traffic_flow(sample_input)
    print(f"   Predicted traffic flow: {predicted_flow:.0f} vehicles/hour")
    
    print("\n" + "="*50)
    print("✅ Urban Traffic Optimization System Complete!")
    print("="*50)

if __name__ == "__main__":
    main()