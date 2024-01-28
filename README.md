``` 
#████████╗███████╗░█████╗░███╗░░░███╗  ███╗░░██╗██╗███╗░░░███╗██████╗░██╗░░░██╗░██████╗
#╚══██╔══╝██╔════╝██╔══██╗████╗░████║  ████╗░██║██║████╗░████║██╔══██╗██║░░░██║██╔════╝
#░░░██║░░░█████╗░░███████║██╔████╔██║  ██╔██╗██║██║██╔████╔██║██████╦╝██║░░░██║╚█████╗░
#░░░██║░░░██╔══╝░░██╔══██║██║╚██╔╝██║  ██║╚████║██║██║╚██╔╝██║██╔══██╗██║░░░██║░╚═══██╗
#░░░██║░░░███████╗██║░░██║██║░╚═╝░██║  ██║░╚███║██║██║░╚═╝░██║██████╦╝╚██████╔╝██████╔╝
#░░░╚═╝░░░╚══════╝╚═╝░░╚═╝╚═╝░░░░░╚═╝  ╚═╝░░╚══╝╚═╝╚═╝░░░░░╚═╝╚═════╝░░╚═════╝░╚═════╝░
#──────▄▀▄─────▄▀▄         ----------------------------------------------------------
#─────▄█░░▀▀▀▀▀░░█▄                            Team Members
#─▄▄──█░░░░░░░░░░░█──▄▄  Sisagha Phimmasone | Mustafa Ahmad | Cleopatr-Aliak Manoukian
#█▄▄█─█░░▀░░┬░░▀░░█─█▄▄█   ----------------------------------------------------------
```
# ConUHacks SAP Scheduling Tool Final Submission

The ConUHacks SAP Scheduling Tool is a web application designed to optimize the scheduling of tire change services for a variety of vehicle types. This tool helps tire change shops to efficiently manage their appointments, track revenue, and analyze service data for business insights.

## Features

- **Optimized Scheduling Algorithm**: Allocates service appointments to minimize wait times and ensure availability across different vehicle types.
- **Dynamic Time Slot Management**: Supports different servicing times for compact cars, medium cars, full-size cars, and class 1 & 2 trucks.
- **Revenue Tracking**: Calculates the total and lost revenue, providing valuable data for business analysis.
- **Anomaly Detection**: Filters out inconsistent or incorrect data entries during CSV file parsing.
- **Daily Initialization**: Resets booth availability daily, preventing rollover and ensuring fresh scheduling every day.
- **FIFO Booking Policy**: Implements a First In, First Out policy to manage overlapping bookings fairly.
- **Comprehensive Statistics**: Provides detailed statistics on serviced and turned away vehicles, including reasons for turn-aways.
- **Booth Utilization Insights**: Offers insights into booth utilization to optimize operational efficiency.
- **User-Friendly Interface**: Simple and intuitive user interface for uploading CSV files and reviewing scheduling outcomes.
- **CSV Data Processing**: Parses and processes appointment data from CSV files with robust error handling.
- **Flask-Based Web Application**: Built using Flask, a lightweight WSGI web application framework.

## Getting Started

To run this application on your local machine, follow these steps:

1. Ensure you have Python installed on your system.
2. Clone the repository to your local machine.
3. Navigate to the cloned directory and install the required dependencies using `pip install -r requirements.txt`.
4. Run the Flask app with `python app.py`.
5. Access the web application at `http://localhost:5000` in your web browser.

## Usage

1. Prepare a CSV file with appointment data in the format `call_timestamp, appointment_timestamp, vehicle_type`.
2. Navigate to the web application's home page.
3. Click the file upload area to select and upload your CSV file.
4. Review the generated statistics and insights after processing.

## Contributing

Contributions are welcome. If you would like to contribute:

* Fork the repository.
* Create a new feature branch (git checkout -b feature/YourFeature).
* Commit your changes (git commit -m 'Add some YourFeature').
* Push to the branch (git push origin feature/YourFeature).
* Open a new Pull Request.

## Acknowledgments

- ConUHacks 2024 Nimbus Team Members: Sisagha Phimmasone, Mustafa Ahmad, Cleopatr-Aliak-Manoukian for their contributions and dedication to the project.

