import streamlit as st
import numpy as np
from PIL import Image
import random
import os
import joblib
import cv2

st.set_page_config(page_title="Cat vs Dog Quiz", layout="centered")

@st.cache_resource
def load_model():
    return joblib.load("model.pkl")

model = load_model()

def get_random_image():
    label = random.choice(["cat", "dog"])
    folder = f"data/{label}"
    file = random.choice(os.listdir(folder))
    return os.path.join(folder, file), label

def preprocess(image):
    img = np.array(image)
    img = cv2.resize(img, (64, 64))
    img = img.flatten()
    return img.reshape(1, -1)

if "image_path" not in st.session_state:
    path, label = get_random_image()
    st.session_state.image_path = path
    st.session_state.label = label
    st.session_state.answered = False

st.title("🐶🐱 Cat or Dog Quiz")

image = Image.open(st.session_state.image_path).convert("RGB")
st.image(image, use_column_width=True)

user_choice = st.radio("選択してください", ["Dog", "Cat"])

if st.button("判定"):
    img = preprocess(image)
    pred = model.predict(img)[0]

    model_pred = "Dog" if pred == 1 else "Cat"
    correct_label = st.session_state.label.capitalize()

    st.markdown("---")
    st.write(f"あなた：**{user_choice}**")
    st.write(f"モデル：**{model_pred}**")
    st.write(f"正解　：**{correct_label}**")

    if user_choice == correct_label:
        st.success("正解")
    else:
        st.error("不正解")

    st.session_state.answered = True

if st.session_state.answered:
    if st.button("次の問題"):
        path, label = get_random_image()
        st.session_state.image_path = path
        st.session_state.label = label
        st.session_state.answered = False
        st.rerun()