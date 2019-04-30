# import dependencies 
import datetime as dt
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
from datetime import datetime

engine = create_engine("sqlite:///Hawaii.sqlite?check_same_thread=False")
Base = automap_base()
Base.prepare(engine, reflect=True)
Station = Base.classes.station
Measurement = Base.classes.measurement
session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"Welcome!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of rain fall for prior year"""
    precip=session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date).all()
    return jsonify (precip)

@app.route("/api/v1.0/stations")    
def stations():
    station_list=session.query(Station.station).all()
    return jsonify (station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    recent_date=session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    recent_year=datetime.strptime(recent_date[0],'%Y-%m-%d')-dt.timedelta(days=365)
    recent_year
    tob=session.query(Measurement.tobs, Measurement.date).filter(Measurement.date > recent_year ).order_by(Measurement.date).all()
    return jsonify(tob)

@app.route("/api/v1.0/start")
def starting():
     start_date = dt.date(2016, 5, 14) - dt.timedelta(days=365)    
     start=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all() 
     return jsonify(start)

@app.route("/api/v1.0/start/end")
def ending():
    end_date=dt.date(2016, 5, 14) - dt.timedelta(days=365)  
    start_date = dt.date(2016, 5, 3) - dt.timedelta(days=365)    
    start_end=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    return jsonify(start_end)

if __name__ == '__main__':
    app.run(debug=False)
    
