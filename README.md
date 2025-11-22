# AI-Driven Micro-Lending Risk Assessment Platform

This platform generates highly granular risk heatmaps at the district, block, and panchayat levels to support safer micro-lending decisions using machine learning clustering models and advanced analytics.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Generate Sample Data
```bash
python generate_sample_data.py
```

### 3. Launch Interactive Dashboard
```bash
streamlit run simple_dashboard.py
```

### 4. View Comprehensive Analysis
```bash
python demo.py
```

## 🎯 Features

- **Multi-level Geographic Analysis**: Risk assessment at district, block, and panchayat levels
- **Machine Learning Models**: Advanced clustering algorithms (K-Means, DBSCAN, Hierarchical)
- **Risk Scoring**: Comprehensive risk scoring based on multiple factors
- **Interactive Heatmaps**: Visual risk representation using interactive maps
- **Data Simulation**: Realistic transactional and demographic data generation
- **Web Dashboard**: Interactive Streamlit dashboard for visualization and analysis

## 📊 Platform Components

### Core Modules
- **Data Generation** (`src/data_generation/`): Creates synthetic micro-lending datasets
- **Risk Assessment** (`src/models/`): ML-based risk scoring and clustering
- **Visualization** (`src/visualization/`): Interactive charts and geographic heatmaps
- **Dashboard** (`dashboard/`): Real-time risk monitoring interface

### Risk Factors Analyzed
- **Demographic**: Age, income, education, occupation
- **Financial**: Credit history, existing loans, savings, expenses
- **Geographic**: Rainfall, crop yield, infrastructure, market access
- **Transactional**: Loan amount, repayment history, payment delays

## 🛠️ Technology Stack

- **Machine Learning**: scikit-learn, XGBoost, LightGBM, CatBoost
- **Data Processing**: Pandas, NumPy, GeoPandas
- **Visualization**: Plotly, Folium, Streamlit, Matplotlib, Seaborn
- **Geographic Analysis**: Geopy, Shapely for coordinate processing

## 📁 Project Structure

```
├── data/                    # Generated datasets
├── results/                 # Risk assessment outputs
├── visualizations/          # Generated charts and heatmaps
├── src/                     # Source code
│   ├── data_generation/     # Data simulation modules
│   ├── models/             # Machine learning models
│   ├── visualization/      # Visualization components
│   └── utils/              # Utility functions
├── dashboard/              # Streamlit dashboard
├── notebooks/              # Jupyter notebooks for analysis
├── config/                 # Configuration files
└── .vscode/                # VS Code tasks and settings
```

## 🎮 Available Commands

### VS Code Tasks (Ctrl+Shift+P → "Tasks: Run Task")
- **Generate Sample Data**: Create synthetic datasets
- **Run Simple Dashboard**: Launch basic Streamlit interface
- **Run Full Dashboard**: Launch comprehensive dashboard
- **Install Dependencies**: Install all required packages

### Command Line Options
```bash
# Generate sample data
python generate_sample_data.py

# Run comprehensive demo
python demo.py

# Launch simple dashboard
streamlit run simple_dashboard.py

# Launch full dashboard (requires complete data pipeline)
streamlit run dashboard/app.py

# Run data pipeline components
python main.py data      # Generate data only
python main.py models    # Train models only
python main.py viz       # Create visualizations only
python main.py full      # Run complete pipeline
```

## 📈 Sample Output

The platform generates:

- **500 synthetic borrowers** across 5 districts
- **Risk scores** from 0 (low risk) to 1 (high risk)
- **Geographic coordinates** for Tamil Nadu region
- **Administrative hierarchy** (District → Block → Panchayat)
- **Interactive visualizations** and heatmaps

### Key Metrics
- Average risk score calculation
- High-risk borrower identification (>0.7 risk score)
- Geographic risk distribution
- Demographic risk patterns
- Loan portfolio exposure analysis

## 🎯 Use Cases

1. **Micro-Finance Institutions**: Risk-based lending decisions
2. **Banks**: Rural and agricultural lending risk assessment
3. **Government Agencies**: Policy making for financial inclusion
4. **Researchers**: Study micro-lending patterns and risks
5. **Fintech Companies**: Geographic expansion planning

## 💡 Key Insights Generated

- **Risk Distribution**: Breakdown of borrowers by risk categories
- **Geographic Hotspots**: Districts with highest/lowest risk
- **Demographic Patterns**: Risk correlations with age, income, education
- **Portfolio Analysis**: Total exposure and risk concentration
- **Predictive Indicators**: Early warning signals for defaults

## 🔧 Customization

### Risk Factor Weights
Modify `config/settings.py` to adjust:
- Demographic factor weights
- Geographic risk parameters
- Financial risk thresholds
- Model hyperparameters

### Data Generation
Customize `src/data_generation/generate_data.py` for:
- Different geographic regions
- Custom borrower profiles
- Alternative risk factors
- Varying dataset sizes

## 📊 Dashboard Features

### Interactive Components
- **Risk Score Distribution**: Histograms and statistical summaries
- **Geographic Visualization**: Scatter plots with risk mapping
- **Administrative Analysis**: District-level comparisons
- **Data Filtering**: Dynamic filters by risk score and category
- **Real-time Metrics**: Key performance indicators

### Visualization Types
- Risk heatmaps on geographic maps
- Interactive scatter plots and histograms
- Correlation matrices and box plots
- Administrative level comparisons
- Time-series analysis (when applicable)

## 🚀 Next Steps & Enhancements

1. **Real Data Integration**: Connect to actual micro-lending databases
2. **Advanced ML Models**: Implement deep learning for risk prediction
3. **Real-time Updates**: Stream processing for live risk assessment
4. **Mobile Dashboard**: React Native or Flutter mobile app
5. **API Development**: RESTful APIs for third-party integration
6. **Alert Systems**: Automated notifications for high-risk scenarios

## 📝 License

MIT License - feel free to use and modify for your projects.

## 🤝 Contributing

Contributions welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.
