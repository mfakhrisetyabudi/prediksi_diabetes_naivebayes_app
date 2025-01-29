from flask import Flask, request, render_template
import pickle
import numpy as np

app = Flask(__name__)

# Load model Naive Bayes untuk prediksi diabetes
model_file = open('naive_bayes_diabetes.pkl', 'rb')
model = pickle.load(model_file, encoding='bytes')

@app.route('/')
def index():
    return render_template('index.html', hasil_prediksi=None)

@app.route('/predict', methods=['POST'])
def predict():
    '''
    Memprediksi kemungkinan diabetes berdasarkan input pengguna
    dan menampilkan hasil ke halaman HTML.
    '''
    try:
        # Mengambil 8 input dari form
        jenis_kelamin = request.form['jenis_kelamin']
        umur = int(request.form['umur'])  # Konversi ke bilangan bulat
        hipertensi = 1 if request.form['hipertensi'] == 'Ya' else 0
        jantung = 1 if request.form['jantung'] == 'Ya' else 0
        merokok = request.form['merokok']
        bmi = float(request.form['bmi'])
        hbA1c = float(request.form['hbA1c'])
        gula_darah = int(request.form['gula_darah'])  # Konversi ke bilangan bulat
        
        # Encoding data
        jenis_kelamin_encoded = 0 if jenis_kelamin == 'Laki-laki' else 1
        
        # Encoding riwayat merokok
        merokok_mapping = {
            "tidak pernah": 0,
            "saat ini": 2,
            "mantan perokok": 1,
            "pernah merokok": 2,
            "tidak saat ini": 0,
            "No Info": -1
        }
        merokok_encoded = merokok_mapping.get(merokok, -1)
        
        # Menyatukan semua fitur menjadi array numpy
        data = np.array([[jenis_kelamin_encoded, umur, hipertensi, jantung, merokok_encoded, bmi, hbA1c, gula_darah]])
        
        # Melakukan prediksi
        prediction = model.predict(data)
        
        # Menentukan output hasil prediksi
        hasil_prediksi = "Diabetes" if prediction[0] == 1 else "Tidak Diabetes"
        
        # Konversi hipertensi dan jantung ke Ya/Tidak
        hipertensi = "Ya" if hipertensi == 1 else "Tidak"
        jantung = "Ya" if jantung == 1 else "Tidak"
        
    except Exception as e:
        hasil_prediksi = f"Terjadi kesalahan: {str(e)}"
        
        # Kembalikan semua variabel ke bentuk semula sebelum return render_template
        hipertensi = request.form['hipertensi']
        jantung = request.form['jantung']
        jenis_kelamin = request.form['jenis_kelamin']
        merokok = request.form['merokok']
        bmi = request.form['bmi']
        hbA1c = request.form['hbA1c']
        gula_darah = request.form['gula_darah']
        umur = request.form['umur']
    
    return render_template('index.html', hasil_prediksi=hasil_prediksi, jenis_kelamin=jenis_kelamin, umur=umur, hipertensi=hipertensi, jantung=jantung, merokok=merokok, bmi=bmi, hbA1c=hbA1c, gula_darah=gula_darah)

if __name__ == '__main__':
    app.run(debug=True)