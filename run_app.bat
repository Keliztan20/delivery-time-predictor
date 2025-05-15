@echo off

:: 1. Check if venv exists, if not create it
if not exist .\venv\ (
    echo Creating virtual environment...
    python -m venv venv
)

:: 2. Activate the virtual environment
call .\venv\Scripts\activate.bat

:: 3. Upgrade pip (inside venv, no --user needed)
python -m pip install --upgrade pip

:: 4. Install requirements (inside venv)
pip install -r requirements.txt

:: 5. Run Streamlit
streamlit run app.py

pause