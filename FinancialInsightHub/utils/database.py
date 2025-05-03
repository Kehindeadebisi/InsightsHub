import os
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey, MetaData, Table, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from datetime import datetime
import time

# Get the database connection URL from environment variables
DATABASE_URL = os.environ.get('DATABASE_URL')

# Create the SQLAlchemy engine with connection pooling and retry settings
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,           # Test connections before using them
    pool_recycle=3600,            # Recycle connections after 1 hour
    connect_args={
        "connect_timeout": 10,    # Connection timeout of 10 seconds
    }
)

# Create a base class for declarative models
Base = declarative_base()

# Create a session factory
Session = sessionmaker(bind=engine)

# Function to get a session with retry logic
def get_session(max_retries=3, retry_delay=1):
    """Get a database session with retry logic for resilience"""
    retries = 0
    last_error = None
    
    while retries < max_retries:
        try:
            session = Session()
            # Test the connection
            session.execute(text("SELECT 1"))
            return session
        except (OperationalError, SQLAlchemyError) as e:
            last_error = e
            session.close()
            retries += 1
            time.sleep(retry_delay)
            print(f"Database connection attempt {retries} failed, retrying...")
    
    # If we get here, all retries failed
    print(f"Failed to connect to database after {max_retries} attempts: {last_error}")
    return None

# Define models for each data type
class Finance(Base):
    __tablename__ = 'finance'
    
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    currency = Column(String, nullable=False)
    fx_rate = Column(Float, nullable=False)
    exposure = Column(Float, nullable=False)
    inflow = Column(Float, nullable=False)
    outflow = Column(Float, nullable=False)
    net_position = Column(Float, nullable=False)
    country = Column(String, nullable=False)
    
    @classmethod
    def from_dataframe(cls, df):
        """Convert a dataframe to a list of Finance objects"""
        records = []
        for _, row in df.iterrows():
            record = cls(
                date=datetime.strptime(row['Date'], '%Y-%m-%d').date() if isinstance(row['Date'], str) else row['Date'],
                currency=row['Currency'],
                fx_rate=row['FX_Rate'],
                exposure=row['Exposure'],
                inflow=row['Inflow'],
                outflow=row['Outflow'],
                net_position=row['Net_Position'],
                country=row['Country']
            )
            records.append(record)
        return records

    @classmethod
    def to_dataframe(cls, session):
        """Convert Finance table data to a pandas DataFrame"""
        query = session.query(cls)
        records = query.all()
        
        data = [{
            'Date': record.date,
            'Currency': record.currency,
            'FX_Rate': record.fx_rate,
            'Exposure': record.exposure,
            'Inflow': record.inflow,
            'Outflow': record.outflow,
            'Net_Position': record.net_position,
            'Country': record.country
        } for record in records]
        
        return pd.DataFrame(data)

class HR(Base):
    __tablename__ = 'hr'
    
    id = Column(Integer, primary_key=True)
    month = Column(String, nullable=False)
    department = Column(String, nullable=False)
    headcount = Column(Integer, nullable=False)
    new_hires = Column(Integer, nullable=False)
    terminations = Column(Integer, nullable=False)
    turnover_rate = Column(Float, nullable=False)
    avg_leave_days = Column(Float, nullable=False)
    sick_days = Column(Integer, nullable=False)
    location = Column(String, nullable=False)
    avg_onboarding_days = Column(Integer, nullable=False)
    
    @classmethod
    def from_dataframe(cls, df):
        """Convert a dataframe to a list of HR objects"""
        records = []
        for _, row in df.iterrows():
            record = cls(
                month=row['Month'],
                department=row['Department'],
                headcount=row['Headcount'],
                new_hires=row['New_Hires'],
                terminations=row['Terminations'],
                turnover_rate=row['Turnover_Rate'],
                avg_leave_days=row['Avg_Leave_Days'],
                sick_days=row['Sick_Days'],
                location=row['Location'],
                avg_onboarding_days=row['Avg_Onboarding_Days']
            )
            records.append(record)
        return records

    @classmethod
    def to_dataframe(cls, session):
        """Convert HR table data to a pandas DataFrame"""
        query = session.query(cls)
        records = query.all()
        
        data = [{
            'Month': record.month,
            'Department': record.department,
            'Headcount': record.headcount,
            'New_Hires': record.new_hires,
            'Terminations': record.terminations,
            'Turnover_Rate': record.turnover_rate,
            'Avg_Leave_Days': record.avg_leave_days,
            'Sick_Days': record.sick_days,
            'Location': record.location,
            'Avg_Onboarding_Days': record.avg_onboarding_days
        } for record in records]
        
        return pd.DataFrame(data)

