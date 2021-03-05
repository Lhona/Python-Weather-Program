#Our functions, first function calls next function and the results
#fall like a domino stack
import requests
import os
from GLOB_VAR import zipcode
from GLOB_VAR import key
from GLOB_VAR import uRL
from GLOB_VAR import name_City
from GLOB_VAR import chosen_units

#the start of everything
def main_menu():
    #usual while, if, loop that error checks and sends the input to the next function
    user_entry = ''
    print("===============")
    print("===MAIN MENU===")
    print("===============")
    while user_entry != "QUIT":
        print("Welcome to the weather reporting program.\nBefor we start, we need to know what kind of\nmeasuring units you use.\nPlease type [CONTINUE] to go on or [QUIT] to end the program.")
        print("Please type [KEY] to enter your API or provided API key or type [RECALL] to print out the data of a previous weather report.")
        user_entry = input("Enter choice: ")
        if user_entry == "CONTINUE":
            #finds the weather, default kelvin units but can be set later on
            choose_units()
            break
        elif user_entry == "QUIT":
            #jumps to function that prints and ends the script.
            endprogram()
            break
            #this was from a push with the key in the script. Didn't realize how bad it would've been had it not been for GitGuard.
#        elif user_entry == "KEY":
#            print("Thank you for entering your API key. Please copy and hit CTRL+V on your keyboard when prompted.")
#            key = input("Enter API Key: ")
#            continue
#Got an UnboundLocalError referencing it earlier in a different setup. Forcing the user through the process is easier than going back for it.
        elif user_entry == "RECALL":
            print("Enter a previously saved filename to redisplay the weather with date and time.")
            data_recall()
            break
        else:
            print("Not a valid entry, try again.")
            continue


#this  should allow the user to set between celsius, kelvin(default) or fairrenhight
def choose_units():
    user_entry = ''
    print("=======================")
    print("===MEASUREMENT UNITS===")
    print("=======================")
    while user_entry != "BACK":
        print("Please choose between the two measurement systems:\n[M] for metric.\n[I] for imperial.\n[K] for Kelvin.")
        user_entry = input("Enter: ")
        if user_entry == "M":
            print("Units will be displayed in metric.")
            chosen_units = "&units=metric"
            find_choice(chosen_units)
            break
        elif user_entry == "I":
            print("Units will be displayed in imperial")
            chosen_units = "&units=imperial"
            find_choice(chosen_units)
            break
        elif user_entry == "K":
            print("Units will be displayed in kelvin, the default value.")
            chosen_units = ''
            find_choice(chosen_units)
            break
        else:
            print("Not a valid entry, try again.")
            continue

#this is a bit different. I figured asking the user for presets first before
#finding the city would be easier, as it sets the search method values as city
#or zipcode. Much easier IMO. Though with the amount of IF statements, I could've
#used a dictionary to use a .get method instead...
def find_choice(set_units):
    user_entry = ''
    print("======================")
    print("===CITY AND ZIPCODE===")
    print("======================")
    name_City = ''
    zipcode = ''
    while user_entry != "BACK": #using a different setup this time, will roll back to the main menu.
        print("Please choose between the two location methods:\n[CITY]\n[ZIPCODE]")
        user_entry = input("Enter Choice:")
        if user_entry == "CITY":
            print("You have chosen to use the city name as the identifier.\nPlease input the city name.")
            name_City = input("Enter City Name:")
            print("You have input the city " + str(name_City))
            construct_URL(name_City, set_units)
            break
        elif user_entry == "ZIPCODE":
            print("You have chosen to use the zipcode as the identifier.\nPlease input the zipcode.")
            zipcode = input("Enter Zipcode:")
            print("You have input the zipcode " + str(zipcode))
            construct_URL(zipcode, set_units)
            break
        elif user_entry == "BACK":
            print("Returning to main menu...")
            main_menu()
            break
        else:
            print("Not a valid entry, please try again.")
            continue



