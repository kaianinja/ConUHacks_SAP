#████████╗███████╗░█████╗░███╗░░░███╗  ███╗░░██╗██╗███╗░░░███╗██████╗░██╗░░░██╗░██████╗
#╚══██╔══╝██╔════╝██╔══██╗████╗░████║  ████╗░██║██║████╗░████║██╔══██╗██║░░░██║██╔════╝
#░░░██║░░░█████╗░░███████║██╔████╔██║  ██╔██╗██║██║██╔████╔██║██████╦╝██║░░░██║╚█████╗░
#░░░██║░░░██╔══╝░░██╔══██║██║╚██╔╝██║  ██║╚████║██║██║╚██╔╝██║██╔══██╗██║░░░██║░╚═══██╗
#░░░██║░░░███████╗██║░░██║██║░╚═╝░██║  ██║░╚███║██║██║░╚═╝░██║██████╦╝╚██████╔╝██████╔╝
#░░░╚═╝░░░╚══════╝╚═╝░░╚═╝╚═╝░░░░░╚═╝  ╚═╝░░╚══╝╚═╝╚═╝░░░░░╚═╝╚═════╝░░╚═════╝░╚═════╝░
#──────▄▀▄─────▄▀▄         ----------------------------------------------------------
#─────▄█░░▀▀▀▀▀░░█▄                   ConUHacks 2024 Team Members
#─▄▄──█░░░░░░░░░░░█──▄▄  Sisagha Phimmasone | Mustafa Ahmad | Cleopatr-Aliak-Manoukian
#█▄▄█─█░░▀░░┬░░▀░░█─█▄▄█   ----------------------------------------------------------


from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import csv
from datetime import datetime, timedelta
import os

# Constants for service details
SERVICE_HOURS = (7, 19)  # Operating hours: 7AM to 7PM, 12 hours total
OPERATIONAL_MINUTES_PER_DAY = (SERVICE_HOURS[1] - SERVICE_HOURS[0]) * 60
VEHICLE_TYPES = {
    'compact': {'service_time': 30, 'charge': 150},
    'medium': {'service_time': 30, 'charge': 150},
    'full-size': {'service_time': 30, 'charge': 150},
    'class 1 truck': {'service_time': 60, 'charge': 250},
    'class 2 truck': {'service_time': 120, 'charge': 700}
}

FREE_BOOTHS = 5

# Method to insert day separators after each day of booking
def insert_day_separators(df, timestamp_column):
    # Initialize a list to hold the processed data
    processed_data = []

    # Initialize a variable to track the last date
    last_date = None

    for index, row in df.iterrows():
        current_date = row[timestamp_column].date()

        # Check if the date has changed
        if last_date and current_date != last_date:
            # Insert a separator DataFrame
            separator = pd.DataFrame([{'Timestamp1': '', 'Timestamp2': '----- New Day -----', 'Category': ''}])
            processed_data.append(separator)

        processed_data.append(row.to_frame().T)  # Convert row to DataFrame and transpose
        last_date = current_date

    # Concatenate all DataFrame pieces
    return pd.concat(processed_data, ignore_index=True)

