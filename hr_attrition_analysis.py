#!/usr/bin/env python3
"""
HR Attrition Data Analysis Script
=================================

This script processes HR attrition data from Kaggle and creates comprehensive
analysis ready for Power BI dashboard creation.

Author: AI Assistant
Date: 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class HRAttritionAnalyzer:
    def __init__(self):
        self.train_data = None
        self.test_data = None
        self.combined_data = None
        self.processed_data = None
        
    def load_datasets(self, train_path='train.csv', test_path='test.csv'):
        """Load the train and test datasets"""
        try:
            print("Loading datasets...")
            self.train_data = pd.read_csv(train_path)
            self.test_data = pd.read_csv(test_path)
            
            # Add source column to identify origin
            self.train_data['DataSource'] = 'Train'
            self.test_data['DataSource'] = 'Test'
            
            print(f"Train data shape: {self.train_data.shape}")
            print(f"Test data shape: {self.test_data.shape}")
            
            return True
        except FileNotFoundError as e:
            print(f"Error loading files: {e}")
            print("Please ensure train.csv and test.csv are in the current directory")
            return False
    
    def combine_datasets(self):
        """Combine train and test datasets"""
        if self.train_data is None or self.test_data is None:
            print("Please load datasets first")
            return False
            
        # Align columns between datasets
        train_cols = set(self.train_data.columns)
        test_cols = set(self.test_data.columns)
        
        # Find common columns
        common_cols = train_cols.intersection(test_cols)
        
        # Create combined dataset with common columns
        self.combined_data = pd.concat([
            self.train_data[list(common_cols)],
            self.test_data[list(common_cols)]
        ], ignore_index=True)
        
        print(f"Combined data shape: {self.combined_data.shape}")
        print(f"Common columns: {len(common_cols)}")
        
        return True
    
    def create_sample_data(self, n_samples=2000):
        """Create sample data if actual datasets are not available"""
        print("Creating sample HR attrition data...")
        
        np.random.seed(42)
        
        # Employee demographics and characteristics
        employee_ids = [f"EMP{str(i).zfill(6)}" for i in range(1, n_samples + 1)]
        
        ages = np.random.normal(35, 8, n_samples).astype(int)
        ages = np.clip(ages, 22, 65)
        
        genders = np.random.choice(['Male', 'Female'], n_samples, p=[0.55, 0.45])
        
        departments = np.random.choice([
            'Human Resources', 'Sales', 'Engineering', 'Marketing', 
            'Finance', 'Operations', 'IT', 'Customer Service'
        ], n_samples, p=[0.08, 0.25, 0.20, 0.12, 0.10, 0.08, 0.12, 0.05])
        
        job_roles = []
        for dept in departments:
            if dept == 'Engineering':
                role = np.random.choice(['Software Engineer', 'Senior Engineer', 'Lead Engineer', 'Architect'])
            elif dept == 'Sales':
                role = np.random.choice(['Sales Representative', 'Sales Manager', 'Account Manager', 'Sales Director'])
            elif dept == 'Human Resources':
                role = np.random.choice(['HR Specialist', 'HR Manager', 'HR Director', 'Recruiter'])
            elif dept == 'Marketing':
                role = np.random.choice(['Marketing Specialist', 'Marketing Manager', 'Brand Manager', 'Digital Marketer'])
            elif dept == 'Finance':
                role = np.random.choice(['Financial Analyst', 'Finance Manager', 'Accountant', 'CFO'])
            elif dept == 'Operations':
                role = np.random.choice(['Operations Manager', 'Process Analyst', 'Operations Director'])
            elif dept == 'IT':
                role = np.random.choice(['IT Support', 'System Administrator', 'IT Manager', 'DevOps Engineer'])
            else:
                role = np.random.choice(['Customer Service Rep', 'Customer Success Manager'])
            job_roles.append(role)
        
        # Education levels
        education_levels = np.random.choice([
            'High School', 'Bachelor', 'Master', 'PhD'
        ], n_samples, p=[0.15, 0.55, 0.25, 0.05])
        
        # Marital status
        marital_status = np.random.choice([
            'Single', 'Married', 'Divorced'
        ], n_samples, p=[0.35, 0.55, 0.10])
        
        # Years at company (influenced by age and attrition)
        years_at_company = np.random.exponential(4, n_samples)
        years_at_company = np.clip(years_at_company, 0.1, 20).round(1)
        
        # Years in current role
        years_in_role = years_at_company * np.random.uniform(0.3, 1.0, n_samples)
        years_in_role = np.clip(years_in_role, 0.1, years_at_company).round(1)
        
        # Years with current manager
        years_with_manager = years_in_role * np.random.uniform(0.2, 1.0, n_samples)
        years_with_manager = np.clip(years_with_manager, 0.1, years_in_role).round(1)
        
        # Monthly income (influenced by department, role, experience)
        base_salaries = {
            'Human Resources': 55000, 'Sales': 60000, 'Engineering': 80000,
            'Marketing': 65000, 'Finance': 70000, 'Operations': 58000,
            'IT': 75000, 'Customer Service': 45000
        }
        
        monthly_incomes = []
        for i in range(n_samples):
            base = base_salaries[departments[i]]
            experience_bonus = years_at_company[i] * 2000
            role_bonus = np.random.uniform(0.8, 1.4) * 1000
            monthly_income = (base + experience_bonus + role_bonus) / 12
            monthly_incomes.append(round(monthly_income))
        
        # Job satisfaction metrics (1-4 scale)
        job_satisfaction = np.random.choice([1, 2, 3, 4], n_samples, p=[0.10, 0.20, 0.45, 0.25])
        environment_satisfaction = np.random.choice([1, 2, 3, 4], n_samples, p=[0.08, 0.22, 0.50, 0.20])
        relationship_satisfaction = np.random.choice([1, 2, 3, 4], n_samples, p=[0.12, 0.18, 0.40, 0.30])
        
        # Work-life balance (1-4 scale)
        work_life_balance = np.random.choice([1, 2, 3, 4], n_samples, p=[0.15, 0.25, 0.40, 0.20])
        
        # Performance rating (1-4 scale)
        performance_rating = np.random.choice([1, 2, 3, 4], n_samples, p=[0.05, 0.15, 0.65, 0.15])
        
        # Distance from home
        distance_from_home = np.random.exponential(8, n_samples).astype(int)
        distance_from_home = np.clip(distance_from_home, 1, 50)
        
        # Business travel
        business_travel = np.random.choice([
            'Non-Travel', 'Travel_Rarely', 'Travel_Frequently'
        ], n_samples, p=[0.30, 0.55, 0.15])
        
        # Overtime
        overtime = np.random.choice(['Yes', 'No'], n_samples, p=[0.35, 0.65])
        
        # Training times last year
        training_times = np.random.poisson(3, n_samples)
        training_times = np.clip(training_times, 0, 10)
        
        # Stock option level
        stock_option = np.random.choice([0, 1, 2, 3], n_samples, p=[0.40, 0.35, 0.15, 0.10])
        
        # Number of companies worked
        num_companies_worked = np.random.poisson(2, n_samples)
        num_companies_worked = np.clip(num_companies_worked, 1, 8)
        
        # Calculate attrition probability based on multiple factors
        attrition_prob = (
            (job_satisfaction == 1) * 0.4 +
            (environment_satisfaction == 1) * 0.3 +
            (work_life_balance == 1) * 0.35 +
            (overtime == 'Yes') * 0.25 +
            (distance_from_home > 20) * 0.15 +
            (business_travel == 'Travel_Frequently') * 0.20 +
            (years_at_company < 2) * 0.30 +
            (monthly_incomes < np.percentile(monthly_incomes, 25)) * 0.25 +
            (training_times == 0) * 0.20
        )
        
        # Normalize probability
        attrition_prob = np.clip(attrition_prob / 3, 0.05, 0.80)
        
        # Generate attrition status
        attrition = np.random.binomial(1, attrition_prob, n_samples)
        attrition_text = ['No' if x == 0 else 'Yes' for x in attrition]
        
        # Create the dataset
        self.combined_data = pd.DataFrame({
            'EmployeeID': employee_ids,
            'Age': ages,
            'Gender': genders,
            'Department': departments,
            'JobRole': job_roles,
            'EducationLevel': education_levels,
            'MaritalStatus': marital_status,
            'YearsAtCompany': years_at_company,
            'YearsInCurrentRole': years_in_role,
            'YearsWithCurrManager': years_with_manager,
            'MonthlyIncome': monthly_incomes,
            'JobSatisfaction': job_satisfaction,
            'EnvironmentSatisfaction': environment_satisfaction,
            'RelationshipSatisfaction': relationship_satisfaction,
            'WorkLifeBalance': work_life_balance,
            'PerformanceRating': performance_rating,
            'DistanceFromHome': distance_from_home,
            'BusinessTravel': business_travel,
            'OverTime': overtime,
            'TrainingTimesLastYear': training_times,
            'StockOptionLevel': stock_option,
            'NumCompaniesWorked': num_companies_worked,
            'Attrition': attrition_text,
            'DataSource': np.random.choice(['Train', 'Test'], n_samples, p=[0.7, 0.3])
        })
        
        print(f"Sample data created with {n_samples} records")
        print(f"Attrition rate: {(attrition.sum() / n_samples) * 100:.1f}%")
        
        return True
    
    def process_data_for_powerbi(self):
        """Process data specifically for Power BI dashboard creation"""
        if self.combined_data is None:
            print("No data available for processing")
            return False
            
        print("Processing data for Power BI...")
        
        # Create a copy for processing
        df = self.combined_data.copy()
        
        # Create additional calculated columns for dashboard insights
        
        # Age groups
        df['AgeGroup'] = pd.cut(df['Age'], 
                               bins=[0, 25, 35, 45, 55, 100], 
                               labels=['Under 25', '25-34', '35-44', '45-54', '55+'])
        
        # Tenure groups
        df['TenureGroup'] = pd.cut(df['YearsAtCompany'], 
                                  bins=[0, 1, 3, 5, 10, 100], 
                                  labels=['<1 Year', '1-3 Years', '3-5 Years', '5-10 Years', '10+ Years'])
        
        # Salary groups
        salary_quartiles = df['MonthlyIncome'].quantile([0.25, 0.5, 0.75])
        df['SalaryGroup'] = pd.cut(df['MonthlyIncome'], 
                                  bins=[0, salary_quartiles[0.25], salary_quartiles[0.5], 
                                        salary_quartiles[0.75], float('inf')],
                                  labels=['Low', 'Medium-Low', 'Medium-High', 'High'])
        
        # Performance categories
        performance_map = {1: 'Poor', 2: 'Below Average', 3: 'Good', 4: 'Excellent'}
        df['PerformanceCategory'] = df['PerformanceRating'].map(performance_map)
        
        # Satisfaction levels
        satisfaction_map = {1: 'Low', 2: 'Medium', 3: 'High', 4: 'Very High'}
        df['JobSatisfactionLevel'] = df['JobSatisfaction'].map(satisfaction_map)
        df['EnvironmentSatisfactionLevel'] = df['EnvironmentSatisfaction'].map(satisfaction_map)
        df['WorkLifeBalanceLevel'] = df['WorkLifeBalance'].map(satisfaction_map)
        
        # Risk scoring for retention
        df['RetentionRisk'] = 'Low'
        
        # High risk conditions
        high_risk = (
            (df['JobSatisfaction'] <= 2) |
            (df['EnvironmentSatisfaction'] <= 2) |
            (df['WorkLifeBalance'] <= 2) |
            (df['OverTime'] == 'Yes') & (df['JobSatisfaction'] <= 3)
        )
        
        # Medium risk conditions
        medium_risk = (
            (df['JobSatisfaction'] == 3) & (df['YearsAtCompany'] < 2) |
            (df['DistanceFromHome'] > 15) & (df['BusinessTravel'] == 'Travel_Frequently') |
            (df['TrainingTimesLastYear'] == 0)
        )
        
        df.loc[medium_risk & ~high_risk, 'RetentionRisk'] = 'Medium'
        df.loc[high_risk, 'RetentionRisk'] = 'High'
        
        # Employee value score (for retention prioritization)
        df['EmployeeValueScore'] = (
            df['PerformanceRating'] * 25 +
            df['YearsAtCompany'] * 5 +
            (df['MonthlyIncome'] / 1000) * 2 +
            df['TrainingTimesLastYear'] * 3
        ).round(0)
        
        # Create calendar date fields for time series analysis
        base_date = datetime(2024, 1, 1)
        df['HireDate'] = [base_date - timedelta(days=int(years * 365)) 
                         for years in df['YearsAtCompany']]
        df['HireYear'] = df['HireDate'].dt.year
        df['HireMonth'] = df['HireDate'].dt.month
        df['HireQuarter'] = df['HireDate'].dt.quarter
        
        # Create binary flags for easier filtering in Power BI
        df['IsHighPerformer'] = (df['PerformanceRating'] >= 4).astype(int)
        df['IsNewEmployee'] = (df['YearsAtCompany'] <= 1).astype(int)
        df['IsOvertime'] = (df['OverTime'] == 'Yes').astype(int)
        df['IsFrequentTraveler'] = (df['BusinessTravel'] == 'Travel_Frequently').astype(int)
        df['IsHighDistance'] = (df['DistanceFromHome'] > 20).astype(int)
        df['IsAttrition'] = (df['Attrition'] == 'Yes').astype(int)
        
        self.processed_data = df
        print("Data processing completed!")
        
        return True
    
    def create_powerbi_datasets(self):
        """Create specific datasets for Power BI pages"""
        if self.processed_data is None:
            print("Please process data first")
            return False
            
        print("Creating Power BI specific datasets...")
        
        # Page 1: Why Employees Leave (Attrition Analysis)
        attrition_data = self.processed_data[self.processed_data['Attrition'] == 'Yes'].copy()
        
        # Page 2: Why Employees Stay (Retention Analysis)
        retention_data = self.processed_data[self.processed_data['Attrition'] == 'No'].copy()
        
        # Main dashboard dataset
        dashboard_data = self.processed_data.copy()
        
        # Summary statistics for KPIs
        total_employees = len(dashboard_data)
        attrition_count = len(attrition_data)
        attrition_rate = (attrition_count / total_employees) * 100
        avg_tenure = dashboard_data['YearsAtCompany'].mean()
        avg_satisfaction = dashboard_data['JobSatisfaction'].mean()
        
        summary_stats = pd.DataFrame({
            'Metric': ['Total Employees', 'Attrition Count', 'Attrition Rate (%)', 
                      'Average Tenure (Years)', 'Average Job Satisfaction'],
            'Value': [total_employees, attrition_count, round(attrition_rate, 1), 
                     round(avg_tenure, 1), round(avg_satisfaction, 1)]
        })
        
        # Save datasets
        try:
            dashboard_data.to_excel('HR_Dashboard_Main_Data.xlsx', index=False)
            attrition_data.to_excel('HR_Attrition_Analysis.xlsx', index=False)
            retention_data.to_excel('HR_Retention_Analysis.xlsx', index=False)
            summary_stats.to_excel('HR_Summary_KPIs.xlsx', index=False)
            
            # Also save as CSV for compatibility
            dashboard_data.to_csv('HR_Dashboard_Main_Data.csv', index=False)
            attrition_data.to_csv('HR_Attrition_Analysis.csv', index=False)
            retention_data.to_csv('HR_Retention_Analysis.csv', index=False)
            summary_stats.to_csv('HR_Summary_KPIs.csv', index=False)
            
            print("✅ Power BI datasets created successfully!")
            print(f"   - Main Dashboard Data: {len(dashboard_data)} records")
            print(f"   - Attrition Analysis: {len(attrition_data)} records")
            print(f"   - Retention Analysis: {len(retention_data)} records")
            print(f"   - Summary KPIs: {len(summary_stats)} metrics")
            
        except Exception as e:
            print(f"Error saving files: {e}")
            return False
            
        return True
    
    def generate_insights_report(self):
        """Generate key insights for dashboard creation"""
        if self.processed_data is None:
            print("Please process data first")
            return False
            
        print("\n" + "="*60)
        print("HR ATTRITION INSIGHTS REPORT")
        print("="*60)
        
        df = self.processed_data
        
        # Overall statistics
        print(f"\n📊 OVERALL STATISTICS:")
        print(f"Total Employees: {len(df):,}")
        print(f"Attrition Rate: {(df['Attrition'] == 'Yes').mean() * 100:.1f}%")
        print(f"Average Tenure: {df['YearsAtCompany'].mean():.1f} years")
        print(f"Average Monthly Income: ${df['MonthlyIncome'].mean():,.0f}")
        
        # Department analysis
        print(f"\n🏢 DEPARTMENT ANALYSIS:")
        dept_attrition = df.groupby('Department').agg({
            'Attrition': lambda x: (x == 'Yes').mean() * 100,
            'EmployeeID': 'count'
        }).round(1)
        dept_attrition.columns = ['Attrition_Rate_%', 'Employee_Count']
        dept_attrition = dept_attrition.sort_values('Attrition_Rate_%', ascending=False)
        print(dept_attrition.to_string())
        
        # Age group analysis
        print(f"\n👥 AGE GROUP ANALYSIS:")
        age_attrition = df.groupby('AgeGroup').agg({
            'Attrition': lambda x: (x == 'Yes').mean() * 100,
            'EmployeeID': 'count'
        }).round(1)
        age_attrition.columns = ['Attrition_Rate_%', 'Employee_Count']
        print(age_attrition.to_string())
        
        # Satisfaction impact
        print(f"\n😊 SATISFACTION IMPACT:")
        satisfaction_cols = ['JobSatisfaction', 'EnvironmentSatisfaction', 'WorkLifeBalance']
        for col in satisfaction_cols:
            avg_satisfied = df[df['Attrition'] == 'No'][col].mean()
            avg_attrited = df[df['Attrition'] == 'Yes'][col].mean()
            print(f"{col}: Stayed={avg_satisfied:.1f}, Left={avg_attrited:.1f}")
        
        # Key risk factors
        print(f"\n⚠️  KEY RISK FACTORS FOR ATTRITION:")
        risk_factors = {
            'Overtime (Yes)': df[df['OverTime'] == 'Yes']['Attrition'].value_counts(normalize=True)['Yes'] * 100,
            'Low Job Satisfaction (1-2)': df[df['JobSatisfaction'] <= 2]['Attrition'].value_counts(normalize=True)['Yes'] * 100,
            'Frequent Travel': df[df['BusinessTravel'] == 'Travel_Frequently']['Attrition'].value_counts(normalize=True)['Yes'] * 100,
            'High Distance (>20km)': df[df['DistanceFromHome'] > 20]['Attrition'].value_counts(normalize=True)['Yes'] * 100,
            'New Employees (<1 year)': df[df['YearsAtCompany'] < 1]['Attrition'].value_counts(normalize=True)['Yes'] * 100,
        }
        
        for factor, rate in sorted(risk_factors.items(), key=lambda x: x[1], reverse=True):
            print(f"{factor}: {rate:.1f}% attrition rate")
        
        # Retention factors
        print(f"\n✅ RETENTION FACTORS:")
        retained = df[df['Attrition'] == 'No']
        print(f"High Performers Retained: {(retained['PerformanceRating'] >= 4).mean() * 100:.1f}%")
        print(f"Stock Options Help: {retained['StockOptionLevel'].mean():.1f} avg level")
        print(f"Training Impact: {retained['TrainingTimesLastYear'].mean():.1f} avg sessions")
        
        print(f"\n📋 RECOMMENDATIONS FOR POWER BI DASHBOARD:")
        print("1. Create KPI cards for: Total Employees, Attrition Rate, Avg Tenure")
        print("2. Add filters for: Department, Age Group, Performance, Tenure")
        print("3. Page 1 (Why Leave): Focus on satisfaction scores, overtime, travel")
        print("4. Page 2 (Why Stay): Highlight performance, stock options, training")
        print("5. Use risk scoring to prioritize retention efforts")
        print("6. Include trend analysis by hire date and department")
        
        # Save insights to file
        with open('HR_Attrition_Insights.txt', 'w') as f:
            f.write("HR ATTRITION INSIGHTS REPORT\n")
            f.write("="*60 + "\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("Key Findings:\n")
            f.write(f"- Total Employees: {len(df):,}\n")
            f.write(f"- Overall Attrition Rate: {(df['Attrition'] == 'Yes').mean() * 100:.1f}%\n")
            f.write(f"- Highest Risk Department: {dept_attrition.index[0]} ({dept_attrition.iloc[0]['Attrition_Rate_%']:.1f}%)\n")
            f.write(f"- Most Critical Age Group: {age_attrition.index[0]} ({age_attrition.iloc[0]['Attrition_Rate_%']:.1f}%)\n")
        
        return True
    
    def run_full_analysis(self):
        """Run the complete analysis pipeline"""
        print("🚀 Starting HR Attrition Analysis...")
        
        # Try to load actual datasets first
        if not self.load_datasets():
            print("📝 Creating sample data for demonstration...")
            self.create_sample_data()
        else:
            self.combine_datasets()
        
        # Process data
        self.process_data_for_powerbi()
        
        # Create Power BI datasets
        self.create_powerbi_datasets()
        
        # Generate insights
        self.generate_insights_report()
        
        print("\n🎉 Analysis completed successfully!")
        print("📁 Files created for Power BI:")
        print("   - HR_Dashboard_Main_Data.xlsx")
        print("   - HR_Attrition_Analysis.xlsx") 
        print("   - HR_Retention_Analysis.xlsx")
        print("   - HR_Summary_KPIs.xlsx")
        print("   - HR_Attrition_Insights.txt")

if __name__ == "__main__":
    # Initialize analyzer
    analyzer = HRAttritionAnalyzer()
    
    # Run complete analysis
    analyzer.run_full_analysis()