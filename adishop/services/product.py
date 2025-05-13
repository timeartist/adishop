import os

import pandas as pd
from flask import request, jsonify

from adishop.services import BaseService, run_service, parse_args

class ProductService(BaseService):
    def __init__(self, *args, **kwargs):    
        """Initialize the product service by loading data"""
        super().__init__(*args, **kwargs)
        self.db_df = self._load_data()
        
    def handle_get(self):
        """Handle product queries using the loaded DataFrame"""
        # Extract SKU from URL query parameters using Flask's request
        sku = request.args.get('sku')
        
        # Use query_data function to filter products
        ##TODO: we could potentially add more filters here, but not going to implement that as it's not core for this exercise
        result = self._query_data(self.db_df, sku=sku)
        
        # Convert to dict for JSON serialization
        if not result.empty: 
            return jsonify(result.to_dict(orient='records')[0]), 200
        else: 
            return jsonify({"error": "Product not found"}), 404
    
    def _load_csv_to_pandas(self):
        # Read the CSV file
        df = pd.read_csv('products.csv')
        
        # Convert crawled_at string to datetime
        df['crawled_at'] = pd.to_datetime(df['crawled_at'])
        
        # Convert empty strings in original_price to NaN and remove currency symbols
        df['original_price'] = df['original_price'].replace('', float('nan'))
        
        # Clean price columns by removing currency symbols and converting to numeric
        df['original_price'] = df['original_price'].astype(str).str.replace('$', '').str.replace(',', '').replace('', float('nan')).astype(float, errors='ignore')
        df['selling_price'] = df['selling_price'].astype(str).str.replace('$', '').str.replace(',', '').replace('', float('nan')).astype(float, errors='ignore')
        
        # Define column types using pandas dtypes
        dtypes = {
            'index': 'int64',
            'url': 'str',
            'name': 'str',
            'sku': 'str',
            'selling_price': 'float64',
            'original_price': 'float64',
            'currency': 'str',
            'availability': 'str',
            'color': 'str',
            'category': 'str',
            'source': 'str',
            'source_website': 'str',
            'breadcrumbs': 'str',
            'description': 'str',
            'brand': 'str',
            'images': 'str',
            'country': 'str',
            'language': 'str',
            'average_rating': 'float64',
            'reviews_count': 'int64',
            'crawled_at': 'datetime64[ns]'
        }
        
        # Apply the pandas dtypes
        df = df.astype({k: v for k, v in dtypes.items() if k in df.columns})
        # Store the DataFrame for later querying
        # You can save it as a pickle file for persistence
        df.to_pickle('products_db.pkl')
        
        print("Data successfully loaded into in-memory pandas DataFrame")
        return df

    def _query_data(self, df, sku=None, **filters):
        """
        Query the DataFrame with filters or by specific SKU
        Examples: 
        - query_data(df, brand='Adidas', color='black')
        - query_data(df, sku='ABC123')
        """
        if sku is not None:
            # Return a single row by SKU
            if sku in df['sku'].values:
                return df[df['sku'] == sku]
            return pd.DataFrame()  # Return empty DataFrame if SKU not found
        
        # Filter by other criteria
        query_result = df.copy()
        for column, value in filters.items():
            if column in df.columns:
                query_result = query_result[query_result[column] == value]
        return query_result

    def _load_data(self):
        """Load data from pickle file if it exists, otherwise load from CSV"""
        if os.path.exists('products_db.pkl'):
            print("Loading data from pickle file...")
            return pd.read_pickle('products_db.pkl')
        else:
            return self._load_csv_to_pandas()

def main():
    """Main function to run the product service"""
    args = parse_args()
    return run_service(ProductService, args)