#this one constructs our URL based on several global values being defined.
def construct_URL(locale_choice, set_units):
    print("Before you can continue, please enter your API Key to connect properly.")
    key = input("Enter API Key:")
    if set_units == "STANDARD":
        set_units = ''
    else:
        set_units = set_units
    comp_URL = str(uRL) + "appid=" + str(key) + "&q=" + str(locale_choice) + str(set_units)
    ping_server(comp_URL) #passes comp_URL to ping_server() function

#here comes the fun part.
#A ping to the server to ensure that we have a connection, otherwise it jumps you a menu.
#this is called at the beginning of each weather_find_x function.
def ping_server(comp_URL): #receives URL to ensure that we have a status 200.
    try:
        status_data = requests.get(comp_URL)
    except:
        print("There's  been an error with the connection.\nReturning to Main Menu.")
        main_menu()
        #jumps back to main menu
    else:
        print("No Connection Errors.\nProceeding with data request.")
    check_valid_entry(comp_URL) #proceeds with request, again passing the URL on(it's starting to get confusing)
    return
#try block to see if the user entered a valid city/zipcode in. if not, it sends them back to find_choice
#method is a bit backwards, but it will essentially return an error if...
#why am I using a try method for a value that shows up either way?
def check_valid_entry(comp_URL):
    weather_data = requests.get(comp_URL).json() #just gimme the json for this.
    validtest = weather_data['cod'] #what code you gonna give us?
    if validtest == "200":
        print("Your entry is valid, proceeding.")
        data_collect(comp_URL)#how many times is a variable passed through a function
                              #before it starts to question its purpose in life.
    elif validtest == "401":
        print("Your API key is invalid, please re-enter your key in the main menu.")
        main_menu()
    else: #duh, this works. Unless it's a really specific one like 501 or the like.
        print("Not a valid entry, returning to city and zipcode choice menu.")
        find_choice()


def data_collect(comp_URL):
    weather_data = requests.get(comp_URL).json()
    tmp_K = weather_data["main"]["temp"]
    feels = weather_data["main"]["feels_like"]
    w_Speed = weather_data["wind"]["speed"]
    humid = weather_data["main"]["humidity"]
    desc = weather_data["weather"][0]["description"]
    data_write(tmp_K, feels, w_Speed, humid, desc)

def data_write(tmp_K, feels, w_Speed, humid, desc):
    if chosen_units == "&units=metric":
        temp_units = "°C"
        vel_units = "MPS (Meter Per Second)"
    elif chosen_units == "&units=imperial":
        temp_units = "°F"
        vel_units = "MPH"
    elif chosen_units == "Standard":
        temp_units = "°K"
        vel_units = "MPS (Meter Per Second)"

    print("You'll need to enter a filename without an extension.")
    new_File = input("Enter a filename to write weather data to-\nYou do not need to include an extension:") + ".txt"
    active_File = open(new_File, "w+")
    active_File.write()
    active_File.write("Temperature is " + str(tmp_K) + str(temp_units) + "\n")
    active_File.write("Temperature feels like " + str(feels) + str(temp_units) + "\n")
    active_File.write("Wind speed is " + str(w_Speed) + " " + str(vel_units) + "\n")
    active_File.write("A brief description of the weather is: " + str(desc) + "\n")
    active_File.write("Humidity is " + str(humid) + "%" + "\n")
    active_File.close()
    data_question()

def data_question(): #this is the "You wanna read or go back to the menu?"
    print("Would you like to read your data or go back to the main menu?")
    print("Enter [READ] to read written data from file or [BACK] to return to menu.")
    print("Enter QUIT to end the program.")
    user_entry = ''
    while user_entry != "BACK":
        user_entry = input("Enter choice:")
        if user_entry == "READ":
            print("Data is being displayed...")
            data_recall()
            break
        elif user_entry == "BACK":
            print("Taking user back to main menu...")
            main_menu()
            break
        elif user_entry == "QUIT":
            print("Quitting the program...")
            endprogram()
            break;
        else:
            print("Not a valid entry, try again.")
            continue

def data_recall():
    print("Enter the name a of a previous file without the extension")
    new_File = input("Enter filename:") + ".txt"
    active_File = open(new_File, "r")
    file_read = active_File.read()
    print(file_read)
    data_question()




def endprogram():
    print("Thank you for using the weather request program!")
