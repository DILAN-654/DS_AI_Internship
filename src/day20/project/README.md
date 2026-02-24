# Customer Analytics - EDA Mini Project

## Project Overview
This project performs a comprehensive Exploratory Data Analysis (EDA) on customer analytics data from various Indian cities. The analysis follows a systematic 4-phase approach to understand customer behavior, demographics, and purchasing patterns.

## Dataset Information
- **File**: `customer_analytics.csv`
- **Records**: 257 customers
- **Features**: 14 attributes including demographics, behavioral metrics, and purchase information
- **Focus**: Understanding customer segments and their purchasing behaviors

## Project Structure

```
project/
├── MiniProject1_EDA.ipynb          # Main analysis notebook
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── DATA_SUMMARY.md                 # Initial data exploration findings
├── EDA_ANALYSIS_REPORT.md          # Detailed analysis report
└── eda_utils.py                    # Utility functions for EDA
```

## Analysis Phases

### Phase 1: The Detective Work (Setup & Inspection)
- Load and inspect the dataset
- Examine shape, data types, and basic statistics
- Document initial observations

### Phase 2: The Cleanup (Data Preprocessing)
- Identify missing values
- Handle missing data through imputation or deletion
- Detect and remove duplicates
- Document all cleaning decisions

### Phase 3: The Deep Dive (Univariate & Bivariate Analysis)
- Create univariate visualizations (histograms, bar charts)
- Explore bivariate relationships (scatter plots, boxplots)
- Interpret patterns and distributions

### Phase 4: The Big Picture (Multivariate & Storytelling)
- Generate correlation matrix heatmap
- Identify multi-variable relationships
- Provide executive summary with top 3 insights

## Key Features Analyzed
- **Demographics**: Age, Gender, Education, Marital Status, City
- **Financial**: Annual Income, Spending Score
- **Behavioral**: Purchase Frequency, Online Visits, Returned Items
- **Transactional**: Last Purchase Amount, Preferred Device
- **Employment**: Years Employed

## How to Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Launch Jupyter Notebook:
   ```bash
   jupyter notebook MiniProject1_EDA.ipynb
   ```

3. Run all cells from top to bottom (Kernel → Restart & Run All)

## Key Deliverables
- Comprehensive Jupyter Notebook with code, markdown explanations, and visualizations
- Data quality assessment and cleaning justifications
- Statistical distributions and relationships visualization
- Executive summary with actionable insights
- Utility functions for reproducible analysis

## Dependencies
- pandas: Data manipulation and analysis
- numpy: Numerical computations
- matplotlib: Static visualizations
- seaborn: Statistical data visualizations
- plotly: Interactive visualizations
- jupyter: Notebook interface

## Author Notes
This project demonstrates professional EDA practices including:
- Clear documentation and markdown explanations
- Rigorous data validation and cleaning
- Comprehensive visualization suite
- Data-driven insights and narrative storytelling
