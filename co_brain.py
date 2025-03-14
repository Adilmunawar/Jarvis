import logging
import threading
import random

from Automation.Automation_Brain import Auto_main_brain, clear_file
from NetHyTechSTT.listen import listen
from TextToSpeech.Fast_DF_TTS import speak
from Data.DLG_Data import online_dlg, offline_dlg
from Automation.Battery import battery_Alert
from Time_Operations.brain import input_manage, input_manage_Alam
from Brain.brain import Main_Brain
from Features.create_file import create_file
from Vision.Vbrain import *
from Vision.MVbrain import *
from Weather_Check.check_weather import get_weather_by_address
from Whatsapp_automation.wa import send_msg_wa
from TextToImage.gen_image import generate_image
from Features.mike_health import mike_health
from Features.speaker_health import speaker_health_test
from Features.br_persentage import check_br_persentage
from Features.set_br import set_brightness_windows
from Features.set_get_volume import *
from Features.check_running_app import *

# Constants
INPUT_FILE = 'input.txt'
LOG_FILE = 'log.txt'
NUMBERS = ["1:", "2:", "3:", "4:", "5:", "6:", "7:", "8:", "9:"]
SPL_NUMBERS = ["11:", "12:"]

# Configure logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(message)s')

def log_message(user_text, response):
    logging.info('You: %s', user_text)
    logging.info('Jarvis: %s', response)

def check_inputs():
    """Monitors the input file and processes commands."""
    output_text = ""
    while True:
        try:
            with open(INPUT_FILE, "r") as file:
                input_text = file.read().lower()
            if input_text != output_text:
                output_text = input_text
                process_input(output_text)
        except Exception as e:
            logging.error("Error while reading input file: %s", e)

def process_input(output_text):
    """Processes the input text and triggers corresponding actions."""
    if output_text.startswith("tell me"):
        output_text = normalize_time_format(output_text)
        if any(spl_num in output_text for spl_num in SPL_NUMBERS):
            input_manage(output_text)
        else:
            for number in NUMBERS:
                if number in output_text:
                    output_text = output_text.replace(number, f"0{number}")
                    input_manage(output_text)
        clear_file()

    elif output_text.startswith("set alarm"):
        output_text = normalize_time_format(output_text)
        if any(spl_num in output_text for spl_num in SPL_NUMBERS):
            input_manage_Alam(output_text)
        else:
            for number in NUMBERS:
                if number in output_text:
                    output_text = output_text.replace(number, f"0{number}")
                    input_manage_Alam(output_text)
        clear_file()

    elif "jarvis" in output_text:
        response = Main_Brain(output_text)
        log_message(output_text, response)
        speak(response)

    elif output_text.startswith("create") and "file" in output_text:
        create_file(output_text)

    elif "what is this" in output_text or "what can you see" in output_text:
        handle_vision_command()

    elif "check weather" in output_text:
        text = output_text.replace("check weather in", "").strip()
        ans = get_weather_by_address(text)
        speak(ans)

    elif "send message on whatsapp" in output_text:
        send_msg_wa()

    elif "generate image" in output_text:
        text = output_text.replace("generate image", "").strip()
        generate_image(text)
        speak("Image generated successfully")

    elif "check mike" in output_text or "check mike health" in output_text:
        mike_health()

    elif "check speaker health" in output_text:
        speaker_health_test()

    elif "check brightness percentage" in output_text:
        check_br_persentage()

    elif "set brightness percentage" in output_text:
        set = output_text.replace("set brightness percentage", "").strip()
        set_brightness_windows(int(set))

    elif "check volume level" in output_text:
        get_volume_windows()

    elif "set volume level" in output_text:
        set = output_text.replace("set volume level", "").replace("%", "").strip()
        set_volume_windows(int(set))

    elif "check running application" in output_text:
        check_running_app()
    else:
        Auto_main_brain(output_text)

def normalize_time_format(text):
    """Normalizes time format in the given text."""
    return text.replace(" p.m.", "PM").replace(" a.m.", "AM")

def handle_vision_command():
    """Handles vision-related commands."""
    image_path = "captured_image.png"
    if capture_image_and_save(image_path):
        encoded_image = encode_image_to_base64(image_path)
        answer = vision_brain(encoded_image)
        speak(answer)

def Jarvis():
    """Main function to start Jarvis."""
    clear_file()
    t1 = threading.Thread(target=listen)
    t2 = threading.Thread(target=check_inputs)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
