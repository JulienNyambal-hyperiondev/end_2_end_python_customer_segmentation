import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
import pickle
import os

RANDOM_SEED = 42
FILE_NAME_PROCESSOR = 'customer_segmentation_preprocessor.sav'
FILENAME_MODEL = 'customer_segmentation_model.sav'
PLOTS_FILENAME = "customer_clusters.png"
PLOTS_DIR = 'plots'

# Generate Synthetic Data (2000 data points)
np.random.seed(RANDOM_SEED)  # for reproducibility

n_samples = 5000

areas = ['North London', 'South London', 'East London', 'West London', 'Central London']
amounts_spent = np.random.uniform(1000.0, 100000.0, size=n_samples)  # £1,000.0 to £100,000.0 (float)
tenures = np.random.uniform(1, 20, size=n_samples)  # 1 to 20 years
qualifications = ['High School', 'Bachelor', 'Masters', 'PhD']

data = {
    'area': np.random.choice(areas, size=n_samples),
    'amount_spent': amounts_spent,
    'tenure': tenures,
    'qualification': np.random.choice(qualifications, size=n_samples)
}

df = pd.DataFrame(data)

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
filename_model = FILENAME_MODEL
pickle.dump(kmeans, open(filename_model, 'wb'))

filename_preprocessor = FILE_NAME_PROCESSOR
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