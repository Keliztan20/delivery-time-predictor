@echo off
pip install --upgrade pip
pip install -r requirements.txt
python assets\LightGBM.py
streamlit run app.py
