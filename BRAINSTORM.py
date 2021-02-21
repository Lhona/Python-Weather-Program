'''
The original flow chart steps
Call main function for code to activate
2. input code for zip code and/or city
3. Run a second function that obtains weather forceast data
4. Display message that a connection attempt is being made
5. Internal code uses Requests Library to connect
6. Display message that connection has been made or failed.
7. Verify data entered does not return an error
8. If error returned, use loop to reprompt request
9. Loop to Repeat step 2 if step 8 occurs
10. Run third function to display data in a readable format
11. Run fourth function to prompt user for a rerun- (Y/N)

Revised-
Call Main Function from Slug_Functions
    Slug initiates menuloop
        menuloop asks user for input data related to zipcode
        menuloop asks user if they want to quit
        menuloop goes to zipcode_Find
        menuloop contains elifs to find any user errors for inputs
        

        zipcode_Find pitches for a request from the server.
        request results are stored in a dictionary
        dictionary is a global variable that is stored in GLOB_VAR
        results are then searched through the dictionary
        results are sorted in dictionary
        results are printed from dictionary in readable format.

        Alternative, use weather_report class to store all data into an object
        object stored into dictionary with zipcode key
        (optional) let user print out data of previously created entries by
        -storing keys in a list/printing out keys and letting users choose
        -what they want printed out. Essentially a web version of the
        -vehicle garage.

        question_loop function is activated.
        question_loop is similar as menuloop
        question_loop asks for confirmation to continue or end program
        question_loop

'''
