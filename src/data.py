# Scripts to load and preprocess data

import pandas as pd
import datetime
import os
# Importe aqui outras bibliotecas necessárias, como requests ou yfinance para coleta de dados
from IPython.display import display
import yfinance as yf
from ta import add_all_ta_features
from ta.utils import dropna
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def display_info(title:str, df:pd.DataFrame, ticker:None, start_date:None, end_date:None):
    """
    Display formatted information about the data processing steps.

    Args:
    title (str): Description of the information to display.
    df (DataFrame): The pandas DataFrame containing the stock data.
    ticker (str): The stock ticker symbol.
    start_date (str): The start date of the data.
    end_date (str): The end date of the data.
    """
    # Creating a separator for aesthetic purposes
    separator = "-" * 50

    # Getting data shape and missing values
    shape_info = f"Data Shape: {df.shape} (rows, columns)"
    missing_values_info = f"Missing Values: {df.isnull().sum().sum()}"


    # Using f-string for formatted output
    info = (
        f"\n{separator}\n"
        f"{title}\n"
        f"Ticker: {ticker}\n"
        f"Start Date: {start_date}\n"
        f"End Date: {end_date}\n"
        f"{shape_info}\n"
        f"{missing_values_info}\n"
        f"{separator}\n"
    )

    print(info)


def load_stock_data(ticker:None, start_date:None, end_date:None, data_dir:str, interval='1m', force_download=False):
    """
    Load or download stock data at minute level.

    Args:
        ticker (str): Stock ticker symbol.
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.
        data_dir (str): Directory to save and load the data.
        interval (str): Data interval (default '1m' for 1 minute).
        force_download (bool): If True, force a fresh download of data.

    Returns:
        DataFrame: DataFrame containing the stock data.
    """
    filename = f"{ticker}_{start_date}_{end_date}.parquet"
    file_path = os.path.join(data_dir, filename)

    # Check if the data file exists and load it, unless force download is specified
    if os.path.exists(file_path) and not force_download:
        print(f"Loading data from {file_path}")
        return pd.read_parquet(file_path)
    else:
        print(f"Downloading data for {ticker}...")
        try:
            df_stock_data = yf.download(ticker, start=start_date, end=end_date, interval=interval)
            if df_stock_data.empty:
                raise ValueError(f"No data found for {ticker} between {start_date} and {end_date}.")
            df_stock_data.to_parquet(file_path)
            print(f"Data saved to {file_path}")
            return df_stock_data
        except Exception as e:
            raise ConnectionError(f"Failed to download data: {e}")


def add_technical_indicators(df_stock_data:pd.DataFrame):
    """
    Adiciona indicadores técnicos ao DataFrame de ações.

    Returns:
    DataFrame: Dados históricos do ativo.

    """
    if df_stock_data.empty:
        raise ValueError("DataFrame está vazio. Não é possível calcular indicadores técnicos.")
    
    df_stock_data = dropna(df_stock_data)
    try:
        df_stock_data_all_features = add_all_ta_features(df_stock_data, open="Open", high="High", low="Low", close="Close", volume="Volume")
    except Exception as e:
        raise ValueError(f"Erro ao adicionar indicadores técnicos: {e}")
    
    return df_stock_data_all_features
     

def clean_data(df_stock_data_all_features:pd.DataFrame):
    """
    Limpa e prepara os dados do ativo.

    Args:
    df (DataFrame): DataFrame contendo dados brutos do ativo.

    Returns:
    DataFrame: DataFrame limpo e pronto para análise.
    """
    # Implemente a lógica de limpeza de dados
    return df_stock_data_all_features

def colect_and_clean_data(ticker:None, start_date:None, end_date:None, data_dir:str, interval='1m', force_download=False):
    """
    Função principal para carregar e preparar dados do ativo.

    Args:
    ticker (str): Ticker do ativo.
    start_date (str): Data de início.
    end_date (str): Data de fim.
    """

    try:
        df_stock_data = load_stock_data(ticker=ticker, start_date=start_date, end_date=end_date, data_dir=data_dir, interval=interval,force_download=force_download)

        df_stock_data_all_features = add_technical_indicators(df_stock_data)

        df_stock_data_all_features_clean=clean_data(df_stock_data_all_features)

        display_info(title='Successful Import', ticker=ticker, start_date=start_date, end_date=end_date, df=df_stock_data_all_features_clean)

        return df_stock_data_all_features_clean
        
    except ValueError as e:
        display(e)
    return None