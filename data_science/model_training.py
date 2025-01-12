import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
import pickle
import os
from synthetic_data_generation import generate_synthetic_data
import configparser

# Load configuration
config = configparser.ConfigParser()
config.read('../config.ini')

# Get configuration values
RANDOM_SEED = config.getint('data_science', 'random_seed')
DATA_PATH = config.get('data_science', 'data_path')
MODEL_PATH = config.get('data_science', 'model_path')
PREPROCESSOR_PATH = config.get('data_science', 'preprocessor_path')

PLOTS_FILENAME = "customer_clusters.png"
PLOTS_DIR = 'plots'

df = pd.DataFrame(generate_synthetic_data())

# Preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), ['amount_spent', 'tenure']),
        ('cat', OneHotEncoder(handle_unknown='ignore'), ['area', 'qualification'])
    ])

processed_data = preprocessor.fit_transform(df)

# K-Means Clustering
kmeans = KMeans(n_clusters=3, random_state=RANDOM_SEED, n_init='auto')  # 3 clusters

# Fit the model
df['cluster'] = kmeans.fit_predict(processed_data)

# Analyze cluster means to assign labels (Low, Middle, High)
cluster_means = df.groupby('cluster').mean(numeric_only=True)
print("Cluster Means:\n", cluster_means)

# Determine cluster labels based on amount_spent
cluster_labels = {}
sorted_clusters = cluster_means.sort_values('amount_spent').index.tolist()
cluster_labels[sorted_clusters[0]] = 'Low Income'
cluster_labels[sorted_clusters[1]] = 'Middle Income'
cluster_labels[sorted_clusters[2]] = 'High Income'

df['cluster_label'] = df['cluster'].map(cluster_labels)
print("\nCluster Labels:\n", cluster_labels)

# Save the model and preprocessor
pickle.dump(kmeans, open(MODEL_PATH, 'wb'))

filename_preprocessor = PREPROCESSOR_PATH
pickle.dump(preprocessor, open(filename_preprocessor, 'wb'))

# Visualization (using only two numerical features for plotting)
plt.figure(figsize=(10, 6))
for cluster, label in cluster_labels.items():
    cluster_data = df[df['cluster'] == cluster]
    plt.scatter(cluster_data['amount_spent'], cluster_data['tenure'], label=label)

plt.xlabel('Amount Spent')
plt.ylabel('Tenure (Years)')
plt.title('Customer Segmentation (K-Means)')
plt.legend()
plt.grid(True)
# Create a 'plots' directory if it doesn't exist
os.makedirs(PLOTS_DIR, exist_ok=True)

# Save the plot to a PNG file in the 'plots' directory
plt.savefig(os.path.join(PLOTS_DIR, PLOTS_FILENAME))

# Show the plot (optional - remove if you don't need to display it)
plt.show()

# Example of prediction
example_data = pd.DataFrame({
    'area': ['North London'],
    'amount_spent': [50000],
    'tenure': [10],
    'qualification': ['Masters']
})

example_processed = preprocessor.transform(example_data)
example_cluster = kmeans.predict(example_processed)
example_label = cluster_labels.get(example_cluster[0])
print(f'\nExample data belongs to cluster: {example_cluster} ({example_label})')

# Save the DataFrame (Optional)
df.to_csv('customer_data_with_clusters.csv', index=False)