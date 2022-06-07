# first neural network with keras tutorial
from numpy import loadtxt
from keras.models import Sequential
from keras.layers import Dense, Dropout
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import Normalizer
from sklearn import metrics

# load the dataset
dataset = loadtxt('Pistachio_28_Dataset.csv', delimiter=',')
# 0 == Kirmizi_Pistachio
# 1 == Siirt_Pistachio

# split into input (X) and output (y) variables
X = dataset[:,0:28]
y = dataset[:,28]

X = Normalizer().fit(X).transform(X)

# Semente aleatoria para fazer o embaralhamento 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42, shuffle=True)

# define the keras model
model = Sequential()
model.add(Dense(100, input_dim=X.shape[1], activation='relu'))
model.add(Dense(33, activation='relu'))
model.add(Dense(11, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

# compile the keras model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# fit the keras model on the dataset
fit = model.fit(
    x = X_train, 
    y = y_train, 
    epochs = 200, 
    validation_data=(X_test, y_test),
    batch_size = 100
)

# evaluate the keras model
_, accuracy = model.evaluate(X, y)
print('Accuracy: %.2f' % (accuracy*100))

pred = (model.predict(X_test) > 0.5).astype("int32")

plt.plot(fit.history['accuracy'])
plt.plot(fit.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

plt.plot(fit.history['loss'])
plt.plot(fit.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

cm = confusion_matrix(y_test, pred)
print("Matriz de confusão: \n", cm)

tn, fp, fn, tp = confusion_matrix(y_test, pred).ravel()

tpr = tp / (tp + fn)
tnr = tn / (tn + fp)
acc = (tp + tn) / (tp + tn + fp + fn)

print("TPR: ", tpr)
print("TNR: ", tnr)
print("ACC: %.2f" % (acc * 100))

fpr, tpr, thresholds = metrics.roc_curve(y_test, pred, pos_label=1)
auc = metrics.auc(fpr, tpr)

plt.plot([0, 1], [0, 1], linestyle='--', lw=2, color='r', label='Chance', alpha=.8)
plt.plot(fpr, tpr, color='b', label=r'ROC (AUC = %0.2f)' % (auc), lw=2, alpha=.8)
plt.suptitle('ROC Curve')
plt.xlabel('FPR')
plt.ylabel('TPR')
plt.legend(loc='lower right')
plt.show()



# # load the dataset
# dataset = loadtxt('/Rice_MSC_Dataset.csv', delimiter=',')
# # split into input (X) and output (y) variables
# X = dataset[:,0:106]
# y = dataset[:,106]
# # define the keras model
# model = Sequential()
# model.add(Dense(100, input_dim=106, activation='relu'))
# model.add(Dense(33, activation='relu'))
# model.add(Dense(11, activation='relu'))
# model.add(Dense(1, activation='sigmoid'))
# # compile the keras model
# model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# # fit the keras model on the dataset
# model.fit(
#     x = X_test, 
#     y = y_test, 
#     epochs = 150, 
#     batch_size= 100
# )
# # evaluate the keras model
# _, accuracy = model.evaluate(X, y)
# print('Accuracy: %.2f' % (accuracy*100))