import threading
import random
from os import getcwd

from internet_check import is_Online
from Alert import Alert
from Data.DLG_Data import online_dlg, offline_dlg
from co_brain import Jarvis
from TextToSpeech.Fast_DF_TTS import speak
from Automation.Battery import check_plug
from Time_Operations.throw_alert import check_schedule, check_Alam

# Define file paths
ALARM_PATH = f"{getcwd()}\\Alam_data.txt"
SCHEDULE_PATH = f'{getcwd()}\\schedule.txt'

# Choose random dialogues
ran_online_dlg = random.choice(online_dlg)
ran_offline_dlg = random.choice(offline_dlg)

def online_tasks():
    """Function to handle tasks when online."""
    threads = [
        threading.Thread(target=speak, args=(ran_online_dlg,)),
        threading.Thread(target=check_plug),
        threading.Thread(target=check_schedule, args=(SCHEDULE_PATH,)),
        threading.Thread(target=Jarvis),
        threading.Thread(target=check_Alam, args=(ALARM_PATH,))
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

def main():
    """Main function to check internet connection and perform tasks."""
    if is_Online():
        online_tasks()
    else:
        Alert(ran_offline_dlg)

if __name__ == "__main__":
    main()
