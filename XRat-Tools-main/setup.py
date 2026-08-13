import os
import time
import webbrowser

os.system("pip install -r requirements.txt")
print()

print("Packages have been installed successfully.")

site_url = "https://guns.lol/3.vlt"
print(f"Opening {site_url}...")
webbrowser.open(site_url)

choice = input("Do you want to launch the menu now? (y/n) : ")

if choice.lower() == 'y':
    print("Launching the menu...")
    os.system("python Xrat.py")
elif choice.lower() == 'n':
    print("See you soon...")
    time.sleep(1)
    exit()
else:
    exit()