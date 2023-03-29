from flask import Flask, render_template, jsonify, request
from matplotlib.figure import Figure
import io
from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import base64
import numpy as np
import matplotlib.pyplot as plt
import control.matlab as cm

app = Flask(__name__, template_folder=('C:\WebDev\Development'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_data_A', methods=['POST'])
def process_data():
   values = []
   for key, value in request.form.items():
       values.append(value)
   A = np.array([[float(values[0]), float(values[1]), float(values[2])], 
                 [float(values[3]), float(values[4]), float(values[5])], 
                 [float(values[6]), float(values[7]), float(values[8])]])
   
#    A = np.array([[12, 13, 14], 
#                  [15, 15, 16], 
#                  [20, 21, 22]])
   
   B = np.array([[float(values[9])],
                 [float(values[10])],
                 [float(values[11])]])
   
#    B = np.array([[1],
#                  [0],
#                  [0]])
   

   C = np.array([[0,0,1]])

   D = np.array([[0]])

   sys = cm.ss(A, B, C, D)

   T = np.linspace(0, 100, 10)
#    _, yout, _ = cm.lsim(sys, T, [1,])
   yout, T = cm.step(sys)
   fig, ax = plt.subplots()
   ax.plot(T, yout)
   ax.set_xlabel('Time(s)')
   ax.set_ylabel('Output')
   img = BytesIO()
#    FigureCanvas(fig).print_png(img)
#    return img.getvalue()

   fig.savefig(img, format='png')
   img.seek(0)
   data = base64.b64encode(img.getbuffer()).decode("ascii")
   return render_template('index.html', plot_url=data)

   #ini beda returny
   # return f"<img src='data:image/png;base64,{data}'/>"


if __name__ == '__main__':
    app.run(debug=True)