import pandas as pd
import os
import numpy as np
from datetime import datetime, timedelta
import time
from utils.database import (
    load_all_data_from_db, create_tables, import_data_from_csv, 
    is_database_initialized, get_session
)

def load_all_data():
    """Load all department data and return as a dictionary"""
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    # Create data files if they don't exist
    create_dummy_data_files()
    
    # Try to connect to database with retries
    db_available = False
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # Try to get a database session
            session = get_session()
            if session:
                session.close()
                db_available = True
                break
        except Exception as e:
            print(f"Database connection attempt {attempt+1} failed: {e}")
            time.sleep(1)  # Wait a second before retrying
    
    # If database is available, try to use it
    if db_available:
        try:
            # Ensure database tables exist
            create_tables()
            
            # Check if database has been initialized with data
            if not is_database_initialized():
                # Import CSV data to database
                import_success = import_data_from_csv()
                if not import_success:
                    print("Data import to database failed, using CSV files")
                    return load_from_csv_files()
            
            # Load data from database
            data = load_all_data_from_db()
            
            # If we got data from the database, return it
            if data:
                print("Data loaded from database successfully")
                return data
        except Exception as e:
            print(f"Error using database: {e}")
    
    # Fallback to CSV files
    print("Using CSV files for data")
    return load_from_csv_files()

def load_from_csv_files():
    """Load data from CSV files as a fallback"""
    data = {}
    
    # Load data from CSV files
    data['finance'] = pd.read_csv('data/finance_data.csv')
    data['hr'] = pd.read_csv('data/hr_data.csv')
    data['payments'] = pd.read_csv('data/payments_data.csv')
    data['engineering'] = pd.read_csv('data/engineering_data.csv')
    data['strategy'] = pd.read_csv('data/strategy_data.csv')
    
    return data

def create_dummy_data_files():
    """Create dummy data files if they don't exist"""
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Create Finance data
    if not os.path.exists('data/finance_data.csv'):
        create_finance_data()
    
    # Create HR data
    if not os.path.exists('data/hr_data.csv'):
        create_hr_data()
    
    # Create Payments data
    if not os.path.exists('data/payments_data.csv'):
        create_payments_data()
    
    # Create Engineering data
    if not os.path.exists('data/engineering_data.csv'):
        create_engineering_data()
    
    # Create Strategy data
    if not os.path.exists('data/strategy_data.csv'):
        create_strategy_data()

def create_finance_data():
    """Create finance department dummy data"""
    # Generate dates for the last 30 days
    dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(30)]
    
    # Currencies and countries
    currencies = ['USD', 'EUR', 'GBP', 'NGN', 'GHS', 'KES']
    countries = ['Nigeria', 'Ghana', 'Kenya', 'South Africa', 'USA', 'UK']
    
    # Generate data
    data = []
    for date in dates:
        for currency in currencies:
            # FX Rate fluctuation logic
            base_rate = 1.0 if currency == 'USD' else np.random.uniform(0.5, 2.0) if currency in ['EUR', 'GBP'] else np.random.uniform(300, 800)
            daily_fluctuation = np.random.uniform(-0.05, 0.05)
            fx_rate = base_rate * (1 + daily_fluctuation)
            
            # Exposure amounts
            exposure = np.random.uniform(10000, 1000000)
            inflow = np.random.uniform(5000, 500000)
            outflow = np.random.uniform(5000, 400000)
            
            data.append({
                'Date': date,
                'Currency': currency,
                'FX_Rate': fx_rate,
                'Exposure': exposure,
                'Inflow': inflow,
                'Outflow': outflow,
                'Net_Position': inflow - outflow,
                'Country': np.random.choice(countries)
            })
    
    # Create DataFrame and save to CSV
    df = pd.DataFrame(data)
    df.to_csv('data/finance_data.csv', index=False)

