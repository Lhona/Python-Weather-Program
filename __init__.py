__all__ = [
    "menuloop", #start of the program, also allows users to quit
    "choose_units", #lets users choose measurement
    "find_choice", #users chooses between city or zipcode as the method
    "weather_find_city", #executes finding weather for city
    "weather_find_zipcode", #executes finding weather for zipcode
    "construct_URL", #constructs the URL with previous considerations in mind.
    "ping_server", #pings server to ensure connection, returns to menu if it doesn't work
    "check_valid_entry", #checks if entry was valid, if not(404 error) then returns to menu.
    "data_collect", #collects data from json after successful connection and verification
    "data_write", #writes data to a saved file in the main directory with custom user name
    "data_question", #asks the user if they want to save and start over, or display the data and start over.
    "data_recall", #recalls a specific filename and reads off the data.
    "",
    "",
    "",
    "",
    "",
]
