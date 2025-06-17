import subprocess
import time
# Start Django server
django_server = subprocess.Popen(['python', 'manage.py', 'runserver'])
time.sleep(10)
# Start Streamlit server
streamlit_server = subprocess.Popen(['python','-m' , 'streamlit', 'run', 'dash.py'])
# Wait for both processes to finish
django_server.wait()
streamlit_server.wait()
