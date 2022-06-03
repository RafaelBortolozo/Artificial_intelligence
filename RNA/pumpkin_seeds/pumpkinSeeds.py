# first neural network with keras tutorial
from numpy import loadtxt
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense

# load the dataset
dataset = loadtxt('Pumpkin_Seeds_Dataset/Pumpkin_Seeds_Dataset.csv', delimiter=',')
# 0 == Çerçevelik
# 1 == Ürgüp Sivrisi

# split into input (X) and output (y) variables
X = dataset[:,0:12]
y = dataset[:,12]

# Semente aleatoria para fazer o embaralhamento 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=True)

# define the keras model
model = Sequential()
model.add(Dense(100, input_dim=12, activation='relu'))
model.add(Dense(33, activation='relu'))
model.add(Dense(11, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

# compile the keras model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# fit the keras model on the dataset
model.fit(
    x = X, 
    y = y, 
    epochs = 200, 
    batch_size = 100,
    validation_split = 0.333
)


# evaluate the keras model
_, accuracy = model.evaluate(X, y)
print('Accuracy: %.2f' % (accuracy*100))

# load the dataset
dataset = loadtxt('Pumpkin_Seeds_Dataset/Pumpkin_Seeds_Dataset.csv', delimiter=',')
# split into input (X) and output (y) variables
X = dataset[:,0:12]
y = dataset[:,12]
# define the keras model
model = Sequential()
model.add(Dense(100, input_dim=12, activation='relu'))
model.add(Dense(33, activation='relu'))
model.add(Dense(11, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
# compile the keras model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# fit the keras model on the dataset
model.fit(
    x = X, 
    y = y, 
    epochs = 150, 
    batch_size= 100)
# evaluate the keras model
_, accuracy = model.evaluate(X, y)
print('Accuracy: %.2f' % (accuracy*100))