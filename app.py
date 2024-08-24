# app.py
from flask import Flask, render_template

app = Flask(__name__)

# Import the required functions from the provided Python files
from pyserver import dispTrains

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/display_trains')
def display_trains():
    trains_info = dispTrains()  # Call the dispTrains function from pyserver.py
    # Pass the trains_info to the HTML template for rendering
    return render_template('display_trains.html', trains_info=trains_info)

if __name__ == '__main__':
    app.run(debug=True)
