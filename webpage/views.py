import time
from django.shortcuts import render
import serial
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Data
from . import predict_max, predict_min
from datetime import datetime

max_pred = '...'
min_pred = '...'
location = 'Yasuj'


def pred_func(location):
    global max_pred
    global min_pred

    today = datetime.now().strftime("%Y/%m/%d")
    dataset = (Data.objects.filter(location=location).exclude(date=today)).order_by('date', 'time')[:248]
    data_list = []
    for data in dataset:
        data_list.append(float(data.temperature))
    data = data_list
    max_pred = predict_max.max_pred(data)
    time.sleep(1)
    min_pred = predict_min.min_pred(data)

    return max_pred, min_pred


class SensorDataView(APIView):
    # get data from Arduino
    def get(self, request, format=None):
        global max_pred
        global min_pred
        global location

        if request.GET:
            location = request.GET.get('location')
            max_pred = '...'
            min_pred = '...'
            max_pred, min_pred = pred_func(location)
        ser = serial.Serial('COM7', 9600)  # Arduino settings
        data = ser.readline().decode('utf-8').strip().split(',')

        # check validation
        if len(data) == 2:
            humidity, temperature = data
            h = humidity.split()
            t = temperature.split()

            # day
            time_now = datetime.now()
            today = time_now.strftime("%A")

            # time --:--:--
            time_now = str(datetime.now()).split()
            time = time_now[1][:5]

            # dateد
            date_now = datetime.now().strftime("%Y/%m/%d")

            # ساعاتی که داده‌ها ذخیره می شوند
            target_hours = ['00:00', '03:00',
                            '06:00', '09:00',
                            '12:00', '15:00', '18:00', '21:00']

            if str(time) in target_hours:
                existing = Data.objects.filter(time=time, date=date_now)
                if not existing:
                    Data(
                        location='Yasuj',
                        temperature=str(t[1]),
                        time=time,
                        date=date_now
                    ).save()

            # send data to front
            context = {
                'humidity': "humidity:" + " " + str(h[1][:2] + h[2]),
                'temperature': str(t[1])[:2] + "°",
                'day': today[:3],
                'time': time,
                'date': date_now,
                'max_pred': '↑' + ' ' + str(max_pred) + '°',
                'min_pred': '↓' + ' ' + str(min_pred) + '°',
            }

            return Response(context,
                            status=status.HTTP_200_OK)

        else:
            context2 = {
                'humidity': 'error',
                'temperature': 'error',
                'day': 'error',
                'time': 'error',
                'date': 'error',
                'max_pred': 'error',
                'min_pred': 'error',
            }
            return Response(context2, status=status.HTTP_400_BAD_REQUEST)


def showView(request):
    return render(request,'webpage/front_web_proj.html')
