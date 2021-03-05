#Our functions, first function calls next function and the results
#fall like a domino stack
import requests
import os

#the start of everything
def menuloop():
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
        elif user_entry == "KEY":
            print("Thank you for entering your API key. Please copy and hit CTRL+V on your keyboard when prompted.")
            key = input("Enter API Key: ")
            break
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
        if user_entry == "C":
            print("Units will be displayed in metric.")
            chosen_units = "&units=metric"
            find_choice()
            break
        elif user_entry == "F":
            print("Units will be displayed in imperial")
            chosen_units = "&units=imperial"
            find_choice()
            break
        elif user_entry == "K":
            print("Units will be displayed in kelvin, the default value.")
            chosen_units = ''
            find_choice()
            break
        else:
            print("Not a valid entry, try again.")
            continue

#this is a bit different. I figured asking the user for presets first before
#finding the city would be easier, as it sets the search method values as city
#or zipcode. Much easier IMO. Though with the amount of IF statements, I could've
#used a dictionary to use a .get method instead...
def find_choice():
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
            construct_URL(name_City)
            break
        elif user_entry == "ZIPCODE":
            print("You have chosen to use the zipcode as the identifier.\nPlease input the zipcode.")
            zipcode = input("Enter Zipcode:")
            print("You have input the zipcode " + str(zipcode))
            construct_URL(zipcode)
            break
        elif user_entry == "BACK":
            print("Returning to main menu...")
            menuloop()
            break
        else:
            print("Not a valid entry, please try again.")
            continue



#this one constructs our URL based on several global values being defined.
def construct_URL(locale_choice):
    comp_URL = uRL + "appid=" + str(key) + "&q=" + str(locale_choice) + str(chosen_units)
    ping_server(comp_URL) #passes comp_URL to ping_server() function

#here comes the fun part.
#A ping to the server to ensure that we have a connection, otherwise it jumps you a menu.
#this is called at the beginning of each weather_find_x function.
def ping_server(comp_URL): #receives URL to ensure that we have a status 200.
    try:
        status_data = requests.get(comp_URL)
    except:
        print("There's  been an error with the connection.\nReturning to Main Menu.")
        menuloop()
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
    if chosen_units == "&units=celsius":
        new_units = "°C"
    elif chosen_units == "&units=fahrenheit":
        new_units = "°C"
    print("You'll need to enter a filename without an extension.")
    new_File = input("Enter a filename to write weather data to-\nYou do not need to include an extension:") + ".txt"
    active_File = open(new_File, "w+")
    active_File.write()
    active_File.write("Temperature is " + str(tmp_K) + new_units + "\n")
    active_File.write("Temperature feels like " + str(feels) + str(new_units) + "\n")
    active_File.write("Wind speed is " + str(w_Speed) + " MPH" + "\n")
    active_File.write("A brief description of the weather is: " + str(desc) + "\n")
    active_File.write("Humidity is " + str(humid) + "%" + "\n")
    active_File.close()
    data_question()




def data_recall():
    print("Enter the name a of a previous file without the extension")
    new_File = input("Enter filename:") + ".txt"
    active_File = open(new_File, "r")
    file_read = active_File.read()
    print(file_read)
    menuloop()




def question_loop():
    #similar to menu loop, just asks the user if they're interested in trying again
    print("Would you like to start over again?\nType {YES} or {NO}.")
    user_entry = ''
    while user_entry != "NO":
        user_entry = input("Enter: ")
        if user_entry == "YES"
            menuloop()
            break
        elif user_entry == "NO"
            endprogram()
            break
        else:
            print("Not a valid entry, try again.")
            continue

def endprogram():
    print("Thank you for using the weather request program!")
