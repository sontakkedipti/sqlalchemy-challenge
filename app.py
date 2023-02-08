import numpy as np
import sqlalchemy

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.sql import exists  

from flask import Flask, jsonify



#Connecting to  Database 
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station


# Flask Setup
app = Flask(__name__)

# Setting up Flask Routes


# Homepage page
@app.route("/")
def welcome():
    """List all available routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

# last year variable
last_year = '2016-08-23'

# Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value
# Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create session (link) from Python to the DB
    session = Session(engine)

    # Query Measurement
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= last_year).group_by(Measurement.date).order_by(Measurement.date).all()

    # Create a dictionary
    precipitation_analysis = []
    for each_row in results:
        dict = {}
        dict["date"] = each_row.date
        dict["prcp"] = each_row.prcp
        precipitation_analysis.append(dict)

    # Close the session
    session.close()

    return jsonify(precipitation_analysis)


#Return a JSON list of stations from the dataset
@app.route("/api/v1.0/stations")
def stations():
    # Create session (link) from Python to the DB
    session = Session(engine)

    # Query Stations
    results = session.query(Station.name).all()

    # Convert list of tuples into normal list
    stations = list(np.ravel(results))

    # Close the session
    session.close()

    return jsonify(stations)


# Query the dates and temperature observations of the most active station for the last year of data
@app.route("/api/v1.0/tobs") 
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query to find most active station
    station_list = (session.query(Measurement.station, func.count(Measurement.station))
                             .group_by(Measurement.station)
                             .order_by(func.count(Measurement.station).desc())
                             .all())
    
    station_activity = station_list[0][0]

    # Return a list of tobs for the last year
    results = (session.query(Measurement.station, Measurement.date, Measurement.tobs)
                      .filter(Measurement.date >= last_year)
                      .filter(Measurement.station == station_activity)
                      .all())

    # Create list of temperature observations for the previous year
    tobs_list = []
    for result in results:
        line = {}
        line["Station"] = result[0]
        line["Date"] = result[1]
        line["Temperature"] = int(result[2])
        tobs_list.append(line)

    # Close the session
    session.close()    

    return jsonify(tobs_list)


# Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
# For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
@app.route("/api/v1.0/<start>")
def start(start):

    # Create session (link) from Python to the DB
    session = Session(engine)

    # Query to find stats on date
    results = session.query(func.min(Measurement.tobs), 
                            func.avg(Measurement.tobs), 
                            func.max(Measurement.tobs)).filter(Measurement.date >= start).all()

    # Save result
    min = results[0][0]
    avg = results[0][1]
    max = results[0][2]
    
    # Print result
    print_result = (['Entered Start Date: ' + start,
    			'The lowest temp was: '  + str(min),
    			'The average temp was: ' + str(avg),
    			'The highest temp was: ' + str(max)])

    # Close the session
    session.close()  

    return jsonify(print_result)
   

# For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):

    # Create session (link) from Python to the DB
    session = Session(engine)

    # Query stats for dates within range
    date_range_results = (session.query(func.min(Measurement.tobs),
                                        func.avg(Measurement.tobs), 
                                        func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all())
    
    # Save result
    min = date_range_results[0][0]
    avg = date_range_results[0][1]
    max = date_range_results[0][2]
    
    # Print Result
    print_results = (['Entered Start Date: ' + start,
    			'Entered End Date: ' + end,
    			'The lowest temp was: '  + str(min),
    			'The average temp was: ' + str(avg),
    			'The highest temp was: ' + str(max)])

    # Close the session
    session.close() 

    return jsonify(print_results)

if __name__ == '__main__':
    app.run(debug=True)