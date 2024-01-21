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


import csv
from datetime import datetime, timedelta

# Constants for service details
SERVICE_HOURS = (7, 19)  # Operating hours: 7AM to 7PM, 12 hours total
OPERATIONAL_MINUTES_PER_DAY = 12 * 60  # Total operational minutes per day
VEHICLE_TYPES = {
    'compact': {'service_time': 30, 'charge': 150},
    'medium': {'service_time': 30, 'charge': 150},
    'full-size': {'service_time': 30, 'charge': 150},
    'class 1 truck': {'service_time': 60, 'charge': 250},
    'class 2 truck': {'service_time': 120, 'charge': 700}
}
FREE_BOOTHS = 5  

# Function to parse CSV data as well as removing invalid/ irrelevant data
def parse_csv_data_with_anomaly_check(file_path):
    valid_appointments = []
    with open(file_path, newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            try:
                call_time_str, request_time_str, vehicle_type = row
                if vehicle_type not in VEHICLE_TYPES:
                    continue  # Skip rows with unknown vehicle types (file structure specific)
                call_time = datetime.strptime(call_time_str, '%Y-%m-%d %H:%M:%S')
                request_time = datetime.strptime(request_time_str, '%Y-%m-%d %H:%M:%S')
                
                # Check if call time is before or at the same time as request time, add
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


        # Check if the service is within operating hours
        service_time = VEHICLE_TYPES[vehicle_type]['service_time']
        end_time = request_time + timedelta(minutes=service_time)
        if request_time.hour < SERVICE_HOURS[0] or (end_time.hour > SERVICE_HOURS[1] or (end_time.hour == SERVICE_HOURS[1] and end_time.minute > 0)):
            turned_away_customers[vehicle_type] += 1
            
            lost_revenue += VEHICLE_TYPES[vehicle_type]['charge']
            continue

        start_minute = (request_time.hour * 60 + request_time.minute) - (SERVICE_HOURS[0] * 60)
        end_minute = start_minute + service_time

        # Try to allocate a free booth
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



