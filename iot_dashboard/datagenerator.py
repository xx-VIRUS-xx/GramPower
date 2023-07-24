from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType
from datetime import datetime, timedelta
from devices.models import RealTimeData,Device
import time
import random
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iot_dashboard.settings') 
# Replace 'your_project_name' with your Django project name
django.setup()

# Create a SparkSession
spark = SparkSession.builder \
    .appName("Data Generator") \
    .getOrCreate()

# Schema for the data
schema = StructType([
    StructField("Current", DoubleType(), True),
    StructField("Voltage", DoubleType(), True),
    StructField("Power", DoubleType(), True),
    StructField("Timestamp", TimestampType(), True)
])

# Create an empty DataFrame
df = spark.createDataFrame([], schema)

# Function to generate random data
def generate_data():
    current = random.uniform(0, 10)
    voltage = random.uniform(100, 250)
    power = current * voltage
    timestamp = datetime.now()
    return current, voltage, power, timestamp

device_ids = Device.objects.values_list('device_id', flat=True)
# Main loop to generate and store data
while True:

    device_id = random.choice(device_ids)

    current, voltage, power, timestamp = generate_data()
    data = [(current, voltage, power, timestamp)]
    new_data = spark.createDataFrame(data, schema)
    
    # Append new data to the DataFrame
    df = df.union(new_data)
    
    # Store the data in the SQLite database
    
    real_time_data = RealTimeData(device_id=device_id,current=current, voltage=voltage, power=power, timestamp=timestamp)
    real_time_data.save()
    
    # Wait for 5 seconds before generating the next data point
    time.sleep(random.uniform(5,10))
