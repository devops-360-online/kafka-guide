# Instructions for Setting Up the Environment

### 1. Install Required Packages

```bash
pip3 install -r requirements.txt
```

### 2. Run Producers
Open two separate terminals and run the following commands in each:

- **Terminal 1: Run Bus 1 Producer**
  ```python3 producer-bus1.py```

- **Terminal 2: Run Bus 2 Producer**
  ```python3 producer-bus2.py```

### 3. Run Consumer
To process the data from the producers, run the consumer script:

```python3 main.py```

### 4. Create a Mapbox Account
To use map visualizations, create an account to obtain a public token:

- Sign up at [Mapbox Account](https://account.mapbox.com/)

### 5. Learn More About Using Leaflet for Maps
For a quick start on implementing Leaflet in your projects, refer to:

- [Leaflet Quick Start Guide](https://leafletjs.com/examples/quick-start/)
