"""
Sales Data Analysis - Complete Python Implementation
=====================================================
Author: Expert Data Analyst
Date: 2025
Description: Comprehensive analysis of global sales data with visualizations
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set visualization style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

class SalesAnalyzer:
    """
    A comprehensive sales data analyzer class with advanced analytics capabilities
    """
    
    def __init__(self, filepath):
        """Initialize the analyzer with data file"""
        self.df = pd.read_csv(filepath)
        self._preprocess_data()
        
    def _preprocess_data(self):
        """Clean and prepare data for analysis"""
        # Convert date columns
        self.df['Order Date'] = pd.to_datetime(self.df['Order Date'])
        self.df['Ship Date'] = pd.to_datetime(self.df['Ship Date'])
        
        # Create derived features
        self.df['Shipping_Days'] = (self.df['Ship Date'] - self.df['Order Date']).dt.days
        self.df['Year'] = self.df['Order Date'].dt.year
        self.df['Month'] = self.df['Order Date'].dt.month
        self.df['Quarter'] = self.df['Order Date'].dt.quarter
        self.df['Profit_Margin'] = (self.df['Total Profit'] / self.df['Total Revenue']) * 100
        
        print("✓ Data preprocessing completed")
        print(f"  Dataset: {len(self.df)} records, {len(self.df.columns)} columns")
        
    def get_summary_statistics(self):
        """Generate comprehensive summary statistics"""
        summary = {
            'Total Records': len(self.df),
            'Date Range': f"{self.df['Order Date'].min().date()} to {self.df['Order Date'].max().date()}",
            'Total Revenue': f"${self.df['Total Revenue'].sum():,.2f}",
            'Total Profit': f"${self.df['Total Profit'].sum():,.2f}",
            'Average Profit Margin': f"{(self.df['Total Profit'].sum() / self.df['Total Revenue'].sum() * 100):.2f}%",
            'Average Order Value': f"${self.df['Total Revenue'].mean():,.2f}",
            'Total Units Sold': f"{self.df['Units Sold'].sum():,}",
            'Unique Products': self.df['Item Type'].nunique(),
            'Unique Countries': self.df['Country'].nunique(),
            'Unique Regions': self.df['Region'].nunique()
        }
        return summary
    
    def analyze_regional_performance(self):
        """Analyze performance across regions"""
        regional = self.df.groupby('Region').agg({
            'Total Revenue': 'sum',
            'Total Profit': 'sum',
            'Order ID': 'count',
            'Units Sold': 'sum',
            'Profit_Margin': 'mean'
        }).round(2)
        
        regional.columns = ['Revenue', 'Profit', 'Orders', 'Units', 'Avg_Margin_%']
        regional = regional.sort_values('Revenue', ascending=False)
        regional['Revenue_Share_%'] = (regional['Revenue'] / regional['Revenue'].sum() * 100).round(2)
        
        return regional
    
    def analyze_product_performance(self):
        """Analyze product category performance"""
        products = self.df.groupby('Item Type').agg({
            'Total Revenue': 'sum',
            'Total Profit': 'sum',
            'Units Sold': 'sum',
            'Order ID': 'count'
        }).round(2)
        
        products.columns = ['Revenue', 'Profit', 'Units', 'Orders']
        products['Profit_Margin_%'] = ((products['Profit'] / products['Revenue']) * 100).round(2)
        products['Avg_Order_Value'] = (products['Revenue'] / products['Orders']).round(2)
        products = products.sort_values('Revenue', ascending=False)
        
        return products
    
    def analyze_time_trends(self):
        """Analyze trends over time"""
        yearly = self.df.groupby('Year').agg({
            'Total Revenue': 'sum',
            'Total Profit': 'sum',
            'Order ID': 'count',
            'Profit_Margin': 'mean'
        }).round(2)
        
        yearly.columns = ['Revenue', 'Profit', 'Orders', 'Avg_Margin_%']
        yearly['YoY_Revenue_Growth_%'] = yearly['Revenue'].pct_change() * 100
        
        return yearly
    
    def analyze_shipping_performance(self):
        """Analyze shipping and logistics"""
        shipping = self.df.groupby('Order Priority')['Shipping_Days'].agg([
            'count', 'mean', 'median', 'min', 'max', 'std'
        ]).round(2)
        
        shipping.columns = ['Orders', 'Avg_Days', 'Median_Days', 'Min_Days', 'Max_Days', 'Std_Dev']
        
        return shipping
    
    def analyze_sales_channels(self):
        """Compare sales channel performance"""
        channels = self.df.groupby('Sales Channel').agg({
            'Total Revenue': 'sum',
            'Total Profit': 'sum',
            'Order ID': 'count',
            'Units Sold': 'sum'
        }).round(2)
        
        channels.columns = ['Revenue', 'Profit', 'Orders', 'Units']
        channels['Avg_Order_Value'] = (channels['Revenue'] / channels['Orders']).round(2)
        channels['Profit_Margin_%'] = ((channels['Profit'] / channels['Revenue']) * 100).round(2)
        
        return channels
    
    def get_top_countries(self, n=10):
        """Get top N countries by revenue"""
        countries = self.df.groupby('Country').agg({
            'Total Revenue': 'sum',
            'Total Profit': 'sum',
            'Order ID': 'count'
        }).round(2)
        
        countries.columns = ['Revenue', 'Profit', 'Orders']
        countries = countries.sort_values('Revenue', ascending=False).head(n)
        
        return countries
    
    def correlation_analysis(self):
        """Analyze correlations between numerical variables"""
        numerical_cols = ['Units Sold', 'Unit Price', 'Unit Cost', 
                         'Total Revenue', 'Total Cost', 'Total Profit', 
                         'Shipping_Days', 'Profit_Margin']
        
        correlation_matrix = self.df[numerical_cols].corr()
        
        return correlation_matrix
    
    def export_analysis_report(self, filename='analysis_report.txt'):
        """Export comprehensive analysis to text file"""
        with open(filename, 'w') as f:
            f.write("="*80 + "\n")
            f.write("COMPREHENSIVE SALES DATA ANALYSIS REPORT\n")
            f.write("="*80 + "\n\n")
            
            # Summary Statistics
            f.write("1. SUMMARY STATISTICS\n")
            f.write("-" * 80 + "\n")
            summary = self.get_summary_statistics()
            for key, value in summary.items():
                f.write(f"{key:.<50} {value}\n")
            f.write("\n")
            
            # Regional Performance
            f.write("2. REGIONAL PERFORMANCE\n")
            f.write("-" * 80 + "\n")
            f.write(self.analyze_regional_performance().to_string())
            f.write("\n\n")
            
            # Product Performance
            f.write("3. PRODUCT PERFORMANCE\n")
            f.write("-" * 80 + "\n")
            f.write(self.analyze_product_performance().to_string())
            f.write("\n\n")
            
            # Time Trends
            f.write("4. YEARLY TRENDS\n")
            f.write("-" * 80 + "\n")
            f.write(self.analyze_time_trends().to_string())
            f.write("\n\n")
            
            # Shipping Performance
            f.write("5. SHIPPING PERFORMANCE\n")
            f.write("-" * 80 + "\n")
            f.write(self.analyze_shipping_performance().to_string())
            f.write("\n\n")
            
            # Sales Channels
            f.write("6. SALES CHANNEL ANALYSIS\n")
            f.write("-" * 80 + "\n")
            f.write(self.analyze_sales_channels().to_string())
            f.write("\n\n")
            
            # Top Countries
            f.write("7. TOP 10 COUNTRIES\n")
            f.write("-" * 80 + "\n")
            f.write(self.get_top_countries(10).to_string())
            f.write("\n\n")
            
            f.write("="*80 + "\n")
            f.write("END OF REPORT\n")
            f.write("="*80 + "\n")
        
        print(f"✓ Analysis report exported to {filename}")


def main():
    """Main execution function"""
    print("\n" + "="*80)
    print("SALES DATA ANALYSIS - COMPREHENSIVE ANALYTICS")
    print("="*80 + "\n")
    
    # Initialize analyzer
    print("Loading and processing data...")
    analyzer = SalesAnalyzer('sales.csv')
    
    # Display summary statistics
    print("\n" + "="*80)
    print("SUMMARY STATISTICS")
    print("="*80)
    summary = analyzer.get_summary_statistics()
    for key, value in summary.items():
        print(f"{key:.<50} {value}")
    
    # Regional analysis
    print("\n" + "="*80)
    print("REGIONAL PERFORMANCE")
    print("="*80)
    print(analyzer.analyze_regional_performance())
    
    # Product analysis
    print("\n" + "="*80)
    print("PRODUCT PERFORMANCE (Top 5)")
    print("="*80)
    print(analyzer.analyze_product_performance().head())
    
    # Time trends
    print("\n" + "="*80)
    print("YEARLY TRENDS")
    print("="*80)
    print(analyzer.analyze_time_trends())
    
    # Shipping analysis
    print("\n" + "="*80)
    print("SHIPPING PERFORMANCE BY PRIORITY")
    print("="*80)
    print(analyzer.analyze_shipping_performance())
    
    # Sales channels
    print("\n" + "="*80)
    print("SALES CHANNEL COMPARISON")
    print("="*80)
    print(analyzer.analyze_sales_channels())
    
    # Export full report
    print("\n" + "="*80)
    analyzer.export_analysis_report('comprehensive_analysis_report.txt')
    print("="*80 + "\n")
    
    print("✓ Analysis completed successfully!")
    print("✓ All insights generated and saved")
    

if __name__ == "__main__":
    main()
