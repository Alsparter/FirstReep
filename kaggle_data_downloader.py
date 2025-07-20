#!/usr/bin/env python3
"""
Kaggle HR Attrition Dataset Downloader
=====================================

This script helps download the HR attrition datasets from Kaggle.
Since direct download requires Kaggle API authentication, this script
provides instructions and alternative methods.

Author: AI Assistant
Date: 2025
"""

import os
import pandas as pd
import requests
from urllib.parse import urlparse
import zipfile

def setup_instructions():
    """Print setup instructions for Kaggle API"""
    print("🔧 KAGGLE API SETUP INSTRUCTIONS")
    print("=" * 50)
    print("\n1. Create a Kaggle Account:")
    print("   - Go to https://www.kaggle.com")
    print("   - Sign up or log in")
    
    print("\n2. Get API Credentials:")
    print("   - Go to https://www.kaggle.com/settings")
    print("   - Scroll down to 'API' section")
    print("   - Click 'Create New API Token'")
    print("   - Download the kaggle.json file")
    
    print("\n3. Install Kaggle API:")
    print("   pip install kaggle")
    
    print("\n4. Setup Credentials:")
    print("   - Linux/Mac: ~/.kaggle/kaggle.json")
    print("   - Windows: C:\\Users\\<username>\\.kaggle\\kaggle.json")
    print("   - Set permissions: chmod 600 ~/.kaggle/kaggle.json")
    
    print("\n5. Download Dataset:")
    print("   kaggle datasets download -d stealthtechnologies/employee-attrition-dataset")

def create_manual_download_guide():
    """Create a guide for manual download"""
    guide_content = """
# Manual Download Guide for HR Attrition Dataset

## Dataset Information
- **Source**: Kaggle - Stealth Technologies
- **Dataset**: Employee Attrition Dataset
- **Files**: train.csv, test.csv

## Step-by-Step Manual Download:

### Method 1: Direct Kaggle Download
1. Visit: https://www.kaggle.com/datasets/stealthtechnologies/employee-attrition-dataset
2. Click "Download" button (requires Kaggle account)
3. Extract the ZIP file to get train.csv and test.csv
4. Place both files in the same directory as your Python scripts

### Method 2: Using Kaggle API (Recommended)
```bash
# Install kaggle
pip install kaggle

# Download dataset
kaggle datasets download -d stealthtechnologies/employee-attrition-dataset

# Extract files
unzip employee-attrition-dataset.zip
```

### Method 3: Alternative Public Datasets
If the main dataset is not available, you can use these alternatives:
- IBM HR Analytics Employee Attrition & Performance
- Human Resources Analytics Case Study

## File Placement
After download, ensure these files are in your working directory:
- train.csv
- test.csv
- hr_attrition_analysis.py
- PowerBI_Dashboard_Guide.md

## Dataset Structure
Expected columns in the dataset:
- Employee demographics (Age, Gender, MaritalStatus)
- Job information (Department, JobRole, JobLevel)
- Compensation (MonthlyIncome, StockOptionLevel)
- Satisfaction metrics (JobSatisfaction, EnvironmentSatisfaction)
- Work conditions (OverTime, BusinessTravel, DistanceFromHome)
- Performance (PerformanceRating, TrainingTimesLastYear)
- Target variable (Attrition)

## Troubleshooting
- **Access Denied**: Ensure you're logged into Kaggle
- **File Not Found**: Check file names and paths
- **Permission Issues**: Verify API token permissions
- **Network Issues**: Try downloading via browser instead

## Next Steps
Once you have the files:
1. Run: python hr_attrition_analysis.py
2. Follow the PowerBI_Dashboard_Guide.md instructions
3. Import generated Excel files into Power BI
"""
    
    with open('Manual_Download_Guide.md', 'w') as f:
        f.write(guide_content)
    
    print("📖 Manual download guide created: Manual_Download_Guide.md")