def create_hr_data():
    """Create HR department dummy data"""
    # Generate dates for the last 12 months
    months = [(datetime.now() - timedelta(days=30*i)).strftime('%Y-%m') for i in range(12)]
    
    # Departments and locations
    departments = ['Engineering', 'Product', 'Finance', 'Operations', 'Marketing', 'HR', 'Legal']
    locations = ['Lagos', 'Accra', 'Nairobi', 'Remote', 'London', 'New York']
    
    # Generate data
    data = []
    for month in months:
        for dept in departments:
            # Headcount and turnover
            headcount = np.random.randint(5, 50)
            hires = np.random.randint(0, 5)
            terminations = np.random.randint(0, 3)
            leave_days = np.random.randint(0, headcount * 2)
            sick_days = np.random.randint(0, headcount)
            
            data.append({
                'Month': month,
                'Department': dept,
                'Headcount': headcount,
                'New_Hires': hires,
                'Terminations': terminations,
                'Turnover_Rate': (terminations / headcount) if headcount > 0 else 0,
                'Avg_Leave_Days': leave_days / headcount if headcount > 0 else 0,
                'Sick_Days': sick_days,
                'Location': np.random.choice(locations),
                'Avg_Onboarding_Days': np.random.randint(5, 30)
            })
    
    # Create DataFrame and save to CSV
    df = pd.DataFrame(data)
    df.to_csv('data/hr_data.csv', index=False)

def create_payments_data():
    """Create Payments/Ops department dummy data"""
    # Generate dates for the last 30 days
    dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(30)]
    
    # Payment channels and countries
    channels = ['Bank Transfer', 'Card', 'Mobile Money', 'Crypto', 'Cash Pickup']
    countries = ['Nigeria', 'Ghana', 'Kenya', 'South Africa', 'USA', 'UK']
    error_types = ['Authentication Failure', 'Network Error', 'Insufficient Funds', 'Bank Rejection', 'Timeout']
    
    # Generate data
    data = []
    for date in dates:
        for channel in channels:
            for country in countries:
                # Transaction metrics
                volume = np.random.randint(100, 10000)
                success_rate = np.random.uniform(0.85, 0.99)
                successful = int(volume * success_rate)
                failed = volume - successful
                
                # Error distribution if there are failures
                if failed > 0:
                    error_type = np.random.choice(error_types)
                else:
                    error_type = 'None'
                
                data.append({
                    'Date': date,
                    'Channel': channel,
                    'Country': country,
                    'Transaction_Volume': volume,
                    'Successful_Transactions': successful,
                    'Failed_Transactions': failed,
                    'Success_Rate': success_rate,
                    'Avg_Processing_Time_Sec': np.random.uniform(1, 10),
                    'Retry_Count': np.random.randint(0, int(failed * 0.5)),
                    'Primary_Error': error_type
                })
    
    # Create DataFrame and save to CSV
    df = pd.DataFrame(data)
    df.to_csv('data/payments_data.csv', index=False)

def create_engineering_data():
    """Create Engineering department dummy data"""
    # Generate hours for the last 72 hours (3 days) with hourly data
    hours = [(datetime.now() - timedelta(hours=i)).strftime('%Y-%m-%d %H:00:00') for i in range(72)]
    
    # Services and metrics
    services = ['Payment Gateway', 'User Auth', 'Account Service', 'Notification Service', 'API Gateway']
    environments = ['Production', 'Staging', 'Development']
    alert_types = ['High CPU', 'Memory Leak', 'API Latency', 'Database Connection', 'Service Unavailable']
    
    # Generate data
    data = []
    for hour in hours:
        for service in services:
            for env in environments:
                # Performance metrics
                cpu_usage = np.random.uniform(10, 90)
                memory_usage = np.random.uniform(20, 85)
                latency = np.random.uniform(10, 500)
                throughput = np.random.uniform(100, 5000)
                
                # Error rate logic - higher when CPU or memory is high
                error_rate = np.random.uniform(0.0, 0.1)
                if cpu_usage > 80 or memory_usage > 80:
                    error_rate = np.random.uniform(0.1, 0.3)
                
                # Alert logic
                has_alert = cpu_usage > 85 or memory_usage > 85 or latency > 400 or error_rate > 0.15
                alert_type = np.random.choice(alert_types) if has_alert else 'None'
                
                data.append({
                    'Timestamp': hour,
                    'Service': service,
                    'Environment': env,
                    'CPU_Usage': cpu_usage,
                    'Memory_Usage': memory_usage,
                    'API_Latency_ms': latency,
                    'Throughput_rps': throughput,
                    'Error_Rate': error_rate,
                    'Alert': alert_type,
                    'Uptime_Percent': np.random.uniform(99.0, 100.0)
                })
    
    # Create DataFrame and save to CSV
    df = pd.DataFrame(data)
    df.to_csv('data/engineering_data.csv', index=False)

