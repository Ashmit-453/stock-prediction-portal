from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import StockPredictionSerializer
from rest_framework import status
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os
from django.conf import settings
from .utils import save_plot
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model
from sklearn.metrics import mean_squared_error, r2_score

class StockPredictionView(APIView):
    def post(self, request):
        serializer = StockPredictionSerializer(data=request.data)
        if serializer.is_valid():
            ticker = serializer.validated_data['ticker']
            now = datetime.now()
            start = datetime(now.year-10, now.month, now.day)
            end = now
            df = yf.download(ticker, start, end)
            if df.empty:
                return Response({"error": "No data found for the given ticker.",
                                 'status': status.HTTP_404_NOT_FOUND})
            df = df.reset_index()
            plt.switch_backend('AGG')
            plt.figure(figsize=(12, 5))
            plt.plot(df.Close, label='Closing Price')
            plt.title(f'Closing price of {ticker}')
            plt.xlabel('Days')
            plt.ylabel('Price')
            plt.legend()
            # Save the plot to a file
            plot_filename = f"{ticker}_plot.png"
            plot_img_path = os.path.join(settings.MEDIA_ROOT, f"{ticker}_plot.png")
            plot_img = save_plot(plot_img_path)
            plot_url = request.build_absolute_uri(settings.MEDIA_URL+plot_filename)
            print(plot_img)
            # 100 Days moving average
            ma100 = df.Close.rolling(100).mean()
            plt.switch_backend('AGG')
            plt.figure(figsize=(12, 5))
            plt.plot(df.Close, label='Closing Price')
            plt.plot(ma100, 'r', label='100 DMA')
            plt.title(f'100 Days Moving Average of {ticker}')
            plt.xlabel('Days')
            plt.ylabel('Price')
            plt.legend()
            plot_dma_img = f'{ticker}_100_dma.png'
            plot_dma_img_path = os.path.join(settings.MEDIA_ROOT, plot_dma_img)
            plot_100_dma = save_plot(plot_dma_img_path)
            plot_100_dma_url = request.build_absolute_uri(settings.MEDIA_URL+plot_dma_img)
            
            # 200 Days moving average
            ma200 = df.Close.rolling(200).mean()
            plt.switch_backend('AGG')
            plt.figure(figsize=(12, 5))
            plt.plot(df.Close, label='Closing Price')
            plt.plot(ma100, 'r', label='100 DMA')
            plt.plot(ma200, 'g', label='200 DMA')
            plt.title(f'200 Days Moving Average of {ticker}')
            plt.xlabel('Days')
            plt.ylabel('Price')
            plt.legend()
            plot_dimg_path = f'{ticker}_200_dma.png'
            plot_200_img_path = os.path.join(settings.MEDIA_ROOT, plot_dimg_path)
            plot_200_dma = save_plot(plot_200_img_path)
            plot_200_dma_url = request.build_absolute_uri(settings.MEDIA_URL+plot_dimg_path)
            prediction = f"Predicted data for {ticker}"
            return Response({"prediction": prediction,
                             "plot_img":plot_url,
                             "plot_100_dma":plot_100_dma_url,
                             "plot_200_dma":plot_200_dma_url,})
        return Response(serializer.errors, status=400)