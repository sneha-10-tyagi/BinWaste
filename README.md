# 🗑️ Bin Waste Monitoring System

A real-time waste management system that monitors bin fill levels using an **ultrasonic sensor and Arduino**, classifies the status using a machine learning model, and visualizes the system via a **Streamlit Dashboard** for authorities. It also includes a public-facing website with a query form to engage citizens in smart waste reporting.

---

## 🚀 Features

- 📡 **Real-time bin monitoring** using **Arduino + Ultrasonic sensor**
- 🧠 **ML-based classification**:
  - `Empty`: 0.0%
  - `Normal`: < 74.0%
  - `Warning`: 74.0% – 85.0%
  - `Alert`: > 85.0%
- 🗂️ **Self-generated dataset** with 2,711 entries
- ✅ **Classification model** achieving **98% accuracy**
- 📊 **Streamlit dashboard** for municipal authorities
- 📬 **Query form** for public interaction
- 🌐 **Website interface** with project info & public access

---

## 💻 Tech Stack

| Layer            | Tools Used                                 |
|------------------|---------------------------------------------|
| **Hardware**     | Arduino, Ultrasonic Sensor                  |
| **Backend/ML**   | Python, Pandas, Scikit-learn                |
| **Dashboard**    | Streamlit                                   |
             

---

## 🧠 ML Model

A classification model trained on the self-generated dataset to determine bin status in real-time.

**Model Performance:**
- Accuracy: **98%**
- Input Features: Fill percentage, location, timestamp
- Output: `Empty`, `Normal`, `Warning`, or `Alert`

---

## 📺 Dashboard 

- Real-time updates based on live sensor readings
- Status messages with color-coded classification
- Display tailored for municipal authority use

---

## 🌐 Website & Public Feedback

- 📄 A **public-facing website** to raise awareness about smart waste management
- ✉️ **Feedback form** that allows citizens to:
  - Register complaints (e.g., missed pickups, overfilled bins)
  - Request installation of new bins in specific areas
- 🗃️ All feedback is **stored in a backend SQLite database** for further processing and municipal action
- 📁 Includes a **"More" section** with additional information and updates
- 🗺️ **Planned Feature**:  
  An **interactive map interface** where users can view real-time bin locations in their area by clicking on regions
---

