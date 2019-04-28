#----------------------- -------------------------------------
#   coding:utf-8
#------------------------------------------------------------
#	Updata History
#	December  06  16:00, 2018 (Thu) by S.Iwamaru
#------------------------------------------------------------
#
#	AutoEncoder
#		https://blog.keras.io/building-autoencoders-in-keras.html
#------------------------------------------------------------

from keras.layers import Input, Dense
from keras.models import Model

"""
	モデル構築
"""
encoding_dim = 32
input_img = Input(shape=(784,))

#  Encode部分
encoded = Dense(encoding_dim, activation="relu")(input_img)
encoder = Model(input_img, encoded)

#  Decode部分
decoded = Dense(784, activation="sigmoid")(encoded)

autoencoder = Model(input_img, decoded)


encoded_input = Input(shape=(encoding_dim,))
decoder_layer = autoencoder.layers[-1]
decoder = Model(encoded_input, decoder_layer(encoded_input))


"""
	モデルコンパイル
"""
autoencoder.compile(optimizer="adadelta",
		loss="binary_crossentropy")
					
"""
	データ読み込み
"""
from keras.datasets import mnist
import numpy as np

(x_train, _), (x_test, _) = mnist.load_data()

x_train = x_train.astype("float32") / 255.
x_test = x_test.astype("float32") / 255.
x_train = x_train.reshape((len(x_train), np.prod(x_train.shape[1:])))
x_test = x_test.reshape((len(x_test), np.prod(x_test.shape[1:])))

autoencoder.fit( x_train, x_train,
				 epochs=50,
				 batch_size=256,
				 shuffle=True,
				 validation_data=(x_test, x_test))
				 
encoded_imgs = encoder.predict(x_test)
decoded_imgs = decoder.predict(encoded_imgs)

"""
	データの可視化
"""
import matplotlib.pyplot as plt

n = 10
plt.figure(figsize=(20, 4))
for i in range(n):
	#  display original
	ax = plt.subplot(2, n, i + 1)
	plt.imshow(x_test[i].reshape(28, 28))
	plt.gray()
	ax.get_xaxis().set_visible(False)
	ax.get_yaxis().set_visible(False)
	
	
	ax = plt.subplot(2, n, i + 1 + n)
	plt.imshow(decoded_imgs[i].reshape(28, 28))
	plt.gray()
	ax.get_xaxis().set_visible(False)
	ax.get_yaxis().set_visible(False)
plt.show()
