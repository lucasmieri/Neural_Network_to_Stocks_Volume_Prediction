# Main Python Project

# Importing the data module from src package
from src import data

def main():
    # Example usage of functions from data.py
    ticker = "AAPL"
    start_date = "2023-12-25"
    end_date = "2023-12-31"
    data_dir = "./data"

    df_stock = data.colect_and_clean_data(ticker, start_date, end_date, data_dir, force_download=True)

    # Further processing, analysis, or model training can go here

if __name__ == "__main__":
    main()
