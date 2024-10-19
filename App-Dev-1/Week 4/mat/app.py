from flask import Flask, render_template, request, send_file
import matplotlib.pyplot as plt
import numpy as np
import io

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the form data (e.g., a list of numbers to plot)
        data = request.form.get('data')
        
        # Convert the input data (comma-separated numbers) into a list of floats
        data = [float(i) for i in data.split(',')]
        
        # Create the histogram
        plt.figure()
        plt.hist(data, bins=10, edgecolor='black', alpha=0.7)
        plt.title('Histogram')
        plt.xlabel('Values')
        plt.ylabel('Frequency')
        
        # Save the plot to a BytesIO object and return it as a response
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plt.close()
        
        return send_file(img, mimetype='image/png')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)


# import matplotlib
# matplotlib.use("Agg")
# import matplotlib.pyplot as plt



# x=course_marks
# plt.clf()
# plt.hist(x)
# plt.savefig("static/hist.png")