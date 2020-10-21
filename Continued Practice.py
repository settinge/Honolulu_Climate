from flask import Flask,  jsonify
app = Flask(__name__)
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
import numpy as np
import json
from json import JSONEncoder


engine = create_engine("sqlite:///C:\\Users\\samantha.ettinger\\GWU-ARL-DATA-PT-12-2019-U-C\\02-Homework\\10-Advanced-Data-Storage-and-Retrieval\\Instructions\\Resources\\hawaii.sqlite")
# Base = automap_base()
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
Base.classes.keys()
Measurement = Base.classes.measurement
Stat = Base.classes.station
Meas = Base.classes.measurement
session = Session(engine)
# Latest Date
max_date=session.query(Meas.date).order_by(Meas.date.desc()).first()
print(max_date)


year_to_date = dt.date(2017, 8 ,23) - dt.timedelta(days=365)
#-timedelta(days=365)
app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        "/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/20120101<br/>"
        f"/api/v1.0/20120101/20130101"

    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    data=session.query(Meas.prcp,Meas.date).\
    filter(Meas.date >year_to_date).all()
    session.close()

    precip_data = list(np.ravel(data))
    return jsonify(precip_data)

@app.route("/api/v1.0/stations")
def sta():
    session = Session(engine)
    result=session.query(Stat.name).all()
    session.close()

    station_data=list(np.ravel(result))
    return jsonify(station_data)

@app.route("/api/v1.0/tobs")
def temperature():
    session = Session(engine)
    temp_data=session.query(Meas.tobs,Meas.date).\
    filter(Meas.date >year_to_date).all()
    session.close()

    tobs_data = list(np.ravel(temp_data))
    return jsonify(tobs_data)

start=dt.date(2012,1,1)
print(start)
total_data=[]
session=Session(engine)
max_start_data=session.query(func.max(Meas.tobs)).filter(Meas.date>=2012-1-1)
print(max_start_data)
@app.route("/api/v1.0/20120101")
def s_date():
    session=Session(engine)
    max_start_data=session.query(func.max(Meas.tobs)).filter(Meas.date>=start)
    avg_data=session.query(func.avg(Meas.tobs)).filter(Meas.date>=start)
    min_data=session.query(func.min(Meas.tobs)).filter(Meas.date>=start)
    session.close()

    m_data=list(max_start_data)
    a_data=list(avg_data)
    mi_data=list(min_data)
   
    tempdict = {
   "max_temp": m_data[0],
   "avg_temp": a_data[0],
   "min_temp": mi_data[0]
}
   
   
    resp=jsonify(tempdict)
    return resp
   


end=dt.date(2013,1,1)
t_data=[]
@app.route("/api/v1.0/20120101/20130101")
def s_end_date():
    session=Session(engine)
    ma_data=session.query(func.max(Meas.tobs)).filter(Meas.date>=start).filter(Meas.date<=end)
    a_data=session.query(func.avg(Meas.tobs)).filter(Meas.date>=start).filter(Meas.date<=end)
    mi_data=session.query(func.min(Meas.tobs)).filter(Meas.date>=start).filter(Meas.date<=end)
    session.close()

    # t_data=list.append((np.ravel(ma_data)))
    # t_data=list.append((np.ravel(a_data)))
    # t_data=list.append((np.ravel(mi_data)))

    mx_data=list(ma_data)
    avg_data=list(a_data)
    min_data=list(mi_data)

    tdict = {
   "max_temp": mx_data[0],
   "avg_temp": avg_data[0],
   "min_temp": min_data[0]
}
   
    return jsonify(tdict)

  
 

if __name__ == '__main__':
    app.run(debug=True)