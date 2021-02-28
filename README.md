**Jack Nichols**
--
- No directions beyond the basics
- external dependencies mentioned in requirements.txt
- My project uses an API key to retrieve college data, then makes a database file, and fills it with the database with the data I received.
In addition, it retrieves data from an excel file and fills another table in the database file with that data.
- Nothing is missing from the project, the workflow run is completed successfully with the 2 old tests and 4 new ones. The second old test is modified
to use a specific function in demo.py used to test the database, as I felt that was probably a poor methodology.

- I created 2 tables. 
- colleges, the first table, has a column for school id, name, state, city, size in 2017 and 2018, earnings over the poverty line 3 years after completion 2017, and overall repayment after 3 years 2016.(i added school name because I forgot it for sprint 2)
- employment, the second table, has a column for occupation title, total number employed, the hourly wages and annually salary of the bottom 25 percentile, and occupation code
- I have 6 tests that run successfully. 
