import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf
import random
import os

st.set_page_config(page_title="Cat vs Dog Quiz", layout="centered")

st.markdown("""
<style>
button[kind="primary"] {
    background-color: #2da44e;
    color: white;
    border-radius: 6px;
    height: 3em;
    width: 100%;
}
img {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    return tf.keras.applications.MobileNetV2(weights="imagenet")

model = load_model()

def get_random_image():
    label = random.choice(["cat", "dog"])
    folder = f"data/{label}"
    file = random.choice(os.listdir(folder))
    return os.path.join(folder, file), label

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
    img = image.resize((224, 224))
    img_array = np.array(img)
    img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
    img_array = np.expand_dims(img_array, axis=0)

    preds = model.predict(img_array)
    decoded = tf.keras.applications.mobilenet_v2.decode_predictions(preds, top=1)[0][0][1]

    if "dog" in decoded:
        model_pred = "Dog"
    elif "cat" in decoded:
        model_pred = "Cat"
    else:
        model_pred = "Unknown"

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