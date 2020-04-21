def insertDataQuery (table,cursor):
    '''

    Table is a tuple which contains:
        table[0] is a string with the name of the table.
        table[1] is a list in which each line is an entry of the file.
        first line is the header of the table.

        First the table header is parsed to generate the insert query:

            >>> cursor.exectue(
                """ INSERT INTO tableIntheDB(column0, column1,...,columnN)
                    VALUES(?,?,...,?)""",
                    ('a1','a2',...,'aN')
                    )

        Then it iterates through each line, and inserts them in the DB.
        TODO: parallelize / bulk insert
    '''

    # name of the table in the db
    name = table[0]
    print("inserting data in " + name)
    # columns of the table
    #header = table[1][0].split(',')
    header = table[1][0]

    # counting the number of elements to be added in each row
    values = " ) VALUES ("
    for h in header[:-1]: values += "?,"
    values += "?)"

    # building up the insert query statement
    query = "INSERT INTO " + name + " ("
    for h in header[:-1]: query = query + h + ", "
    query = query + header[-1] + values

    # there is a comma in the value of the column (stop_name)
    # it requires to be parsed separately.
    for line in table[1][1:]:
        cursor.execute(query, line)

    ## would it be faster if the lines where split on import (?)
    ## could be parallelized with cursor.executemany (?)
    ## could be parallelized with lambda functions(?)


def createTablesQuery(cursor):
    '''

    this function creates the different tables according to the GTFS standard.
    each table requires different types and must be declared individually.
    '''

    ## trips
    cursor.execute("""CREATE TABLE trips
                        (route_id text,
                        service_id text,
                        trip_id text,
                        trip_headsign text,
                        trip_short_name text,
                        direction_id text,
                        block_id text,
                        shape_id text,
                        wheelchair_accessible text,
                        bikes_allowed text)""")
    ## transfers
    cursor.execute("""CREATE TABLE transfers
                        (from_stop_id bigint,
                        to_stop_id bigint,
                        transfer_type text,
                        min_transfer_time text,
                        from_route_id text,
                        to_route_id text,
                        from_trip_id text,
                        to_trip_id text)""")

    ## stops
    cursor.execute("""CREATE TABLE stops
                        (stop_id bigint,
                        stop_code text,
                        stop_name text,
                        stop_desc text,
                        stop_lat double precision,
                        stop_lon double precision,
                        location_type text,
                        parent_station text,
                        wheelchair_boarding text,
                        platform_code text,
                        zone_id text)""")

    ## stop_times
    cursor.execute("""CREATE TABLE stop_times
                        (trip_id bigint,
                        arrival_time text,
                        departure_time text,
                        stop_id bigint,
                        stop_sequence text,
                        pickup_type text,
                        drop_off_type text,
                        stop_headsign text)""")

    ## shapes
    cursor.execute("""CREATE TABLE shapes
                        (shape_id text,
                        shape_pt_lat double precision,
                        shape_pt_lon double precision,
                        shape_pt_sequence text)""")

    ## routes
    cursor.execute("""CREATE TABLE routes
                        (route_id text,
                        agency_id text,
                        route_short_name text,
                        route_long_name text,
                        route_type text,
                        route_color text,
                        route_text_color text,
                        route_desc text)""")

    ## frequencies
    cursor.execute("""CREATE TABLE frequencies
                        (trip_id bigint,
                        start_time bigint,
                        end_time bigint,
                        headway_secs bigint,
                        exact_times bigint)""")

    ## calendar_dates
    cursor.execute("""CREATE TABLE calendar_dates
                        (service_id bigint,
                        date bigint,
                        exception_type text)""")

    ## calendar
    cursor.execute("""CREATE TABLE calendar
                        (service_id bigint,
                        monday boolean,
                        tuesday boolean,
                        wednesday boolean,
                        thursday boolean,
                        friday boolean,
                        saturday boolean,
                        sunday boolean,
                        start_date bigint,
                        end_date bigint)""")


    ## agency
    cursor.execute("""CREATE TABLE agency
                        (agency_id text,
                        agency_name text,
                        agency_url text,
                        agency_timezone text,
                        agency_lang text,
                        agency_phone text)""" )
