# first neural network with keras tutorial
from numpy import loadtxt
from keras.models import Sequential
from keras.layers import Dense, Dropout
from sklearn.model_selection import learning_curve, train_test_split
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, label_ranking_average_precision_score
from sklearn.preprocessing import Normalizer
from sklearn import metrics

# Carrega o banco de dados com 28 atributos
dataset = loadtxt('Pistachio_28_Dataset.csv', delimiter=',')
# 0 == Kirmizi_Pistachio
# 1 == Siirt_Pistachio

# Separa os resultados de cada linha da base de dados
X = dataset[:,0:28]
y = dataset[:,28]

# Normalizacao dos dados
X = Normalizer().fit(X).transform(X)

# Divisao dos dados para treinamento (66,6%) e teste (33,3%) 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42, shuffle=True)

# Definicao do modelo keras (rede neural) com 4 camadas
model = Sequential()
model.add(Dense(100, input_dim=X.shape[1], activation='relu'))
model.add(Dense(33, activation='relu'))
model.add(Dense(11, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

# Compilacao do modelo
# Desempenho (AUC) de cada otimizador para 2000 epocas
# 1° - nadam - 0.88
# 2° - adam - 0.87
# 3° - adamax - 0.84
model.compile(loss='binary_crossentropy', optimizer="adam", metrics=['accuracy'])

# Treinamento do modelo com os dados de TREINAMENTO, validando o modelo com dados de TESTE
fit = model.fit(
    x = X_train, # Atributos de treinamento
    y = y_train, # Resultados de treinamento
    epochs = 20000, # Numero de "geracoes"
    validation_data=(X_test, y_test),
    batch_size = 256
)

# Retorna todas as classificacoes da amostra de teste (array de 0-1)
pred = (model.predict(X_test) > 0.5).astype("int32")

# Grafico de acuracia
plt.plot(fit.history['accuracy'])
plt.plot(fit.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

# Grafico de loss
plt.plot(fit.history['loss'])
plt.plot(fit.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

# Matriz de confusao, passando as classificacoes do dataset e do modelo
cm = confusion_matrix(y_test, pred)
print("\nMatriz de confusão:")
print("0) ", cm[0][0], " acertos, ", cm[0][1], " erros;")
print("1) ", cm[1][1], " acertos, ", cm[1][0], " erros;\n")

tn, fp, fn, tp = confusion_matrix(y_test, pred).ravel()

# Taxa de verdadeiro positivo, o quanto ele realmente acertou do que era positivo (classe 1)
tpr = tp / (tp + fn)

# Taxa de verdadeiro negativo, o quanto ele realmente acertou do que era negativo (classe 0)
tnr = tn / (tn + fp)

# Taxa de acuracia (acuracia simplesmente conta quantas classificacoes batem com os resultados do dataset)
acc = (tp + tn) / (tp + tn + fp + fn)

print("TPR (verdadeiro positivo): ", round(tpr,2))
print("TNR (verdadeiro negativo): ", round(tnr,2))
print("ACC (acuracia): %.2f\n" % (acc * 100))

# Grafico que mostra o quao bom eh o classificador. Quanto mais longe da linha tracejada, melhor eh o desempenho do classificador
fpr, tpr, thresholds = metrics.roc_curve(y_test, pred, pos_label=1)
auc = metrics.auc(fpr, tpr)

plt.plot([0, 1], [0, 1], linestyle='--', lw=2, color='r', label='Chance', alpha=.8)
plt.plot(fpr, tpr, color='b', label=r'ROC (AUC = %0.2f)' % (auc), lw=2, alpha=.8)
plt.suptitle('ROC Curve')
plt.xlabel('FPR')
plt.ylabel('TPR')
plt.legend(loc='lower right')
plt.show()
