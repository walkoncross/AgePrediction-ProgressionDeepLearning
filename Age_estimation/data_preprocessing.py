import os
import re
import PIL
from PIL import Image
import numpy as np 
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D,Convoltion1D,MaxPooling1D
from keras.layers.normalization import BatchNormalization
from keras.regularizers import l2
from keras.optimizers import SGD,RMSprop
from keras.regularizers import l2, activity_l2,l1

new_path=os.path.join('.','aligned')
files=os.listdir(new_path)
len(files)
file=open('aligned_age.txt','r')
label_text=file.readlines()
len(label_text)

folder_names=[]
for i in files:
    image_path=os.path.join(new_path,i)
    folder_names.append(i)


 
for i in folder_names:
     print i



label_text_cleaned=[]
for i in label_text:
   label_text_cleaned.append(i.strip().split(' ')[0])



file_list=[]
file_list[:]=[]
for i in folder_names:	
    fdr_name=os.path.join('./aligned/',i+'/')
    list=os.listdir(os.path.join('./aligned/',i+'/'))
    for j in list:
        if j.replace('landmark_aligned_face.','') in label_text_cleaned:
           file_list.append(fdr_name+j.strip())


for i in file_list:
     print i.replace('landmark_aligned_face.','')


labels=[]
labels[:]=[]
for i in file_list:
     name=i.replace('face.','face~').split('~')[1]
     for j in label_text:
          l_name=j.strip().split(' ')[0]
          label=j.strip().split(' ')[1]
          if l_name==name:
              labels.append(int(label))



size=256,256
img_list=[]
img_list[:]=[]
for i in file_list:
     img=Image.open(i).convert('L')
     img.thumbnail(size,Image.ANTIALIAS)
     data = np.asarray( img, dtype="int32")
     data.shape
     img_list.append(data)


   
img_np_array=np.asarray(img_list)
img_np_array.shape

img_np_array_new=np.reshape(img_np_array,(17393,227,227,1)) 
img_np_array_new=np.reshape(img_np_array_new,(17393,1,227,227)) 

##

img_np_array_new=np.reshape(img_np_array,(17393,35,35,1)) 
img_np_array_new=np.reshape(img_np_array_new,(17393,1,35,35)) 
##

X_train=img_np_array_new[0:14000]
X_test=img_np_array_new[14000:17393]
label_np_array=np.asarray(labels)
label_np_array.shape

Y_train=label_np_array[0:14000]
Y_test=label_np_array[14000:17393]
y_train2=np_utils.to_categorical(Y_train,8)
y_test2=np_utils.to_categorical(Y_test,8)

model = Sequential()
# input: 100x100 images with 3 channels -> (3, 100, 100) tensors.
# this applies 32 convolution filters of size 3x3 each.
model.add(Convolution2D(32, 3, 3, border_mode='valid', input_shape=(1, 227, 227)))
model.add(Activation('relu'))
model.add(Convolution2D(32, 3, 3))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(BatchNormalization())
model.add(Dropout(0.25))

model.add(Convolution2D(64, 3, 3, border_mode='valid'))
model.add(Activation('relu'))
model.add(Convolution2D(64, 3, 3))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(1, 1)))
model.add(BatchNormalization())
model.add(Dropout(0.25))

model.add(Convolution2D(64, 3, 3, border_mode='valid'))
model.add(Activation('relu'))
model.add(Convolution2D(64, 3, 3))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(1, 1)))
model.add(BatchNormalization())
model.add(Dropout(0.25))

model.add(Convolution2D(128, 3, 3, border_mode='valid'))
model.add(Activation('relu'))
model.add(Convolution2D(128, 3, 3))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(BatchNormalization())
model.add(Dropout(0.25))

model.add(Convolution2D(256, 3, 3, border_mode='valid'))
model.add(Activation('relu'))
model.add(Convolution2D(256, 3, 3))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(BatchNormalization())
model.add(Dropout(0.25))

model.add(Convolution2D(384, 3, 3, border_mode='valid'))
model.add(Activation('relu'))
model.add(Convolution2D(384, 3, 3))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(BatchNormalization())
model.add(Dropout(0.25))

model.add(Convolution2D(384, 3, 3, border_mode='valid'))
model.add(Activation('relu'))
model.add(Convolution2D(384, 3, 3))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(BatchNormalization())
model.add(Dropout(0.25))

model.add(Flatten())
# Note: Keras does automatic shape inference.
model.add(Dense(256))
model.add(Activation('relu'))
model.add(Dropout(0.5))

model.add(Dense(256))
model.add(Activation('relu'))
model.add(Dropout(0.5))

model.add(Dense(8))
model.add(Activation('softmax'))

sgd = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd)

model.fit(X_train, y_train2, batch_size=32, nb_epoch=2,show_accuracy=True, verbose=2)
score = model.evaluate(X_test, Y_test2, batch_size=16)

json_string = model.to_json()
open('my_model_architecture_123.json', 'w').write(json_string)
model.save_weights('my_model_weights_new.h5')