class Payments(Base):
    __tablename__ = 'payments'
    
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    channel = Column(String, nullable=False)
    country = Column(String, nullable=False)
    transaction_volume = Column(Integer, nullable=False)
    successful_transactions = Column(Integer, nullable=False)
    failed_transactions = Column(Integer, nullable=False)
    success_rate = Column(Float, nullable=False)
    avg_processing_time_sec = Column(Float, nullable=False)
    retry_count = Column(Integer, nullable=False)
    primary_error = Column(String, nullable=False)
    
    @classmethod
    def from_dataframe(cls, df):
        """Convert a dataframe to a list of Payments objects"""
        records = []
        for _, row in df.iterrows():
            record = cls(
                date=datetime.strptime(row['Date'], '%Y-%m-%d').date() if isinstance(row['Date'], str) else row['Date'],
                channel=row['Channel'],
                country=row['Country'],
                transaction_volume=row['Transaction_Volume'],
                successful_transactions=row['Successful_Transactions'],
                failed_transactions=row['Failed_Transactions'],
                success_rate=row['Success_Rate'],
                avg_processing_time_sec=row['Avg_Processing_Time_Sec'],
                retry_count=row['Retry_Count'],
                primary_error=row['Primary_Error']
            )
            records.append(record)
        return records

    @classmethod
    def to_dataframe(cls, session):
        """Convert Payments table data to a pandas DataFrame"""
        query = session.query(cls)
        records = query.all()
        
        data = [{
            'Date': record.date,
            'Channel': record.channel,
            'Country': record.country,
            'Transaction_Volume': record.transaction_volume,
            'Successful_Transactions': record.successful_transactions,
            'Failed_Transactions': record.failed_transactions,
            'Success_Rate': record.success_rate,
            'Avg_Processing_Time_Sec': record.avg_processing_time_sec,
            'Retry_Count': record.retry_count,
            'Primary_Error': record.primary_error
        } for record in records]
        
        return pd.DataFrame(data)

class Engineering(Base):
    __tablename__ = 'engineering'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(String, nullable=False)
    service = Column(String, nullable=False)
    environment = Column(String, nullable=False)
    cpu_usage = Column(Float, nullable=False)
    memory_usage = Column(Float, nullable=False)
    api_latency_ms = Column(Float, nullable=False)
    throughput_rps = Column(Float, nullable=False)
    error_rate = Column(Float, nullable=False)
    alert = Column(String, nullable=False)
    uptime_percent = Column(Float, nullable=False)
    
    @classmethod
    def from_dataframe(cls, df):
        """Convert a dataframe to a list of Engineering objects"""
        records = []
        for _, row in df.iterrows():
            record = cls(
                timestamp=row['Timestamp'],
                service=row['Service'],
                environment=row['Environment'],
                cpu_usage=row['CPU_Usage'],
                memory_usage=row['Memory_Usage'],
                api_latency_ms=row['API_Latency_ms'],
                throughput_rps=row['Throughput_rps'],
                error_rate=row['Error_Rate'],
                alert=row['Alert'],
                uptime_percent=row['Uptime_Percent']
            )
            records.append(record)
        return records

    @classmethod
    def to_dataframe(cls, session):
        """Convert Engineering table data to a pandas DataFrame"""
        query = session.query(cls)
        records = query.all()
        
        data = [{
            'Timestamp': record.timestamp,
            'Service': record.service,
            'Environment': record.environment,
            'CPU_Usage': record.cpu_usage,
            'Memory_Usage': record.memory_usage,
            'API_Latency_ms': record.api_latency_ms,
            'Throughput_rps': record.throughput_rps,
            'Error_Rate': record.error_rate,
            'Alert': record.alert,
            'Uptime_Percent': record.uptime_percent
        } for record in records]
        
        return pd.DataFrame(data)

