# Python Simulated IoT Device

A Python-based IoT device simulator that connects to an MQTT broker using credentials obtained from a device hub API.

[Device Hub API](https://kernopy-edge-hub.azurewebsites.net/docs)


## Features

- Simulates IoT device behavior with configurable parameters
- Securely connects to Kernopy MQTT broker using TLS
- Generates random sensor data values
- Configurable message frequency and count
- Automatic credential and configuration management via [device hub API](https://kernopy-edge-hub.azurewebsites.net/docs)

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/simulated-device-python.git
cd simulated-device-python
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root with the following variables:

```env
DEVICE_HUB_URL=<your-device-hub-api-url>
DEVICE_ID=<your-device-id>
DEVICE_PRIMARY_KEY=<your-device-primary-key>
MAX_MESSAGES=100
TIME_DELAY=5
```

## Usage

Run the simulator:

```bash
python main.py
```

The simulator will:
1. Connect to the device hub API to get MQTT credentials and device config parameters
2. Establish a secure MQTT connection
3. Generate and publish simulated sensor data
4. Continue publishing based on MAX_MESSAGES and TIME_DELAY settings

## Data Format

The simulator publishes messages in the following JSON format:

```json
{
    "edge_ts": "2024-03-16T12:34:56.789",
    "data": [
        {
            "parameter": "sensor1",
            "value": 45.67
        },
        {
            "parameter": "sensor2",
            "value": 78.90
        }
    ]
}
```

## Error Handling

- The simulator includes error handling for API connections
- TLS security for MQTT connections
- Automatic reconnection attempts on connection loss

