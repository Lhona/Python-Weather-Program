#Global variables go HERE
global zipcode
global key
global uRL
global name_City
global chosen_units
name_City = '' #name of city, should user decide to enter it in.
zipcode = '' #zipcode number
key = "" #API key, you'll have to enter it in manually to ensure that it's not out there on the web(where someone else can use it.)
uRL = "http://api.openweathermap.org/data/2.5/weather?" #URL, or rather the base
#of it, we can add and modify as needed based on user inputs.
chosen_units = ''# this determines whether or not the weather is output as kelvin,
#celsius, or fahrenheit.
