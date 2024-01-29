# Import necessary libraries
from flask import Flask, request, jsonify, render_template_string
import subprocess
import time
import Adafruit_DHT


# Initialize Flask app
app = Flask(__name__)

# HTML content for Home Page (index)
home_page_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Remote Lab</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            background-color: #f0f0f0;
        }

        .container {
            max-width: 500px;
            margin: 0 auto;
            padding: 20px;
            background-color: #ffffff;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
            border-radius: 5px;
            margin-top: 50px;
        }

        h1, h2 {
            color: #333;
        }

        a {
            display: block;
            margin: 10px 0;
            padding: 10px;
            background-color: #007BFF;
            color: #fff;
            text-decoration: none;
            border-radius: 5px;
            transition: background-color 0.3s;
        }

        a:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Welcome to the Remote Lab</h1>
        
        <!-- Lab List -->
        <h2>Lab List</h2>
        <a href="/computational_lab">Computational Power Lab</a>
        <a href="/temperature_lab">Temperature Remote Sensing Lab</a>
    </div>
</body>
</html>
"""

# HTML content for Computational Power Lab Page
computational_lab_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Computational Power Lab</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            background-color: #f0f0f0;
        }

        .container {
            max-width: 500px;
            margin: 0 auto;
            padding: 20px;
            background-color: #ffffff;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
            border-radius: 5px;
            margin-top: 50px;
        }

        h1, h2 {
            color: #333;
        }

        p {
            color: #555;
        }

        textarea {
            width: 100%;
            height: 200px;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
            margin-bottom: 10px;
        }

        button {
            background-color: #007BFF;
            color: #fff;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }

        #computationalOutput {
            margin-top: 10px;
            padding: 10px;
            background-color: #f9f9f9;
            border: 1px solid #ccc;
            border-radius: 5px;
        }

        #computationalExecutionTime {
            margin-top: 10px;
            color: #777;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Computational Power Lab</h1>
        <p>Perform computations and measure execution time:</p>
        <textarea id="computationalCode" placeholder="Enter Python code here"></textarea>
        <button onclick="executeComputationalCode()">Execute</button>
        <div id="computationalOutput"></div>
        <div id="computationalExecutionTime"></div>
    </div>
    
    <script>
        function executeComputationalCode() {
            const computationalCode = document.getElementById("computationalCode").value;

            fetch("/execute_computational", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ code: computationalCode }),
            })
            .then((response) => response.json())
            .then((data) => {
                document.getElementById("computationalOutput").innerText = data.output;
                document.getElementById("computationalExecutionTime").innerText = `Execution Time: ${data.execution_time}`;
            })
            .catch((error) => {
                console.error("Error:", error);
            });
        }
    </script>
</body>
</html>
"""

# HTML content for Temperature Remote Sensing Lab Page

temperature_lab_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Temperature Remote Sensing Lab</title>
    <style>
        /* (styles remain unchanged) */
    </style>
</head>
<body>
    <div class="container">
        <h1>Temperature Remote Sensing Lab</h1>
        <p>Real-time temperature and humidity:</p>
        <button onclick="getTemperatureReading()">Get Temperature Reading</button>
        <div id="temperatureReading"></div>
    </div>
    
    <script>
        function getTemperatureReading() {
            fetch("/get_temperature")
            .then(response => response.json())
            .then(data => {
                document.getElementById("temperatureReading").innerText = `Temperature: ${data.temperature}`;
            })
            .catch(error => {
                console.error("Error:", error);
            });
        }
    </script>
</body>
</html>
"""


# Define routes

# Home Page (index)
@app.route("/")
def index():
    return render_template_string(home_page_content)

# Computational Power Lab Page
@app.route("/computational_lab")
def computational_lab():
    return render_template_string(computational_lab_content)

# Temperature Remote Sensing Lab Page
@app.route("/temperature_lab")
def temperature_lab():
    return render_template_string(temperature_lab_content)

# Execute Computational Code

    
@app.route("/execute_computational", methods=["POST"])
def execute_computational_code():
    try:
        data = request.get_json()
        computational_code = data["code"]

        # Execute the computational code
        start_time = time.time()
        result = subprocess.check_output(["python3", "-c", computational_code], stderr=subprocess.STDOUT, text=True)
        end_time = time.time()

        execution_time = end_time - start_time

        return jsonify({"output": result.strip(), "execution_time": f"{execution_time:.5f} seconds"})
    except Exception as e:
        return jsonify({"error": str(e)})
    

    

# Simulate Temperature Reading
@app.route("/get_temperature", methods=["GET"])
def get_temperature_reading():
    # Read real-time temperature from DHT sensor
    DHT_SENSOR = Adafruit_DHT.DHT11
    DHT_PIN = 4
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    
    if humidity is not None and temperature is not None:
        temperature_reading = f"{temperature:.1f}°C, Humidity: {humidity:.1f}%"
        return jsonify({"temperature": temperature_reading})
    else:
        return jsonify({"error": "Sensor failure. Check wiring."})



# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080);
