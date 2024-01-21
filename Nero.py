import tensorflow 
from tensorflow import keras
from PIL import Image
import numpy as np

def classify(path):
	np.set_printoptions(suppress=True)
	model = tensorflow.keras.models.load_model('keras_model.h5', compile=False)
	data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32) #Это  массив numpy с формой (1, 224, 224, 3) и типом данных float32.
	image = Image.open(path)
	image = image.resize((224, 224))
	image_array = np.asarray(image)
	normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1 #normalized_image_array будет иметь значения пикселей от -1 до 1.
	data[0] = normalized_image_array
	prediction = model.predict(data) #прогнозирования с использованием предварительно обученной модели
	conclusion = ' '
	if prediction[0][0]>prediction[0][1]:
		print('Это кошка')
		conclusion = 'Это кошка'
	else:
		print('Это собака')
		conclusion = 'Это собака'
	return conclusion
	
	
	
	