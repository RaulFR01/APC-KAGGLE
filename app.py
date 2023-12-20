from flask import Flask, render_template, request, send_from_directory, url_for
from keras.preprocessing import image
from keras.models import load_model
import numpy as np
import keras
import os
app = Flask(__name__)

fotosFolder = "static/fotos"
app.config['fotosFolder'] = fotosFolder
app.config['SECRET_KEY'] = 'oq_=HU>N(ZtufoB'
model = load_model("models/modeloAPC.h5")


@app.route("/upload", methods=['GET','POST'])
def uploadFoto():
    if request.method == 'POST':
        if request.files:

            foto = request.files['foto']

            print(foto)

    foto = request.files['foto']
    ruta = os.path.join(app.config['fotosFolder'], foto.filename)
    foto.save(ruta)
    
    img = image.load_img(ruta, target_size=(256,256))

    img_array = image.img_to_array(img) / 255.0

    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)
    predictedClass = np.argmax(prediction)
    if predictedClass == 0:
        prediccion = 'Fresh Apple'
    elif predictedClass == 1:
        prediccion ='Fresh Banana'
    elif predictedClass == 2:
        prediccion ='Fresh Orange'
    elif predictedClass == 3:
        prediccion ='Rotten Apple'
    elif predictedClass == 4:
        prediccion ='Rotten Banana'
    elif predictedClass == 5:
        prediccion ='Rotten Orange'

    return render_template('index.html', foto=foto.filename, prediccion = prediccion)
@app.route('/selectFoto/<nombre_foto>')
def selectFoto(nombre_foto):
    ruta_completa = os.path.join(app.config['fotosFolder'], nombre_foto)
    return ruta_completa
@app.route("/")
def helloWorld():

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)