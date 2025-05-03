# Bin Waste Monitoring System 🗑️

A real-time waste management system that monitors bin fill levels using an ultrasonic sensor and Arduino, triggers alerts, and visualizes data via a Streamlit dashboard with machine learning-based classification.

Features
- Real-time bin fill monitoring using Arduino + Ultrasonic sensor
- Status classification follows these thresholds: "Empty" (0.0%), "Normal" (<74.0%),"Warning" (74.0-85.0%), and "Alert" (>85.0%).
- Self-generated dataset with 2,711 entries
- Classification model with 98% accuracy
- Streamlit dashboard for authorities
- Query form for public interaction
- Website interface for basic information

Tech Stack
- Arduino
- Python (Pandas, Scikit-learn)
- Streamlit
- HTML/CSS/JS
- SQLite
