# Customer Segmentation Project

A machine learning application that segments customers into Low, Middle, and High Income groups using K-Means clustering. The project includes synthetic data generation, model training, and a web interface for making predictions.

## Project Structure

```
customer_segmentation/
├── artifacts/
│   ├── customer_data_with_clusters.csv
│   ├── customer_segmentation_model.sav
│   └── customer_segmentation_preprocessor.sav
├── data_science/
│   ├── plots/
│   │   └── customer_clusters.png
│   ├── customer_data_with_clusters.csv
│   ├── model_training.py
│   └── synthetic_data_generation.py
├── templates/
│   └── index.html
├── techtalk_venv/
├── .gitignore
├── app.py
├── config.ini
├── README.md
└── requirements.txt
```

## Features

- **Synthetic Data Generation**: Creates realistic customer data for training
- **K-Means Clustering**: Segments customers into three distinct groups
- **Data Visualization**: Generates plots to visualize customer segments
- **Web Interface**: Flask-based UI for making predictions
- **Preprocessing Pipeline**: Handles both numerical and categorical features
- **Model Persistence**: Saves trained model and preprocessor for reuse

## Technical Details

### Data Features

- Area (Categorical): Customer's geographical location
- Amount Spent (Numerical): Total spending amount
- Tenure (Numerical): Years as a customer
- Qualification (Categorical): Educational qualification

### Model Architecture

- **Preprocessing**: 
  - StandardScaler for numerical features (amount_spent, tenure)
  - OneHotEncoder for categorical features (area, qualification)
- **Clustering**: K-Means with 3 clusters
- **Output**: Low Income, Middle Income, or High Income segment

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/customer-segmentation.git
   cd customer-segmentation
   ```

2. **Set Up Python Environment**
   ```bash
   python -m venv techtalk_venv
   
   # Windows
   techtalk_venv\Scripts\activate
   
   # Unix/MacOS
   source techtalk_venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

The `config.ini` file contains important settings:

```ini
[data_science]
random_seed = 42
data_path = artifacts/customer_data_with_clusters.csv
model_path = artifacts/customer_segmentation_model.sav
preprocessor_path = artifacts/customer_segmentation_preprocessor.sav

[flask]
debug = True
port = 5000
```

## Usage

1. **Generate Data and Train Model**
   ```bash
   cd data_science
   python model_training.py
   ```
   This will:
   - Generate synthetic customer data
   - Train the K-Means model
   - Create visualization plots
   - Save model artifacts

2. **Start the Web Application**
   ```bash
   cd ..
   flask run
   ```
   Access the application at `http://localhost:5000`

3. **Make Predictions**
   - Input customer details in the web interface
   - Click "Predict" to see the customer segment
   - Results are color-coded:
     - Red: Low Income
     - Orange: Middle Income
     - Green: High Income

## Development

### Key Files

- `synthetic_data_generation.py`: Contains logic for creating synthetic customer data
- `model_training.py`: Implements the clustering model and preprocessing pipeline
- `app.py`: Flask application with routing and prediction logic
- `index.html`: Web interface template

### Adding New Features

1. **Extend Data Generation**
   - Modify `synthetic_data_generation.py` to add new features
   - Update preprocessing pipeline in `model_training.py`

2. **Modify Web Interface**
   - Edit `templates/index.html` for UI changes
   - Update routes in `app.py` for new functionality

## Deployment

### Local Deployment
Follow the installation and usage instructions above.

### Render Deployment

1. **Create a Git Repository**
   - Push your code to a Git repository (GitHub, GitLab, etc.)
   - Ensure `.gitignore` excludes:
     ```
     techtalk_venv/
     __pycache__/
     *.pyc
     ```

2. **Create a Render Account**
   - Sign up at [render.com](https://render.com)
   - Connect your Git repository

3. **Create a New Web Service**
   - Click "New +"
   - Select "Web Service"
   - Choose your repository
   - Give your service a name

4. **Configure Build and Start Commands**
   ```bash
   # Build Command
   pip install -r requirements.txt

   # Start Command
   gunicorn app:app
   ```

5. **Environment Variables**
   Add the following variables in Render's environment settings:
   ```
   PYTHON_VERSION=3.9.0
   FLASK_ENV=production
   ```

6. **Additional Settings**
   - Instance Type: Choose based on your needs (Free tier available)
   - Region: Select closest to your users
   - Branch: main (or your preferred branch)
   - Auto-Deploy: Enable if desired

7. **Health Check**
   - Path: `/`
   - Status Code: `200`

8. **Post-Deployment**
   - Verify the deployment by accessing your Render URL
   - Test the prediction functionality
   - Monitor the service logs for any issues

## Troubleshooting

Common issues and solutions:

1. **Model Not Found**
   - Ensure `model_training.py` has been run
   - Check paths in `config.ini`

2. **Import Errors**
   - Verify virtual environment is activated
   - Confirm all dependencies are installed

3. **Visualization Issues**
   - Check if `plots` directory exists
   - Ensure matplotlib is properly configured

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Scikit-learn for machine learning tools
- Flask for web framework
- Contributors and maintainers

## Version History

- 1.0.0: Initial release with basic clustering
- 1.1.0: Added synthetic data generation
- 1.2.0: Implemented web interface
