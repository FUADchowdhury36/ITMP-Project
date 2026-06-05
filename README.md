ITMP — How to Run
==================

REQUIREMENTS
- Python 3.12+ (python.org/downloads) — tick "Add python.exe to PATH" during install
- Git (optional, for cloning)


FIRST-TIME SETUP (do once)
---------------------------
1. cd ITMPProject
2. python -m venv venv
3. venv\Scripts\activate          (Mac/Linux: source venv/bin/activate)
4. pip install django python-decouple thefuzz
5. python manage.py migrate
6. python manage.py shell < ITMPApp/generate_data.py   (loads sample data)


EVERY TIME — START THE SERVER
------------------------------
1. cd ITMPProject
2. venv\Scripts\activate
3. python manage.py runserver
4. Open http://127.0.0.1:8000 in browser

Keep the terminal open while using the app. Press Ctrl+C to stop.


TEST ACCOUNTS (password: test12345)
--------------------------------------
Candidate : sam.naf36@outlook.com
Employer  : naf.sam36@yahoo.com


COMMON ERRORS
--------------
"python not recognized"     → reinstall Python, tick "Add to PATH"
"execution policy" error    → run: Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
"No module named django"    → venv not active; run venv\Scripts\activate then pip install again
"Port already in use"       → run: python manage.py runserver 8001, then open :8001
"Site can't be reached"     → server not running; run manage.py runserver and keep terminal open