class Strategy(Base):
    __tablename__ = 'strategy'
    
    id = Column(Integer, primary_key=True)
    period = Column(String, nullable=False)
    kpi_category = Column(String, nullable=False)
    kpi_name = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    target = Column(Float, nullable=False)
    yoy_growth = Column(Float, nullable=False)
    
    @classmethod
    def from_dataframe(cls, df):
        """Convert a dataframe to a list of Strategy objects"""
        records = []
        for _, row in df.iterrows():
            record = cls(
                period=row['Period'],
                kpi_category=row['KPI_Category'],
                kpi_name=row['KPI_Name'],
                value=row['Value'],
                target=row['Target'],
                yoy_growth=row['YoY_Growth']
            )
            records.append(record)
        return records

    @classmethod
    def to_dataframe(cls, session):
        """Convert Strategy table data to a pandas DataFrame"""
        query = session.query(cls)
        records = query.all()
        
        data = [{
            'Period': record.period,
            'KPI_Category': record.kpi_category,
            'KPI_Name': record.kpi_name,
            'Value': record.value,
            'Target': record.target,
            'YoY_Growth': record.yoy_growth
        } for record in records]
        
        return pd.DataFrame(data)

def create_tables():
    """Create all database tables if they don't exist"""
    Base.metadata.create_all(engine)

def drop_tables():
    """Drop all database tables"""
    Base.metadata.drop_all(engine)

def import_data_from_csv():
    """Import data from CSV files into the database"""
    # Create a session using our retry logic
    session = get_session()
    if not session:
        print("Could not establish database connection. Using CSV files instead.")
        return False
    
    try:
        # First, make sure tables exist
        create_tables()
        
        # Check if tables already have data
        if session.query(Finance).count() > 0:
            print("Data already exists in the database. Skipping import.")
            session.close()
            return True
            
        # Import Finance data
        if os.path.exists('data/finance_data.csv'):
            finance_df = pd.read_csv('data/finance_data.csv')
            finance_records = Finance.from_dataframe(finance_df)
            session.add_all(finance_records)
        
        # Import HR data
        if os.path.exists('data/hr_data.csv'):
            hr_df = pd.read_csv('data/hr_data.csv')
            hr_records = HR.from_dataframe(hr_df)
            session.add_all(hr_records)
        
        # Import Payments data
        if os.path.exists('data/payments_data.csv'):
            payments_df = pd.read_csv('data/payments_data.csv')
            # Ensure Primary_Error is a string type - fixing the type error
            payments_df['Primary_Error'] = payments_df['Primary_Error'].astype(str)
            payments_records = Payments.from_dataframe(payments_df)
            session.add_all(payments_records)
        
        # Import Engineering data
        if os.path.exists('data/engineering_data.csv'):
            engineering_df = pd.read_csv('data/engineering_data.csv')
            engineering_records = Engineering.from_dataframe(engineering_df)
            session.add_all(engineering_records)
        
        # Import Strategy data
        if os.path.exists('data/strategy_data.csv'):
            strategy_df = pd.read_csv('data/strategy_data.csv')
            strategy_records = Strategy.from_dataframe(strategy_df)
            session.add_all(strategy_records)
        
        # Commit the changes
        session.commit()
        print("Data import completed successfully")
        return True
    except Exception as e:
        session.rollback()
        print(f"Error importing data: {e}")
        return False
    finally:
        session.close()

def load_all_data_from_db():
    """Load all department data from the database and return as a dictionary"""
    # Get a session with retry logic
    session = get_session()
    if not session:
        return None
        
    try:
        data = {}
        
        # Load data from database tables
        data['finance'] = Finance.to_dataframe(session)
        data['hr'] = HR.to_dataframe(session)
        data['payments'] = Payments.to_dataframe(session)
        data['engineering'] = Engineering.to_dataframe(session)
        data['strategy'] = Strategy.to_dataframe(session)
        
        return data
    except Exception as e:
        print(f"Error loading data from database: {e}")
        return None
    finally:
        session.close()

def is_database_initialized():
    """Check if the database has been initialized with data"""
    # Get a session with retry logic
    session = get_session()
    if not session:
        return False
        
    try:
        # Check if any tables have data
        try:
            # Try one table first to check if tables even exist
            finance_count = session.query(Finance).count()
            
            # If first check worked, check all tables
            hr_count = session.query(HR).count()
            payments_count = session.query(Payments).count()
            engineering_count = session.query(Engineering).count()
            strategy_count = session.query(Strategy).count()
            
            return (finance_count > 0 and hr_count > 0 and payments_count > 0 and 
                    engineering_count > 0 and strategy_count > 0)
        except Exception as e:
            # If querying tables failed, they probably don't exist yet
            print(f"Error checking database tables: {e}")
            return False
    except Exception as e:
        print(f"Error checking database initialization: {e}")
        return False
    finally:
        session.close()