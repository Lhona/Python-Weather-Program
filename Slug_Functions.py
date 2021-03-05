#Our functions, first function calls next function and the results
#fall like a domino stack
import requests
import os

def menuloop():
    #usual while, if, loop that error checks and sends the input to the next function
    user_entry = ''
    while user_entry != "QUIT":
        print("Welcome to the weather reporting program.\nBefor we start, we need to know what kind of\nmeasuring units you use.\nPlease type [CONTINUE] to go on or [QUIT] to end the program.")
        user_entry = input("Enter choice: ")
        if user_entry == "CONTINUE":
            #finds the weather, default kelvin units but can be set later on
            choose_units()
            break
        elif user_entry == "QUIT":
            #jumps to function that prints and ends the script.
            endprogram()
            break
        else:
            print("Not a valid entry, try again.")
            continue


#this  should allow the user to set between celsius, kelvin(default) or fairrenhight
def choose_units():
    user_entry = ''
    while user_entry != "BACK":
        print("Please choose between the two measurement systems:\n[C] for Celsius.\n[F] for Fahrenheit.\n[K] for Kelvin.")
        user_entry = input("Enter: ")
        if user_entry == "C":
            print("Units will be displayed in Celsius.")
            chosen_units = "&units=celsius"
            find_choice()
            break
        elif user_entry == "F":
            print("Units will be displayed in Fahrenheit")
            chosen_units = "&units=fahrenheit"
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
    while user_entry != "BACK": #using a different setup this time, will roll back to the main menu.
        name_City = ''
        zipcode = ''
        print("Please choose between the two location methods:\n[CITY]\n[ZIPCODE]")
        user_entry = input("Enter Choice:")
        if user_entry == "CITY":
            print("You have chosen to use the city name as the identifier.\nPlease input the city name.")
            name_City = input("Enter City Name:")
            print("You have input the city " + str(name_City))
            weather_find_city()
            break
        elif user_entry == "ZIPCODE":
            print("You have chosen to use the zipcode as the identifier.\nPlease input the zipcode.")
            zipcode = input("Enter Zipcode:")
            print("You have input the zipcode " + str(zipcode))
            weather_find_zipcode()
            break
        else:
            print("Not a valid entry, please try again.")
            continue
#this one constructs our URL based on several global values being defined.
def construct_URL():
    comp_URL = uRL + "appid=" + key + "&q=" + local_choice + unit_Choice

#here comes the fun part.
#A ping to the server to ensure that we have a connection, otherwise it jumps you a menu.
#this is called at the beginning of each weather_find_x function.
def ping_server():
    try:
        status_data = requests.get(comp_URL)
    except:
        print("There's  been an error with the connection.\nReturning to Main Menu.")
        #jumps back to main menu
    else:
        print("No Connection Errors.\nProceeding with data request.")
    check_valid_entry()
    return
#try block to see if the user entered a valid city/zipcode in. if not, it sends them back to find_choice
def check_valid_entry():
    validtest = weather_data['cod']
    if validtest == "404":
        print("Not a valid entry, try again")



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
