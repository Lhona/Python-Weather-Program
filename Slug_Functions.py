#Our functions, first function calls next function and the results
#fall like a domino stack
import requests
import os
from GLOB_VAR import zipcode
from GLOB_VAR import key
from GLOB_VAR import uRL
from GLOB_VAR import name_City
from GLOB_VAR import chosen_units
import time


#the start of everything
def main_menu():
    #usual while, if, loop that error checks and sends the input to the next function
    user_entry = ''
    print("===============")
    print("===MAIN MENU===")
    print("===============")
    while user_entry != "QUIT":
        print("Welcome to the weather reporting program.\nBefore we start, we need to know what kind of\nmeasuring units you use.\nPlease type [CONTINUE] to go on or [QUIT] to end the program.")
        print("Also type [RECALL] to print out the data of a previous weather report.")
        user_entry = input("Enter choice between CONTINUE, QUIT, or RECALL in main menu: ")
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
        print("Please choose between the two measurement systems:\n[M] for metric.\n[I] for imperial.\n[K] for kelvin.")
        user_entry = input("Enter M, I, or K for measurements: ")
        if user_entry == "M":
            print("Units will be displayed in metric.")
            chosen_units = user_entry
            find_choice(chosen_units)
            break
        elif user_entry == "I":
            print("Units will be displayed in imperial")
            chosen_units = user_entry
            find_choice(chosen_units)
            break
        elif user_entry == "K":
            print("Units will be displayed in kelvin, the default value.")
            chosen_units = user_entry
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
        print("Please choose between the two location methods:\n[CITY]\n[ZIPCODE]\n[COMBINE] - Enter both City then Zipcode.")
        user_entry = input("Enter CITY, ZIPCODE, or COMBINE to use both:")
        doubleornothing = ''#I kept getting a postal code from ukraine with just the zipcode alone.
        #so I went and added a dual functionality that should work.
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
        elif user_entry == "COMBINE":
            print("You can combine both city and zipcode to get a more accurate location.")
            print("Enter City Name:")
            name_City = input("Enter City Name: ")
            print("Enter Zipcode")
            zipcode = input("Enter Zipcode: ")
            doubleornothing = name_City + "," + zipcode
            print("You have entered " + str(doubleornothing))
            construct_URL(doubleornothing, set_units)
            break
        else:
            print("Not a valid entry, please try again.")
            continue



#this one constructs our URL based on several global values being defined.
def construct_URL(locale_choice, set_units):
    print("======================")
    print("===URL CONSTRUCTION===")
    print("======================")
    print("Before you can continue, please enter your API Key to connect properly.")
    key = input("Enter API Key:")
    url_units = '' #much safeer IMO to do this, doesn't pass a global everywhere. makes the global  a flag of sorts
    if set_units == "M":
        url_units = "&units=metric"
    elif set_units == "I":
        url_units = "&units=imperial"
    elif set_unit == "K":
        url_units = ''
    comp_URL = str(uRL) + "&q=" + str(locale_choice) + str(url_units) + "&appid=" + str(key) #kept missing the & sign on appid...
    ping_server(comp_URL, set_units) #passes comp_URL to ping_server() function

#here comes the fun part.
#A ping to the server to ensure that we have a connection, otherwise it jumps you a menu.
#this is called at the beginning of each weather_find_x function.
def ping_server(comp_URL, set_units): #receives URL to ensure that we have a status 200.
    print("=================")
    print("===SERVER PING===")
    print("=================")
    try:
        status_data = requests.get(comp_URL)
    except:
        print("There's  been an error with the connection.\nReturning to Main Menu.")
        main_menu()
        #jumps back to main menu
    else:
        print("No Connection Errors.\nProceeding with data request.")
    check_valid_entry(comp_URL, set_units) #proceeds with request, again passing the URL on(it's starting to get confusing)

