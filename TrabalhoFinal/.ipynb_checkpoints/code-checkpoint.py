import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
from keras import layers
from keras.preprocessing import image
import os
import cv2



# 1. creating directories for storing training, testing and validation data in resp class_names subdirectories
# 2. prepare_data reads images, converts into suitable scale and flips them if needed (in case of training data) and saves them.
# 3. train_cnt == # training data points
# 4. val_cnt = # val_data data points (images)
# Rest will be testing data

# Cria as pastas com os dados do modelo
os.makedirs('images/training/covid',exist_ok = True)
os.makedirs('images/training/normal',exist_ok = True)
os.makedirs('images/testing/covid',exist_ok = True)
os.makedirs('images/testing/normal',exist_ok = True)
os.makedirs('images/validation/covid',exist_ok = True)
os.makedirs('images/validation/normal',exist_ok = True)

def prepare_data(pre,des,train_cnt,val_cnt):
    for file in os.listdir(pre+'/images'):
        
        image = cv2.resize(cv2.imread(pre+'/images/'+file),(256,256))
        mask = cv2.resize(cv2.imread(pre+'/masks/'+file),(256,256))
        image *= mask
        
        if(train_cnt > 0) : 
            cv2.imwrite('images/training/'+des+'/'+file,image)
            if(des == 'covid') : cv2.imwrite('images/training/'+des+'/flipped_'+file,image[:,::-1,:])
            train_cnt -= 1
        elif (val_cnt > 0):
            cv2.imwrite('images/validation/'+des+'/'+file,image)
            if(des == 'covid') : cv2.imwrite('images/validation/'+des+'/flipped_'+file,image[:,::-1,:])
            val_cnt -= 1
        else:
            cv2.imwrite('images/testing/'+des+'/'+file,image)
            if(des == 'covid') : cv2.imwrite('images/testing/'+des+'/flipped_'+file,image[:,::-1,:])

pre = './covid-19_dataset'

train_cnt = len(os.listdir(pre+'/COVID/images'))
val_cnt = train_cnt*(0.15)
train_cnt -= 2*val_cnt
prepare_data(pre+'/COVID','covid',train_cnt,val_cnt)
               
train_cnt = len(os.listdir(pre+'/Normal/images'))
val_cnt = train_cnt*(0.15)
train_cnt -= 2*val_cnt
prepare_data(pre+'/Normal','normal',train_cnt,val_cnt)



# Printing Total size of covid & normal dataset resp.

print(len(os.listdir('images/training/covid')),len(os.listdir('images/training/normal')))
print(len(os.listdir('images/validation/covid')),len(os.listdir('images/validation/normal')))
print(len(os.listdir('images/testing/covid')),len(os.listdir('images/testing/normal')))



covid = cv2.imread('./covid-19_dataset/COVID/images/COVID-1.png',cv2.IMREAD_GRAYSCALE)
covid_mask = cv2.imread('./covid-19_dataset/COVID/masks/COVID-1.png',cv2.IMREAD_GRAYSCALE)
covid1 = cv2.imread('images/training/covid/COVID-1.png',cv2.IMREAD_GRAYSCALE)

normal = cv2.imread('./covid-19_dataset/Normal/images/Normal-2.png',cv2.IMREAD_GRAYSCALE)
normal_mask = cv2.imread('./covid-19_dataset/Normal/masks/Normal-2.png',cv2.IMREAD_GRAYSCALE)
normal1 = cv2.imread('images/training/normal/Normal-2.png',cv2.IMREAD_GRAYSCALE)

plt.figure(figsize = (16,16))
plt.subplot(3,2,1)
plt.imshow(covid,cmap = 'gray')
plt.subplot(3,2,2)
plt.imshow(normal,cmap = 'gray')
plt.subplot(3,2,3)
plt.imshow(covid_mask,cmap = 'gray')
plt.subplot(3,2,4)
plt.imshow(normal_mask,cmap = 'gray')
plt.subplot(3,2,5)
plt.imshow(covid1,cmap = 'gray')
plt.xlabel('COVID',fontdict = {'size':25})
plt.subplot(3,2,6)
plt.imshow(normal1,cmap = 'gray')
plt.xlabel('NORMAL',fontdict = {'size':25})
plt.show()



# Building model 
# input shape (256,256,1) => cubic dimension, 2D image, 1 channels(1 unit - deapth)
# Model should be provided grayscale images

def build_model():
    input_layer = keras.Input(shape = (256,256,1)) 
    
    x = layers.Rescaling(1/255.)(input_layer)
    
    x = layers.Conv2D(64,(3,3),activation='relu',name = 'conv2d_2')(x)
    x = layers.MaxPooling2D(pool_size=(2,2))(x)
    x = layers.Dropout(0.5)(x)
    # randomly dropping some training points

    x = layers.Conv2D(128,(3,3),activation='relu',name = 'conv2d_3')(x)
    x = layers.MaxPooling2D(pool_size=(2,2))(x)
    x = layers.Dropout(0.5)(x)

    x = layers.Conv2D(256,(3,3),activation='relu',name = 'conv2d_4')(x)
    x = layers.MaxPooling2D(pool_size=(2,2))(x)
    x = layers.Dropout(0.5)(x)
    
    x = layers.Flatten()(x)
    x = layers.Dense(32,activation='relu',name = 'dense_1')(x)
    x = layers.Dropout(0.5)(x)
    output_layer = layers.Dense(1,activation='sigmoid',name = 'dense_2')(x)

    return keras.Model(input_layer,output_layer,name = 'model')



model = build_model()
model.summary()



# creating data generators

train_gen = image.ImageDataGenerator()
train_ds = train_gen.flow_from_directory(
    'images/training',
    target_size = (256,256),
    batch_size = 128,
    class_mode = 'binary',
    color_mode = 'grayscale'
)

val_gen = image.ImageDataGenerator()
val_ds = val_gen.flow_from_directory(
    'images/validation',
    target_size = (256,256),
    batch_size = 128,
    class_mode = 'binary',
    color_mode = 'grayscale'
)



model.compile(loss = 'binary_crossentropy',optimizer = 'Adam',metrics = ['accuracy'])

history = model.fit(
    train_ds,
    validation_data = val_ds,
    epochs = 30,
)



train_ds.class_indices , val_ds.class_indices



xtest = []
ytest = []

for file in os.listdir('images/testing/covid'):
    image = cv2.imread('images/testing/covid/'+file,cv2.IMREAD_GRAYSCALE)
    image = cv2.resize(image,(256,256))
    xtest.append(image)
    ytest.append(0)
    
for file in os.listdir('images/testing/normal'):
    image = cv2.imread('images/testing/normal/'+file,cv2.IMREAD_GRAYSCALE)
    image = cv2.resize(image,(256,256))
    xtest.append(image)
    ytest.append(1)
    
xtest = np.array(xtest)
ytest = np.array(ytest).reshape(-1,1)



# predicting classes on xtest images and then
# sigmoid gives final output as close to 0 or 1 (not exactly 0 or 1)
# so converting them into 0 or 1 on the basis of closeness

ypred = (model.predict(xtest) > 0.5)*1



# Finding accuracy on testing data

correct_pred = (ytest == ypred).sum()
print(100*correct_pred/(ytest.shape[0]))