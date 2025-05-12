import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime

from sqlalchemy.orm import sessionmaker, declarative_base
import datetime

# Create a base class for our class definitions
Base = declarative_base()

class Adidas(Base):
    __tablename__ = 'adidas'
    
    index = Column(Integer, primary_key=True)
    url = Column(String)
    name = Column(String)
    sku = Column(String)
    selling_price = Column(Float)
    original_price = Column(Float, nullable=True)
    currency = Column(String)
    availability = Column(String)
    color = Column(String)
    category = Column(String)
    source = Column(String)
    source_website = Column(String)
    breadcrumbs = Column(String)
    description = Column(String)
    brand = Column(String)
    images = Column(String)
    country = Column(String)
    language = Column(String)
    average_rating = Column(Float)
    reviews_count = Column(Integer)
    crawled_at = Column(DateTime)

def load_csv_to_postgres():
    # Read the CSV file
    df = pd.read_csv('adidas.csv')
    
    # Convert crawled_at string to datetime
    df['crawled_at'] = pd.to_datetime(df['crawled_at'])
    
    # Convert empty strings in original_price to NaN
    df['original_price'] = df['original_price'].replace('', float('nan'))
    
    # Create a database connection
    engine = create_engine('postgresql://postgres:password@localhost:5432')
    
    # Create the table
    Base.metadata.create_all(engine)
    
    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Insert data into the database
    try:
        # Use pandas to_sql method for bulk insert
        df.to_sql('adidas', engine, if_exists='replace', index=False)
        print("Data successfully loaded into PostgreSQL database")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    load_csv_to_postgres()