# Function to parse CSV data while handling anomalies and invalid data
def parse_csv_data_with_anomaly_check(file_path):
    valid_appointments = []
    with open(file_path, newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            try:
                call_time_str, request_time_str, _ = row
                call_time = datetime.strptime(call_time_str, '%Y-%m-%d %H:%M:%S')
                request_time = datetime.strptime(request_time_str, '%Y-%m-%d %H:%M:%S')
                
                # Exclude appointments booked in the past (anomalies)
                if call_time <= request_time:
                    valid_appointments.append(row)
            except ValueError:
                continue  # Skip rows with invalid data
    return valid_appointments

# Function to initialize booth availability for a day
def initialize_daily_booth_availability():
    # Initialize availability for dedicated booths and free booths
    return {k: [True] * OPERATIONAL_MINUTES_PER_DAY for k in VEHICLE_TYPES.keys()}, [True] * (OPERATIONAL_MINUTES_PER_DAY * FREE_BOOTHS)

# Function to find next available free booth
def find_free_booth(free_booths, start_minute, end_minute):
    # Iterate over each free booth to check availability
    for i in range(FREE_BOOTHS):
        booth_start = i * OPERATIONAL_MINUTES_PER_DAY
        if all(free_booths[booth_start + minute] for minute in range(start_minute, end_minute)):
            return i  
    return None  # No free booth found

# Function to schedule appointments considering future appointments and gather statistics
def schedule_appointments_with_stats(appointments):
    daily_booth_availability, daily_free_booth_availability = initialize_daily_booth_availability()
    revenue = 0
    lost_revenue = 0
    serviced_customers = {k: 0 for k in VEHICLE_TYPES.keys()}
    turned_away_customers = {k: 0 for k in VEHICLE_TYPES.keys()}
    current_day = None
    total_unused_time_dedicated = {k: 0 for k in VEHICLE_TYPES.keys()}
    total_unused_time_free = 0

    appointments.sort(key=lambda x: x[1])  # Sort appointments by request time

    for appointment in appointments:
        call_time_str, request_time_str, vehicle_type = appointment
        call_time = datetime.strptime(call_time_str, '%Y-%m-%d %H:%M:%S')
        request_time = datetime.strptime(request_time_str, '%Y-%m-%d %H:%M:%S')

        # Reset for a new day
        if current_day is None or request_time.date() != current_day:
            # Calculate unused time for the previous day before resetting
            if current_day is not None:
                for booth_type in VEHICLE_TYPES.keys():
                    total_unused_time_dedicated[booth_type] += sum(daily_booth_availability[booth_type])
                total_unused_time_free += sum(daily_free_booth_availability) / FREE_BOOTHS
            current_day = request_time.date()
            daily_booth_availability, daily_free_booth_availability = initialize_daily_booth_availability()


        # Check if the service fits within the shop's operating hours
        service_time = VEHICLE_TYPES[vehicle_type]['service_time']
        end_time = request_time + timedelta(minutes=service_time)
        if request_time.hour < SERVICE_HOURS[0] or (end_time.hour > SERVICE_HOURS[1] or (end_time.hour == SERVICE_HOURS[1] and end_time.minute > 0)):
            turned_away_customers[vehicle_type] += 1
            
            lost_revenue += VEHICLE_TYPES[vehicle_type]['charge']
            continue

        start_minute = (request_time.hour * 60 + request_time.minute) - (SERVICE_HOURS[0] * 60)
        end_minute = start_minute + service_time

        # Try to allor a free booth
        booth_allocated = False
        if all(daily_booth_availability[vehicle_type][start_minute:end_minute]):
            for minute in range(start_minute, end_minute):
                daily_booth_availability[vehicle_type][minute] = False
            booth_allocated = True
        else:
            free_booth_index = find_free_booth(daily_free_booth_availability, start_minute, end_minute)
            if free_booth_index is not None:
                booth_start = free_booth_index * OPERATIONAL_MINUTES_PER_DAY
                for minute in range(start_minute, end_minute):
                    daily_free_booth_availability[booth_start + minute] = False
                booth_allocated = True

        if booth_allocated:
            revenue += VEHICLE_TYPES[vehicle_type]['charge']
            serviced_customers[vehicle_type] += 1
        else:
            turned_away_customers[vehicle_type] += 1
            lost_revenue += VEHICLE_TYPES[vehicle_type]['charge']

    # Calculate unused time for the last day in the dataset
    for booth_type in VEHICLE_TYPES.keys():
        total_unused_time_dedicated[booth_type] += sum(daily_booth_availability[booth_type])
    total_unused_time_free += sum(daily_free_booth_availability) / FREE_BOOTHS

    return serviced_customers, turned_away_customers, revenue, lost_revenue, total_unused_time_dedicated, total_unused_time_free


app = Flask(__name__)

@app.route('/', methods=["POST", "GET"])
def home():
    # Variable to keep track of processing status
    processed_csv = False
    if request.method == "POST":
        csvFile = request.files['csvInput']
        if csvFile.name != '' and csvFile:
            csvFile.save('uploads/' + csvFile.filename)
            df = pd.read_csv('uploads/' + csvFile.filename, header=None, names=['Timestamp1', 'Timestamp2', 'Category'])
            os.remove('uploads/' + csvFile.filename)
            
            # Add ':00' to the end of each timestamp in the first column
            df['Timestamp1'] = df['Timestamp1'].apply(lambda x: x + ':00')

            # Convert the second timestamp column to datetime
            df['Timestamp2'] = pd.to_datetime(df['Timestamp2'])

            # Sort by the second timestamp
            df = df.sort_values(by='Timestamp2')

            # Insert day separators
            df = insert_day_separators(df, 'Timestamp2')
            
            df.to_csv('uploads/changed_' + csvFile.filename, index=False)
            
            appointments = parse_csv_data_with_anomaly_check('uploads/changed_' + csvFile.filename)
            
            processed_csv = True
            
            os.remove('uploads/changed_' + csvFile.filename)
            
            # Schedule the appointments and calculate revenue
            serviced, turned_away, revenue, lost_revenue, booth_availability, turn_away_reasons = schedule_appointments_with_stats(appointments)
            
            totalVehiclesServiced = serviced['compact'] + serviced['medium'] + serviced['full-size'] + serviced['class 1 truck'] + serviced['class 2 truck']
            totalVehiclesTurnedAway = turned_away['compact'] + turned_away['medium'] + turned_away['full-size'] + turned_away['class 1 truck'] + turned_away['class 2 truck']
            
            return render_template("sap.html", REVENUE = revenue, 
                                               TURNED_AWAY_COUNT = turned_away, 
                                               LOST_REVENUE = lost_revenue, 
                                               PROCESSED_CSV = processed_csv,
                                               SERVICED = serviced,
                                               BOOTH_AVAILABILITY = booth_availability,
                                               TURN_AWAY_REASONS = turn_away_reasons,
                                               CSV_FILENAME = csvFile.filename,
                                               SERVICED_TOTAL_COUNT = totalVehiclesServiced,
                                               TURNED_AWAY_TOTAL = totalVehiclesTurnedAway)
            
    else:
        return render_template("sap.html", PROCESSED_CSV = processed_csv)
if __name__ == "__main__":
    app.run(debug=True)
