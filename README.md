**Jack Nichols**
--
- No directions beyond the basics
- external dependencies mentioned in requirements.txt
-My project uses the 2 tables in the database to display data in a GUI window. The window allows the user to update the file to 
whatever excel file they want, and updates the data without having to close out of the window

- The database has two tables, one for data from the API call and one from the excel file, and stores them for use in the 
college_data file
- All my tests run successfully on my machine and github actions.
 Manual written tests with pictures can be seen in the test_gui_manual.md file.
 
 **Things you should read before running and reading code**
 - Regarding the function test_data_analysis in test_demo.py, there are 5 assert statements. I wasn't sure originally if 
 this was poor practice or not, so I did some research. The general consensus was to follow the idea of Arrange, Act, and Assert, meaning that 
 it's ok to have multiple asserts (keep it to at most 5), if it's testing different parts of the same action. I could have 
 broken up that test function into a few separate ones, but it would require me to arrange and act on the same process multiple times. 
 So I came to the conclusion that because all the assert statements are testing the same action, making sure it follows the necessary criteria in 
 terms of return values based on the input, I figured the multiple asserts were not poor practice. 
 
 - Also, when updating the file in the window, you should know that there is a momentary pause where it appears that the window 
 is not responding, just give it a second, it will return to normal function where you can observe the changes made. Also, if there are values that are null
 for the state, that will show up as a '0' in the window when visualizing data.

 - There is also a large window of waiting when doing the api call, you said to mention if there were any long pauses
 - The way I presented the data (the ratios for the maps) were okayed by you. 