#try block to see if the user entered a valid city/zipcode in. if not, it sends them back to find_choice
#method is a bit backwards, but it will essentially return an error if...
#why am I using a try method for a value that shows up either way?
def check_valid_entry(comp_URL, set_units):
    print("================")
    print("===VALIDATION===")
    print("================")
    weather_data = requests.get(comp_URL).json() #just gimme the json for this.
    validtest = weather_data['cod'] #what code you gonna give us?
    if validtest == 200:
        print("Your entry is valid, proceeding.")
        data_collect(comp_URL, set_units)#how many times is a variable passed through a function
                              #before it starts to question its purpose in life.
    elif validtest == 401:
        print("Your API key or data entry is invalid, returning to main menu.")
        main_menu()
    else: #duh, this works. Unless it's a really specific one like 501 or the like.
        print("Not a valid entry, returning to main menu.")
        print("Error: " + str(validtest))
        print(str(comp_URL))
        main_menu()

#collect our data for writing
def data_collect(comp_URL, set_units):
    weather_data = requests.get(comp_URL).json()
    locale = weather_data["name"] #location we asked for
    cntry = weather_data["sys"]["country"] # country
    tmp_K = weather_data["main"]["temp"]
    feels = weather_data["main"]["feels_like"]
    w_Speed = weather_data["wind"]["speed"]
    humid = weather_data["main"]["humidity"]
    desc = weather_data["weather"][0]["description"]
    data_write(locale, cntry, tmp_K, feels, w_Speed, humid, desc, set_units)

#collected data from above is passed into this function and written to a
#user-named file.
def data_write(locale, cntry, tmp_K, feels, w_Speed, humid, desc, set_units): #set_units been passed around like a football in this file.
    temp_units = ''
    vel_units = ''
    chosen_units = set_units
    if chosen_units == "M":
        temp_units = "°C"
        vel_units = "MPS (Meter Per Second)"
    elif chosen_units == "I":
        temp_units = "°F"
        vel_units = "MPH"
    elif chosen_units == "K":
        temp_units = "°K"
        vel_units = "MPS (Meter Per Second)"

    print("You'll need to enter a filename without an extension.")
    #write filename, and all data to the file before reading it back to the user via another function.
    new_File = input("Enter a filename to write weather data to-\nYou do not need to include an extension:") + ".txt"
    print("The file " + str(new_File) + " has been created.\nWriting data to file...")
    active_File = open(new_File, "w+")
    localtime = time.asctime( time.localtime(time.time()) ) #Gets current date and time.
    active_File.write("The time and date is: " + str(localtime) + "\n") #writes date and time.
    active_File.write("The location is " + str(locale) + ", " + str(cntry) + "\n") #writes city and country
    active_File.write("Temperature is " + str(tmp_K) + str(temp_units) + "\n") #writes temperature
    active_File.write("Temperature feels like " + str(feels) + str(temp_units) + "\n") #writes what it feels like
    active_File.write("Wind speed is " + str(w_Speed) + " " + str(vel_units) + "\n") #writes wind speed
    active_File.write("A brief description of the weather is: " + str(desc) + "\n") #writes brief description
    active_File.write("Humidity is " + str(humid) + "%" + "\n") #writes humidity
    active_File.close()
    time.sleep(1)
    print("Writing data...")
    time.sleep(1)
    print("Writing data...")
    time.sleep(1)
    print("Writing data...")
    time.sleep(1)
    print("Done.\n")
    data_question()

def data_question(): #this is the "You wanna read or go back to the menu?"
    print("==============")
    print("===END MENU===")
    print("==============")
    print("Would you like to read your data or go back to the main menu?")
    print("Enter [READ] to read written data from file or [BACK] to return to menu.")
    print("Enter QUIT to end the program.")
    user_entry = ''
    while user_entry != "QUIT":
        user_entry = input("Enter choice between READ, BACK, and QUIT:")
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

def data_recall(): #recall the data from the saved file.
    print("==================")
    print("===TOTAL RECALL===")
    print("==================")
    print("Enter the name a of a previous file without the extension.\n")
    new_File = input("Enter filename:") + ".txt"
    try: #realized program could crash here if I didn't setup any try blocks.
        active_File = open(new_File, "r")
        file_read = active_File.read()
        print(str(new_File) + " is being displayed.\n")
        print(file_read)

    except:
        print("File does not exist.")
        main_menu()
    data_question()

def endprogram():
    print("Thank you for using the weather request program!")

#It has been done.
