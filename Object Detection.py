#!/usr/bin/env python
# coding: utf-8

# ### Loading Libraries

# In[1]:


import cv2
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()


# In[2]:


from keras.datasets import cifar10
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import confusion_matrix
from keras.layers import Conv2D, MaxPool2D, Flatten, Dense, Dropout
from keras.models import Sequential, load_model
from keras.callbacks import EarlyStopping


# ### Loading Dataset

# In[3]:


(X_train, y_train), (X_test, y_test) = cifar10.load_data()


# In[4]:


labels = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']


# ### Images Preprocessing

# In[5]:


# Display the first 21 images of X_train

fig, axes = plt.subplots(ncols=7, nrows=3, figsize=(17, 8))
index = 0
for i in range(3):
    for j in range(7):
        axes[i,j].set_title(labels[y_train[index][0]])
        axes[i,j].imshow(X_train[index])
        axes[i,j].get_xaxis().set_visible(False)
        axes[i,j].get_yaxis().set_visible(False)
        index += 1
plt.show()


# In[6]:


# Convert both X_train and X_test to grayscale

X_train = np.array([cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) for image in X_train])
X_test = np.array([cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) for image in X_test])


# In[7]:


# Display the first 21 images of X_train (grayscale)

fig, axes = plt.subplots(ncols=7, nrows=3, figsize=(17, 8))
index = 0
for i in range(3):
    for j in range(7):
        axes[i,j].set_title(labels[y_train[index][0]])
        axes[i,j].imshow(X_train[index], cmap='gray')
        axes[i,j].get_xaxis().set_visible(False)
        axes[i,j].get_yaxis().set_visible(False)
        index += 1
plt.show()


# In[8]:


# Value normalization
X_train  = X_train/255
X_test  = X_test/255


# In[9]:


# Label preprocessing
one_hot_encoder = OneHotEncoder(sparse=False)


# In[10]:


one_hot_encoder.fit(y_train)


# In[11]:


y_train = one_hot_encoder.transform(y_train)
y_test = one_hot_encoder.transform(y_test)


# In[12]:


# Defining input shape for CNN
X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], X_train.shape[2], 1)
X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], X_test.shape[2], 1)


# In[13]:


input_shape = (X_train.shape[1], X_train.shape[2], 1)


# ### Constructing CNN model

# In[14]:


model = Sequential()
model.add(Conv2D(16, (3, 3), activation='relu', strides=(1, 1), 
    padding='same', input_shape=input_shape))
model.add(Conv2D(32, (3, 3), activation='relu', strides=(1, 1), 
    padding='same'))
model.add(Conv2D(64, (3, 3), activation='relu', strides=(1, 1), 
    padding='same'))
model.add(MaxPool2D((2, 2)))
model.add(Conv2D(16, (3, 3), activation='relu', strides=(1, 1), 
    padding='same'))
model.add(Conv2D(32, (3, 3), activation='relu', strides=(1, 1), 
    padding='same'))
model.add(Conv2D(64, (3, 3), activation='relu', strides=(1, 1), 
    padding='same'))
model.add(MaxPool2D((2, 2)))
model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(128, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(10, activation='softmax'))


# In[15]:


model.compile(loss='categorical_crossentropy', 
     optimizer='adam',
     metrics=['acc'])


# In[16]:


es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=3)


# ### Model training

# In[17]:


history = model.fit(X_train, y_train, epochs=20, batch_size=32, validation_data=(X_test, y_test), callbacks=[es])


# ### Loading model

# In[18]:


model.save('CNN_CIFAR.h5')
model = load_model('CNN_CIFAR.h5')


# In[19]:


# Model evaluation
plt.title('Accuracy Score')
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.show()


# In[20]:


plt.title('Loss Values')
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.show()


# ### Predicting test data

# In[21]:


predictions = model.predict(X_test)
predictions = one_hot_encoder.inverse_transform(predictions)


# In[22]:


y_test = one_hot_encoder.inverse_transform(y_test)


# ### Confusion matrix

# In[23]:


cm = confusion_matrix(y_test, predictions)


# In[24]:


plt.figure(figsize=(9,9))
sns.heatmap(cm, cbar=False, xticklabels=labels, yticklabels=labels, fmt='d', annot=True, cmap=plt.cm.Blues)
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.show()


# In[25]:


# Displaying test data with its actual and predicted label
X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], X_test.shape[2])


# In[26]:


y_test = y_test.astype(int)
predictions = predictions.astype(int)


# In[27]:


fig, axes = plt.subplots(ncols=7, nrows=3, sharex=False,
    sharey=True, figsize=(17, 8))
index = 0
for i in range(3):
    for j in range(7):
        axes[i,j].set_title('actual:' + labels[y_test[index][0]] + '\n' 
                            + 'predicted:' + labels[predictions[index][0]])
        axes[i,j].imshow(X_test[index], cmap='gray')
        axes[i,j].get_xaxis().set_visible(False)
        axes[i,j].get_yaxis().set_visible(False)
        index += 1
plt.show()

