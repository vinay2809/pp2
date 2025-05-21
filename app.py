
import streamlit as st
import torch
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import sqlite3
from datetime import datetime

st.set_page_config(page_title="ManTra-Net Forgery Detection", layout="centered")
st.title("🔍 ManTra-Net Image Forgery Detection")

# Setup SQLite database
conn = sqlite3.connect('results.db')
c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS detections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT,
    detected_forgery INTEGER,
    timestamp TEXT
)
''')
conn.commit()

def save_result(filename, is_forgery):
    now = datetime.now().isoformat()
    c.execute('INSERT INTO detections (filename, detected_forgery, timestamp) VALUES (?, ?, ?)',
              (filename, int(is_forgery), now))
    conn.commit()

# Load model placeholder (user should insert actual model loading)
@st.cache_resource
def load_model():
    # Replace with your actual model loading code
    return None  # torch.load("ManTraNet_Pytorch_Pretrained_Model.pth")

model = load_model()

uploaded_file = st.file_uploader("Upload an image for forgery detection", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    image_np = np.array(image)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # --- Placeholder Detection Logic ---
    # Replace this with ManTra-Net's actual prediction logic
    detected_forgery = np.random.choice([0, 1])  # Dummy result for demo

    # Show result
    st.markdown(f"### 🔎 Forgery Detected: {'✅ Yes' if detected_forgery else '❌ No'}")

    # Save result to database
    save_result(uploaded_file.name, detected_forgery)

# Show history from database
st.subheader("🗂️ Detection History")
rows = c.execute('SELECT * FROM detections ORDER BY timestamp DESC').fetchall()
for row in rows:
    st.write(f"📁 {row[1]} — Forgery: {'Yes' if row[2] else 'No'} — 🕒 {row[3]}")
