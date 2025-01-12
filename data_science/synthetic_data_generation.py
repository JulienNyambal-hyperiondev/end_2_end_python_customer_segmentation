"""
This module generates synthetic data for the purpose of testing and demonstration.
"""

import numpy as np

RANDOM_SEED = 42

def generate_synthetic_data():
    """
    Generate synthetic data for customer segmentation.
    Returns:
        dict: A dictionary containing synthetic data.
    """
    # Generate Synthetic Data 
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
    return data