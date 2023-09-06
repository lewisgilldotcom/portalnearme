from flask import Flask, render_template, request
import csv
import math

app = Flask(__name__)

# Function to calculate the distance between two points in 3D space
def calculate_distance(x1, y1, z1, x2, y2, z2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)

# Load data from the CSV file into a list of dictionaries
stops = []
with open('/home/lewis/Documents/Nether_Highway_Stops.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        stops.append(row)

# Initialise user coords outside request method to ensure they are useable
user_x = None
user_y = None
user_z = None
nearest_stop = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    global user_x, user_y, user_z, nearest_stop  # Make user coordinates accessible globally

    if request.method == 'POST':
        try:
            #Get user coords
            user_x = float(request.form['x_coordinate'])
            user_y = float(request.form['y_coordinate'])
            user_z = float(request.form['z_coordinate'])

            # Filter out interchanges
            filtered_stops = [stop for stop in stops if "Interchange" not in stop['Name']]

            # Initialize variables to keep track of the nearest stop
            nearest_distance = float('inf')

            # Iterate through stops and find the nearest one
            for stop in filtered_stops:
                stop_x = float(stop['X']) * 8
                stop_y = float(stop['Y'])
                stop_z = float(stop['Z']) * 8
    
                distance = calculate_distance(user_x, user_y, user_z, stop_x, stop_y, stop_z)
    
                if distance < nearest_distance:
                    nearest_distance = distance
                    nearest_stop = stop

            # Escape user input when displaying it in the result template
            if nearest_stop is not None:
                return render_template('result.html', distance=distance, nearest_stop=nearest_stop)
            else:
                return render_template('result.html', distance=distance, nearest_stop={}, no_nearest=True)

        except ValueError:
            # Handle invalid input gracefully
            return render_template('error.html', message="Invalid input. Please enter valid numeric coordinates.")
    return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True)

# Print the nearest stop information
print(f"Nearest Stop Name: {nearest_stop['Name']}")
print(f"Nearest Stop Road: {nearest_stop['Road']}")
print(f"Nearest Stop X: {nearest_stop['X']}")
print(f"Nearest Stop Y: {nearest_stop['Y']}")
print(f"Nearest Stop Z: {nearest_stop['Z']}")

