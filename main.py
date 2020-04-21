'''

First crate and auxiliary functions are called.
Then the client connection is set.
Next, tables are created in the DB.
After that, data to be uploaded is parsed into a tuple containing:
    a string with the name of the database
    a list of lists containing each line a list of elements
Auxiliar parse operations are performed.
Queries to insert data into tables are generated and executed.

Dependencies are:
1. crate                            to create a client to connect and
                                    interact with the database
2. queryFunctions.py                where the queries into crateDB are built
3. auxiliaryParseFunctions.py       where additional data cleaning is
                                    performed to matchthe structure of the tables.

I couln't test the whole code in my crappy PC due to lack of memory so I had
to test it with small chunks. Sorry if there are any underlaying errors.
'''

## check if crate package is installed
package = 'crate'
try:
    __import__(package)
except ImportError:
    print("Crate not found, import crate pacakge.")

## import crate client interface
from crate import client
# query function definitions
from queryFunctions import createTablesQuery
from queryFunctions import insertDataQuery
# parse function definitions
from auxiliaryParseFunctions import columnToBool
from auxiliaryParseFunctions import columnToFloat
from auxiliaryParseFunctions import parseStops


## connect to our instance of the database
try:
    connection = client.connect("http://localhost:4200/")
except ConnectionError:
    print("Unable to connect to crate node")

cursor = connection.cursor()

## After looking at the data, we are going to make the following assumptions:
##      all data between quotation marks is going to be of type text
##      all numeric data is going to be of type bigint unless
##      unless it contains a comma, where will be of type double precision
##      I'm facing issues with matching boolean types so I will load them as text

print("creating tables \n")
createTablesQuery(cursor)

print("... \n")
print("importing data \n")

## first element of the tuple is the name of the table
## second element contains the table. line 0 contains the header for our query
## importing files and parsing into a list of lines
## 
## E.G.
## string trips = "../GTFS_files/trips.txt"

trips           = ('trips',             [line.rstrip().split(',') for line in open('trips.txt')])
transfers       = ('transfers',         [line.rstrip().split(',') for line in open('transfers.txt')])
stops           = ('stops',             [line.rstrip().split(',') for line in open('stops.txt')])
stop_times      = ('stop_times',        [line.rstrip().split(',') for line in open('stop_times.txt')])
shapes          = ('shapes',            [line.rstrip().split(',') for line in open('shapes.txt')])
routes          = ('routes',            [line.rstrip().split(',') for line in open('routes.txt')])
frequencies     = ('frequencies',       [line.rstrip().split(',') for line in open('frequencies.txt')])
calendar_dates  = ('calendar_dates',    [line.rstrip().split(',') for line in open('calendar_dates.txt')])
calendar        = ('calendar',          [line.rstrip().split(',') for line in open('calendar.txt')])
agency          = ('agency',            [line.rstrip().split(',') for line in open('agency.txt')])

# parsing calendar into bools
for i in range(1, 8):
    columnToBool(calendar,i)

# parsing to solve the commma issue
parseStops(stops)
# setting values to float and removing 5 empty entries
# TODO: manage exceptions
columnToFloat(stops,4)
columnToFloat(stops,5)

# transforming string into floats
for i in range(1,2):
    columnToFloat(shapes,i)

print("... \n")

## add table references to an iterable object
## maybe a dictionary is needed to pair each list with its name (trips, "trips"), (transfers, "transfers")...
#tables = [trips, transfers, stops, stop_times, shapes, routes, frequencies, calendar_dates, calendar, agency]
tables = [trips, transfers, stops, stop_times, routes, frequencies, calendar_dates, calendar, agency]

print("starting to insert data in the database \n")
for table in tables:
    insertDataQuery(table, cursor)

print("Task completed successfully")