def create_strategy_data():
    """Create Strategy department dummy data"""
    # Generate quarters for the last 8 quarters (2 years)
    current_year = datetime.now().year
    current_quarter = (datetime.now().month - 1) // 3 + 1
    quarters = []
    for i in range(8):
        q = current_quarter - i
        y = current_year
        while q <= 0:
            q += 4
            y -= 1
        quarters.append(f"{y}-Q{q}")
    quarters.reverse()  # Order from oldest to newest
    
    # Generate data
    data = []
    
    # Key company-wide KPIs
    for quarter in quarters:
        base_multiplier = quarters.index(quarter) / 7  # Growth factor over time
        
        data.append({
            'Period': quarter,
            'KPI_Category': 'Financial',
            'KPI_Name': 'Total Revenue',
            'Value': (2000000 + np.random.uniform(-100000, 300000)) * (1 + base_multiplier),
            'Target': 2500000 * (1 + base_multiplier),
            'YoY_Growth': np.random.uniform(0.15, 0.35)
        })
        
        data.append({
            'Period': quarter,
            'KPI_Category': 'Financial',
            'KPI_Name': 'Operating Margin',
            'Value': np.random.uniform(0.15, 0.25),
            'Target': 0.25,
            'YoY_Growth': np.random.uniform(0.02, 0.1)
        })
        
        data.append({
            'Period': quarter,
            'KPI_Category': 'Customer',
            'KPI_Name': 'Active Users',
            'Value': (50000 + np.random.randint(-5000, 15000)) * (1 + base_multiplier * 1.2),
            'Target': 60000 * (1 + base_multiplier),
            'YoY_Growth': np.random.uniform(0.2, 0.5)
        })
        
        data.append({
            'Period': quarter,
            'KPI_Category': 'Customer',
            'KPI_Name': 'Customer Satisfaction',
            'Value': np.random.uniform(75, 90),
            'Target': 85,
            'YoY_Growth': np.random.uniform(0.01, 0.08)
        })
        
        data.append({
            'Period': quarter,
            'KPI_Category': 'Operations',
            'KPI_Name': 'Transaction Volume',
            'Value': (5000000 + np.random.randint(-200000, 1000000)) * (1 + base_multiplier * 1.5),
            'Target': 6000000 * (1 + base_multiplier),
            'YoY_Growth': np.random.uniform(0.25, 0.6)
        })
        
        data.append({
            'Period': quarter,
            'KPI_Category': 'Operations',
            'KPI_Name': 'Transaction Success Rate',
            'Value': min(99.5, 95 + base_multiplier * 4 + np.random.uniform(0, 1)),
            'Target': 99,
            'YoY_Growth': np.random.uniform(0.005, 0.02)
        })
        
        data.append({
            'Period': quarter,
            'KPI_Category': 'Growth',
            'KPI_Name': 'New Market Entry',
            'Value': int(2 + base_multiplier * 5),
            'Target': int(3 + base_multiplier * 5),
            'YoY_Growth': np.random.uniform(0.1, 0.3)
        })
        
        data.append({
            'Period': quarter,
            'KPI_Category': 'Growth',
            'KPI_Name': 'Product Adoption Rate',
            'Value': np.random.uniform(0.3, 0.5),
            'Target': 0.5,
            'YoY_Growth': np.random.uniform(0.05, 0.15)
        })
    
    # Create DataFrame and save to CSV
    df = pd.DataFrame(data)
    df.to_csv('data/strategy_data.csv', index=False)
