import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error
import argparse
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from darts import TimeSeries
from darts.models import (
    FFT,
    TCNModel,
    VARIMA,
    KalmanForecaster,
    RegressionModel,
    LinearRegressionModel,
    LightGBMModel,
    CatBoostModel,
    XGBModel,
    RNNModel,
    BlockRNNModel,
    NBEATSModel,
    NHiTSModel,
    TransformerModel,
    TFTModel,
    DLinearModel,
    NLinearModel,
)

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Testing script for predictions')
parser.add_argument("--model_name", type=str, help="Name of the forecasting model to use.")
parser.add_argument('--model_path', type=str, help='Path to the trained model')
parser.add_argument('--data_path', type=str, help='Path to the data file')
parser.add_argument("--input_chunk_size", type=int, default=24, help="Size of the input chunk for TCNModel. Default is 24.")
parser.add_argument("--output_chunk_size", type=int, default=12, help="Size of the output chunk for TCNModel. Default is 12.")
parser.add_argument("--target", type=str, help="Target to visualise")
args = parser.parse_args()

def load_data(data_path):
    # Read a pandas DataFrame
    df = pd.read_csv(data_path, delimiter=",")

    if 'SYMBOL' in df.columns:
        df = df.drop('SYMBOL', axis = 1)

    # Create a TimeSeries, specifying the time and value columns
    series = TimeSeries.from_dataframe(df, time_col = "date", fill_missing_dates=True, freq='H')

    # Set aside the last 36 months as a validation series
    series, data, label = series[-200:], series[-200:-48], series[-48:]
    return series, data, label

input_chunk_size = args.input_chunk_size
output_chunk_size = args.output_chunk_size
# Load the trained model
model_name = args.model_name
if model_name == "FFT":
        model = FFT()
elif model_name == "TCN":
    model = TCNModel(input_chunk_length=args.input_chunk_size, output_chunk_length=args.output_chunk_size)
elif model_name == "VARIMA":
        model = VARIMA()
elif model_name == "KalmanForecaster":
    model = KalmanForecaster()
elif model_name == "RegressionModel":
    model = RegressionModel(input_chunk_length=input_chunk_size, output_chunk_length=output_chunk_size)
elif model_name == "LinearRegressionModel":
    model = LinearRegressionModel(input_chunk_length=input_chunk_size, output_chunk_length=output_chunk_size)
elif model_name == "LightGBMModel":
    model = LightGBMModel(input_chunk_length=input_chunk_size, output_chunk_length=output_chunk_size)
elif model_name == "CatBoostModel":
    model = CatBoostModel(input_chunk_length=input_chunk_size, output_chunk_length=output_chunk_size)
elif model_name == "XGBModel":
    model = XGBModel(input_chunk_length=input_chunk_size, output_chunk_length=output_chunk_size)
elif model_name == "RNNModel":
    model = RNNModel(input_chunk_length=input_chunk_size, output_chunk_length=output_chunk_size)
elif model_name == "BlockRNNModel":
    model = BlockRNNModel(input_chunk_length=input_chunk_size, output_chunk_length=output_chunk_size)
elif model_name == "NBEATSModel":
    model = NBEATSModel(input_chunk_length=input_chunk_size, output_chunk_length=output_chunk_size)
elif model_name == "NHiTSModel":
    model = NHiTSModel(input_chunk_length=input_chunk_size, output_chunk_length=output_chunk_size)
elif model_name == "TransformerModel":
    model = TransformerModel(input_chunk_length=input_chunk_size, output_chunk_length=output_chunk_size)
elif model_name == "TFTModel":
    model = TFTModel(input_chunk_length=input_chunk_size, output_chunk_length=output_chunk_size)
elif model_name == "DLinearModel":
    model = DLinearModel()
elif model_name == "NLinearModel":
    model = NLinearModel()
else:
    raise ValueError("Invalid model name. Supported models: FFT, TCN")
model = model.load(args.model_path)
# Load the data
series, data, label = load_data(args.data_path)

# # Normalize the data (using the same scaler as during training)
# scaler = MinMaxScaler()
# data['value'] = scaler.fit_transform(data['value'].values.reshape(-1, 1))

# Perform predictions
predictions = model.predict(len(label))

# # Denormalize the predictions
# predictions = scaler.inverse_transform(predictions.pd_dataframe()['value'].values.reshape(-1, 1))

series[args.target].plot()
predictions[args.target].plot(label="forecast", low_quantile=0.05, high_quantile=0.95)
plt.legend()


# Save the plot as an image
plt.savefig('predictions_plot.png')
plt.show()

# # Compute MSE and MAE
# mse = mean_squared_error(series[-len(predictions):], predictions)
# mae = mean_absolute_error(series[-len(predictions):], predictions)

# # Print MSE and MAE
# print(f'MSE: {mse:.4f}')
# print(f'MAE: {mae:.4f}')


