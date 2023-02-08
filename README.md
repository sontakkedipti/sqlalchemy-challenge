# sqlalchemy-challenge
 To help with trip planning, decided to do a climate analysis about the area. 
 The following sections outline the steps that you need to take to accomplish this task.
 
In this section, used Python and SQLAlchemy to do a basic climate analysis and data exploration of climate database. Specifically, used  SQLAlchemy ORM queries, Pandas, and Matplotlib. To do so, complete the following steps:

1. Used the provided files (climate_starter.ipynb and hawaii.sqlite) to complete your climate analysis and data exploration.
2. Used the SQLAlchemy create_engine() function to connect t  SQLite database.
3. Used the SQLAlchemy automap_base() function to reflect tables into classes, and then save references to the classes named station and measurement.
4. Linked Python to the database by creating a SQLAlchemy session.

Part 1: Analyze and Explore the Climate Data
In this section, used Python and SQLAlchemy to do a basic climate analysis and data exploration of your climate database.
Specifically, used SQLAlchemy ORM queries, Pandas, and Matplotlib.

Performed a precipitation analysis and then a station analysis. Used Pandas to print the summary statistics for the precipitation data.

Part 2 : Design Your Climate App
After completing initial analysis, designed a Flask API based on the queries that just developed. 
To do so, useed Flask to create the routes.
 
1.  /

Start at the homepage.List all the available routes.

2. /api/v1.0/precipitation

Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.

Return the JSON representation of your dictionary.

3. /api/v1.0/stations

Return a JSON list of stations from the dataset.

4. /api/v1.0/tobs

Query the dates and temperature observations of the most-active station for the previous year of data.Return a JSON list of temperature observations for the previous year.

5. /api/v1.0/<start> and /api/v1.0/<start>/<end>

Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
