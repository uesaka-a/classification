import os
import cv2
import numpy as np
from sklearn.linear_model import LogisticRegression
import joblib

def load_images(folder, label):
    data = []
    labels = []
    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        img = cv2.imread(path)
        if img is None:
            continue
        img = cv2.resize(img, (64, 64))
        img = img.flatten()
        data.append(img)
        labels.append(label)
    return data, labels

cat_data, cat_labels = load_images("data/cat", 0)
dog_data, dog_labels = load_images("data/dog", 1)

X = np.array(cat_data + dog_data)
y = np.array(cat_labels + dog_labels)

model = LogisticRegression(max_iter=1000)
model.fit(X, y)

joblib.dump(model, "model.pkl")
print("モデル保存完了")