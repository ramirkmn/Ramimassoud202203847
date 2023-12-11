import openai
import json
import time
import serial

ser = serial.Serial('COMX', 9600) 
api_key = "  "
openai.api_key = api_key


def TurnOnMicrowave(delay):
    signal = {
        "action": "turn_on the microwave ",
        "delay": delay,
      
    }
    print(f"Signal sent: {json.dumps(signal)}")
    time.sleep(delay)
    return "Microwave turned on after delay."

def send_delayed_signal_arduino(delay_time):
    message = f"turn_on {delay_time}\n"  # Send a message with the command and delay time
    ser.write(message.encode())
    print(f"Signal sent to Arduino: Turn on microwave after a delay of {delay_time} seconds")

prompt = "Hello, Please turn on the microwave after a delay  10 seconds"
messages = [{"role": "user", "content": prompt}]

functions = [
    {
        "name": "TurnOnMicrowave",
        "description": "Turn on microwave after a specified delay (10 or 20 seconds)",
        "parameters": {
            "type": "object",
            "properties": {
                "delay": {
                    "type": "integer",
                    "description": "Delay time in seconds for turning on the microwave (10 or 20)",
                    "enum": [10, 20]
                },
            },
            "required": ["delay"],
        },
    }
]

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    messages=messages,
    functions=functions,
    function_call="auto"
)

# take delay from the prompt and then compare it with the delay to know if it is within the range of delay or not
delay = None
choices = response['choices']
for choice in choices:
    if 'function_call' in choice['message']:
        delay_json = choice['message']['function_call']['arguments']
        extracted_delay = json.loads(delay_json).get("delay")
        if extracted_delay and int(extracted_delay) in [10, 20]:
            delay = int(extracted_delay)
            break


if delay:
     send_delayed_signal_arduino(delay)
else:
    print("Delay not specified within the expected range.")

ser.close()