def download_with_kaggle_api():
    """Attempt to download using Kaggle API"""
    try:
        import kaggle
        print("🔄 Attempting to download with Kaggle API...")
        
        # Download the dataset
        kaggle.api.dataset_download_files(
            'stealthtechnologies/employee-attrition-dataset',
            path='.',
            unzip=True
        )
        
        print("✅ Dataset downloaded successfully!")
        return True
        
    except ImportError:
        print("❌ Kaggle package not installed. Run: pip install kaggle")
        return False
    except Exception as e:
        print(f"❌ Download failed: {str(e)}")
        print("💡 Try manual download method")
        return False

def verify_dataset_files():
    """Verify that the required files exist"""
    required_files = ['train.csv', 'test.csv']
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        print("📥 Please download the files manually or use Kaggle API")
        return False
    else:
        print("✅ All required files found!")
        
        # Check file contents
        try:
            train_df = pd.read_csv('train.csv')
            test_df = pd.read_csv('test.csv')
            
            print(f"📊 Train dataset: {train_df.shape[0]} rows, {train_df.shape[1]} columns")
            print(f"📊 Test dataset: {test_df.shape[0]} rows, {test_df.shape[1]} columns")
            
            # Check for Attrition column
            if 'Attrition' in train_df.columns:
                attrition_rate = (train_df['Attrition'] == 'Yes').mean() * 100
                print(f"📈 Training set attrition rate: {attrition_rate:.1f}%")
            
            return True
            
        except Exception as e:
            print(f"❌ Error reading files: {str(e)}")
            return False

def create_sample_urls():
    """Create a file with alternative dataset URLs"""
    urls_content = """
# Alternative HR Attrition Datasets

## Primary Dataset
- Kaggle: https://www.kaggle.com/datasets/stealthtechnologies/employee-attrition-dataset

## Alternative Datasets (if primary is unavailable)
1. IBM HR Analytics Employee Attrition & Performance
   - URL: https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset
   - Features: 35 columns, 1470 employees
   - Similar structure to primary dataset

2. HR Analytics Case Study
   - URL: https://www.kaggle.com/datasets/giripujar/hr-analytics-case-study
   - Features: Multiple CSV files with comprehensive data
   - Includes satisfaction and performance metrics

3. Employee Attrition for Healthcare
   - URL: https://www.kaggle.com/datasets/jpmiller/employee-attrition-for-healthcare
   - Specialized for healthcare industry
   - Good for domain-specific analysis

## Manual Download Steps
1. Click on the dataset URL
2. Sign in to Kaggle
3. Click "Download" button
4. Extract ZIP file
5. Rename files to train.csv and test.csv if needed

## Data Format Requirements
The dataset should contain these key columns:
- Employee ID
- Age, Gender, MaritalStatus
- Department, JobRole
- MonthlyIncome
- JobSatisfaction, EnvironmentSatisfaction, WorkLifeBalance
- OverTime, BusinessTravel
- YearsAtCompany, YearsInCurrentRole
- PerformanceRating
- Attrition (target variable)
"""
    
    with open('Alternative_Dataset_URLs.md', 'w') as f:
        f.write(urls_content)
    
    print("🔗 Alternative dataset URLs created: Alternative_Dataset_URLs.md")

def main():
    """Main function to orchestrate the download process"""
    print("🚀 HR Attrition Dataset Downloader")
    print("=" * 40)
    
    # Check if files already exist
    if verify_dataset_files():
        print("📁 Dataset files already available!")
        print("▶️  You can now run: python hr_attrition_analysis.py")
        return
    
    print("\n🔍 Dataset files not found. Checking download options...")
    
    # Try Kaggle API download
    if not download_with_kaggle_api():
        print("\n📖 Creating download guides...")
        setup_instructions()
        create_manual_download_guide()
        create_sample_urls()
        
        print("\n" + "=" * 60)
        print("📋 NEXT STEPS:")
        print("1. Follow the setup instructions above")
        print("2. Download the dataset manually or via API")
        print("3. Place train.csv and test.csv in this directory")
        print("4. Run this script again to verify")
        print("5. Then run: python hr_attrition_analysis.py")
        print("=" * 60)

if __name__ == "__main__":
    main()