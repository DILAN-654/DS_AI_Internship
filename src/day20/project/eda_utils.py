"""
Utility functions for Exploratory Data Analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Tuple


def get_missing_values_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate a summary of missing values in the dataset.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe to analyze
    
    Returns:
    --------
    pd.DataFrame
        Summary with column names, missing counts, percentages, and types
    """
    missing_data = pd.DataFrame({
        'Column': df.columns,
        'Missing_Count': df.isnull().sum().values,
        'Missing_Percentage': (df.isnull().sum().values / len(df) * 100).round(2),
        'Data_Type': df.dtypes.values
    })
    return missing_data[missing_data['Missing_Count'] > 0].sort_values('Missing_Percentage', ascending=False)


def get_data_quality_report(df: pd.DataFrame) -> dict:
    """
    Generate a comprehensive data quality report.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe to analyze
    
    Returns:
    --------
    dict
        Dictionary containing various quality metrics
    """
    report = {
        'Total_Records': len(df),
        'Total_Columns': len(df.columns),
        'Duplicate_Rows': df.duplicated().sum(),
        'Total_Missing': df.isnull().sum().sum(),
        'Missing_Percentage': (df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100),
        'Memory_Usage_MB': df.memory_usage(deep=True).sum() / 1024**2
    }
    return report


def visualize_missing_data(df: pd.DataFrame, figsize: Tuple[int, int] = (12, 6)) -> None:
    """
    Create visualization of missing data patterns.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe to analyze
    figsize : Tuple[int, int]
        Figure size for the plot
    """
    missing_data = get_missing_values_summary(df)
    
    if len(missing_data) == 0:
        print("No missing values found in the dataset!")
        return
    
    fig, ax = plt.subplots(figsize=figsize)
    missing_data.sort_values('Missing_Percentage').plot(
        kind='barh',
        x='Column',
        y='Missing_Percentage',
        ax=ax,
        legend=False,
        color='coral'
    )
    ax.set_xlabel('Missing Percentage (%)')
    ax.set_ylabel('Columns')
    ax.set_title('Missing Data Distribution Across Columns')
    plt.tight_layout()
    plt.show()


def get_numeric_columns(df: pd.DataFrame) -> list:
    """Get all numeric columns."""
    return df.select_dtypes(include=[np.number]).columns.tolist()


def get_categorical_columns(df: pd.DataFrame) -> list:
    """Get all categorical columns."""
    return df.select_dtypes(include=['object']).columns.tolist()


def get_statistical_summary(df: pd.DataFrame, include_all: bool = False) -> pd.DataFrame:
    """
    Get enhanced statistical summary with additional metrics.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    include_all : bool
        If True, includes categorical columns in summary
    
    Returns:
    --------
    pd.DataFrame
        Enhanced statistical summary
    """
    return df.describe(include='all' if include_all else None).T


def plot_distribution(data, title: str, bins: int = 30, figsize: Tuple[int, int] = (10, 5)) -> None:
    """
    Create a histogram with KDE overlay for distribution visualization.
    
    Parameters:
    -----------
    data : pd.Series
        Data to visualize
    title : str
        Title for the plot
    bins : int
        Number of bins for histogram
    figsize : Tuple[int, int]
        Figure size
    """
    fig, ax = plt.subplots(figsize=figsize)
    ax.hist(data.dropna(), bins=bins, color='skyblue', edgecolor='black', alpha=0.7)
    ax2 = ax.twinx()
    data.dropna().plot(kind='kde', ax=ax2, color='red', linewidth=2)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel('Value')
    ax.set_ylabel('Frequency')
    ax2.set_ylabel('Density')
    plt.tight_layout()
    plt.show()


def plot_categorical(data, title: str, figsize: Tuple[int, int] = (10, 5)) -> None:
    """
    Create a bar chart for categorical data.
    
    Parameters:
    -----------
    data : pd.Series
        Categorical data to visualize
    title : str
        Title for the plot
    figsize : Tuple[int, int]
        Figure size
    """
    fig, ax = plt.subplots(figsize=figsize)
    data.value_counts().plot(kind='bar', ax=ax, color='lightgreen', edgecolor='black')
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel('Category')
    ax.set_ylabel('Count')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


def detect_outliers_iqr(data: pd.Series) -> Tuple[int, list]:
    """
    Detect outliers using IQR method.
    
    Parameters:
    -----------
    data : pd.Series
        Data to analyze
    
    Returns:
    --------
    Tuple[int, list]
        Number of outliers and their indices
    """
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outlier_indices = data[(data < lower_bound) | (data > upper_bound)].index.tolist()
    return len(outlier_indices), outlier_indices


def create_correlation_insights(corr_matrix: pd.DataFrame, top_n: int = 5) -> dict:
    """
    Extract key correlation insights from correlation matrix.
    
    Parameters:
    -----------
    corr_matrix : pd.DataFrame
        Correlation matrix
    top_n : int
        Number of top correlations to extract
    
    Returns:
    --------
    dict
        Dictionary containing positive and negative correlations
    """
    # Get correlations excluding self-correlations
    corr_pairs = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            corr_pairs.append({
                'Feature_1': corr_matrix.columns[i],
                'Feature_2': corr_matrix.columns[j],
                'Correlation': corr_matrix.iloc[i, j]
            })
    
    corr_df = pd.DataFrame(corr_pairs)
    
    return {
        'Strong_Positive': corr_df.nlargest(top_n, 'Correlation').to_dict('records'),
        'Strong_Negative': corr_df.nsmallest(top_n, 'Correlation').to_dict('records')
    }
