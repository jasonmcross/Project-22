import webbrowser
import time

url = "http://localhost:3000/"  

for i in range(250):
    webbrowser.open(url)

print("Link opened 250 times")
