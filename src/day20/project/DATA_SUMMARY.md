# Customer Analytics Dataset - Data Summary

## Dataset Overview
- **File Name:** customer_analytics.csv
- **Total Records:** 257 customers
- **Total Features:** 14 attributes
- **Data Quality:** Excellent (99.97% complete)
- **Analysis Date:** February 2026

## Quick Statistics

| Metric | Value |
|--------|-------|
| Total Data Points | 3,598 |
| Missing Values | 1 (0.03%) |
| Duplicate Records | 0 |
| Memory Usage | ~0.28 MB |

## Feature Breakdown

### Numeric Features (9)
1. **CustomerID** - Range: 1001-1257
2. **Age** - Mean: 35.67 years, Range: 21-53
3. **AnnualIncome** - Mean: $62,162, Range: $35,501-$102,458
4. **SpendingScore** - Mean: 45.89/100, Range: 21-70
5. **YearsEmployed** - Mean: 13.16 years, Range: 1-33
6. **PurchaseFrequency** - Mean: 12.15, Range: 1-23
7. **OnlineVisitsPerMonth** - Mean: 14.56, Range: 3-29
8. **ReturnedItems** - Mean: 2.34, Range: 0-4
9. **LastPurchaseAmount** - Mean: $2,887, Range: $1,002-$4,974

### Categorical Features (5)
1. **Gender** 
   - Male: 47.86% (123)
   - Female: 52.14% (134)

2. **City** (5 cities)
   - Mumbai: 22.57% (58)
   - Bangalore: 21.40% (55)
   - Pune: 20.62% (53)
   - Hyderabad: 19.07% (49)
   - Delhi: 16.34% (42)

3. **Education** (3 levels)
   - Masters: 35.02% (90)
   - PhD: 33.07% (85)
   - Bachelors: 31.91% (82)

4. **MaritalStatus**
   - Single: 50.19% (129)
   - Married: 49.81% (128)

5. **PreferredDevice** (4 devices)
   - Desktop: 26.46% (68)
   - Mobile: 25.29% (65)
   - Tablet: 24.51% (63)
   - Laptop: 23.73% (61)

## Missing Data Analysis

| Column | Missing Count | Missing % | Handling |
|--------|--------------|-----------|----------|
| AnnualIncome | 1 | 0.39% | Imputed with median ($62,195) |
| All Others | 0 | 0.00% | Complete |

**Imputation Justification:** The missing income value was imputed using the median to preserve the customer record while maintaining data distribution. Median is preferred over mean for financial data as it's robust against outliers.

## Data Distribution Characteristics

### Numeric Distributions
- **Age:** Nearly uniform, slight concentration 30-45
- **Income:** Uniform, no clear concentration
- **Spending Score:** Uniform across 0-100 range
- **Purchase Frequency:** Right-skewed (more frequent buyers)
- **Online Visits:** Right-skewed
- **Years Employed:** Right-skewed (newer employees)

### Categorical Patterns
- **Gender:** Perfectly balanced (nearly 50-50)
- **City:** Fairly distributed across 5 cities
- **Education:** Equally distributed across 3 levels
- **Marital Status:** Perfectly balanced (50-50)
- **Device:** Fairly distributed across 4 options

## Correlation Insights

### Strong Relationships
- **YearsEmployed vs Age:** Strong positive (employees are older)
- Most other features show weak correlations
- Income and Spending Score are essentially independent

### Weak Relationships
- Income and SpendingScore: r ≈ 0.08 (virtually independent)
- Age and SpendingScore: r ≈ -0.15 (slightly negative)
- This indicates complex, non-linear relationships

## Data Quality Metrics

| Metric | Score |
|--------|-------|
| Completeness | 99.97% ✓ |
| Uniqueness | 100% ✓ |
| Validity | 100% ✓ |
| Consistency | 100% ✓ |
| **Overall Quality** | **Excellent** |

## Key Observations

✓ **Strengths:**
- Minimal missing data (only 1 value)
- No duplicate records
- Good feature diversity (numeric and categorical)
- Balanced categorical distributions
- Realistic value ranges

⚠️ **Considerations:**

- Age limited to working-age adults (21-53)
- Some features show weak inter-correlations
- Spending score is uniformly distributed (opportunity-focused)

## Business Context

**Customer Base Profile:**
- Mature, working-age customers (avg 35-36 years)
- Diverse income levels in middle-to-upper range
- Balanced gender representation
- Concentrated in major Indian metros
- Well-educated demographic (mostly Masters/PhD)

**Behavioral Characteristics:**
- Moderate purchase frequency (1-23 purchases)
- Active online engagement (3-29 monthly visits)
- Low return rates (0-4 items per customer)
- Average purchase amount ~$2,887
- Diverse device preferences

## Files Included in Analysis
1. MiniProject1_EDA.ipynb - Complete analysis notebook
2. eda_utils.py - Utility functions
3. DATA_SUMMARY.md - This file
4. EDA_ANALYSIS_REPORT.md - Detailed report
5. README.md - Project documentation
6. requirements.txt - Python dependencies
