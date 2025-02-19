import matplotlib.pyplot as plt
import numpy as np
from flask import Flask, Response
import io

app = Flask(__name__)

@app.route('/base-distribution')
def base_distribution():
    # Generating random data
    np.random.seed(0)
    data = np.random.normal(0, 1, 100)  # Generate 100 random numbers from a normal distribution

    # Creating the box plot
    plt.figure(figsize=(10, 5.5))
    plt.boxplot(data)

    # Adding title and labels
    plt.title('Box Plot Example')
    plt.ylabel('Values')

    # Save the plot to a BytesIO object in SVG format
    output = io.BytesIO()
    plt.savefig(output, format='svg')
    plt.close()  # Close the figure to free memory
    output.seek(0)  # Rewind the data

    # Return the SVG image as a response
    return Response(output.getvalue(), mimetype='image/svg+xml')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
