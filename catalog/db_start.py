from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from db_setup import *

engine = create_engine('sqlite:///pendrives.db')
# Binding the engine
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# establishing or creating connections with database
# and represents a "staging zone" for all the objects loaded into the
session = DBSession()

# Remove pendrivesCompanyName if exisitng.
session.query(PenDrivesCompanyName).delete()
# Remove PenDriveName if exisitng.
session.query(PenDriveName).delete()
# Remove PenDriveUser if exisitng.
session.query(PenDriveUser).delete()

# establishing users connections
User1 = PenDriveUser(pdusername="ANANTHA LAVANYA TUMMALAPALLI",
                     email="lavanyatummala777@gmail.com", picture='sample.jpg')
session.add(User1)
session.commit()
print ("Successfully Add First User")
User10 = PenDriveUser(pdusername="KANAMARLAPUDI TEJASRI",
                      email="ammulukruthika777@gmail.com",
                      picture='sample.jpg')
session.add(User10)
session.commit()
print ("Successfully Add Second User")
# adding pendrive companys whichare familiar to us
pdcompany10 = PenDrivesCompanyName(pdusername="SANDISK",
                                   pduser_id=1)
session.add(pdcompany10)
session.commit()

pdcompany20 = PenDrivesCompanyName(pdusername="KINGSTON",
                                   pduser_id=1)
session.add(pdcompany20)
session.commit

pdcompany30 = PenDrivesCompanyName(pdusername="STRONTIUM",
                                   pduser_id=1)
session.add(pdcompany30)
session.commit()

pdcompany40 = PenDrivesCompanyName(pdusername="SONY",
                                   pduser_id=1)
session.add(pdcompany40)
session.commit()

pdcompany50 = PenDrivesCompanyName(pdusername="HP",
                                   pduser_id=1)
session.add(pdcompany50)
session.commit()

pdcompany60 = PenDrivesCompanyName(pdusername="SOLIMO",
                                   pduser_id=1)
session.add(pdcompany60)
session.commit()
# Popular  PENDRIVES of different companies with different models
pendriveName1 = PenDriveName(pdusername="Cruzer Blade",
                             drives_number="1",
                             item_capacity="32GB",
                             drive_name="USB2.0",
                             item_color="Multicolor",
                             transferspeed="480 megabits per second",
                             item_cost="427RS",
                             otgfacility="no",
                             warranty="5 years",
                             date=datetime.datetime.now(),
                             pendrivecompanyid=1,
                             pduser_id=1)
session.add(pendriveName1)
session.commit()
pendriveName10 = PenDriveName(pdusername="Ultra Dual Drive",
                              drives_number="2",
                              item_capacity="128GB",
                              drive_name="USB3.0",
                              item_color="Silver",
                              transferspeed="640 megabits per second",
                              item_cost="2370RS",
                              otgfacility="yes",
                              warranty="5 years",
                              date=datetime.datetime.now(),
                              pendrivecompanyid=1,
                              pduser_id=1)
session.add(pendriveName10)
session.commit()
pendriveName100 = PenDriveName(pdusername="Ultra dual",
                               drives_number="2",
                               item_capacity="32GB",
                               drive_name="USB3.0",
                               item_color="Gold",
                               transferspeed="640 megabits per second",
                               item_cost="589RS",
                               otgfacility="yes",
                               warranty="5 years",
                               date=datetime.datetime.now(),
                               pendrivecompanyid=1,
                               pduser_id=1)
session.add(pendriveName100)
session.commit()
pendriveName2 = PenDriveName(pdusername="DTIG",
                             drives_number="1",
                             item_capacity="32GB",
                             drive_name="USB3.0",
                             item_color="White and red",
                             transferspeed="640 megabits per second",
                             item_cost="499RS",
                             otgfacility="no",
                             warranty="5 years",
                             date=datetime.datetime.now(),
                             pendrivecompanyid=2,
                             pduser_id=1)
session.add(pendriveName2)
session.commit()
pendriveName20 = PenDriveName(pdusername="DTIG4",
                              drives_number="2",
                              item_capacity="64GB",
                              drive_name="USB3.0",
                              item_color="Gold",
                              transferspeed="640 megabits per second",
                              item_cost="2333RS",
                              otgfacility="yes",
                              warranty="5 years",
                              date=datetime.datetime.now(),
                              pendrivecompanyid=2,
                              pduser_id=1)
session.add(pendriveName20)
session.commit()
pendriveName200 = PenDriveName(pdusername="Data Traveler",
                               drives_number="2",
                               item_capacity="32GB",
                               drive_name="USB2.0",
                               item_color="Silver",
                               transferspeed="480 megabits per second",
                               item_cost="569RS",
                               otgfacility="no",
                               warranty="5 years",
                               date=datetime.datetime.now(),
                               pendrivecompanyid=2,
                               pduser_id=1)
session.add(pendriveName200)
session.commit()
pendriveName2000 = PenDriveName(pdusername="Data",
                                drives_number="1",
                                item_capacity="16GB",
                                drive_name="USB2.0",
                                item_color="Black",
                                transferspeed="480 megabits per second",
                                item_cost="522RS",
                                otgfacility="yes",
                                warranty="5 years",
                                date=datetime.datetime.now(),
                                pendrivecompanyid=2,
                                pduser_id=1)
session.add(pendriveName2000)
session.commit()
pendriveName3 = PenDriveName(pdusername="Ammo",
                             drives_number="1",
                             item_capacity="8GB",
                             drive_name="USB2.0",
                             item_color="Silver",
                             transferspeed="480 megabits per second",
                             item_cost="567RS",
                             otgfacility="no",
                             warranty="5 years",
                             date=datetime.datetime.now(),
                             pendrivecompanyid=3,
                             pduser_id=1)
session.add(pendriveName3)
session.commit()
pendriveName30 = PenDriveName(pdusername="Nitro Plus",
                              drives_number="2",
                              item_capacity="32GB",
                              drive_name="USB2.0",
                              item_color="silver",
                              transferspeed="480 megabits per second",
                              item_cost="999RS",
                              otgfacility="yes",
                              warranty="5 years",
                              date=datetime.datetime.now(),
                              pendrivecompanyid=3,
                              pduser_id=1)
session.add(pendriveName30)
session.commit()
pendriveName300 = PenDriveName(pdusername="pollex",
                               drives_number="1",
                               item_capacity="32GB",
                               drive_name="USB2.0",
                               item_color="black",
                               transferspeed="480 megabits per second",
                               item_cost="369RS",
                               otgfacility="no",
                               warranty="5 years",
                               date=datetime.datetime.now(),
                               pendrivecompanyid=3,
                               pduser_id=1)
session.add(pendriveName300)
session.commit()
pendriveName4 = PenDriveName(pdusername="Microvault",
                             drives_number="1",
                             item_capacity="16GB",
                             drive_name="USB2.0",
                             item_color="white",
                             transferspeed="480 megabits per second",
                             item_cost="340RS",
                             otgfacility="no",
                             warranty="5 years",
                             date=datetime.datetime.now(),
                             pendrivecompanyid=4,
                             pduser_id=1)
session.add(pendriveName4)
session.commit()
pendriveName40 = PenDriveName(pdusername="USM",
                              drives_number="1",
                              item_capacity="32GB",
                              drive_name="USB2.0",
                              item_color="Gold",
                              transferspeed="480 megabits per second",
                              item_cost="410RS",
                              otgfacility="no",
                              warranty="5 years",
                              date=datetime.datetime.now(),
                              pendrivecompanyid=4,
                              pduser_id=1)
session.add(pendriveName40)
session.commit()
pendriveName400 = PenDriveName(pdusername="BSM",
                               drives_number="2",
                               item_capacity="64GB",
                               drive_name="USB3.1",
                               item_color="yellow",
                               transferspeed="10 gigabits per second",
                               item_cost="979RS",
                               otgfacility="yes",
                               warranty="2 years",
                               date=datetime.datetime.now(),
                               pendrivecompanyid=4,
                               pduser_id=1)
session.add(pendriveName400)
session.commit()
pendriveName5 = PenDriveName(pdusername="v152w",
                             drives_number="1",
                             item_capacity="32GB",
                             drive_name="USB2.0",
                             item_color="Blue",
                             transferspeed="480 megabits per second",
                             item_cost="499RS",
                             otgfacility="no",
                             warranty="1 years",
                             date=datetime.datetime.now(),
                             pendrivecompanyid=5,
                             pduser_id=1)
session.add(pendriveName100)
session.commit()
pendriveName50 = PenDriveName(pdusername="x765w",
                              drives_number="1",
                              item_capacity="32GB",
                              drive_name="USB3.0",
                              item_color="white",
                              transferspeed="640 megabits per second",
                              item_cost="694RS",
                              otgfacility="yes",
                              warranty="2 years",
                              date=datetime.datetime.now(),
                              pendrivecompanyid=5,
                              pduser_id=1)
session.add(pendriveName50)
session.commit()

print("Your Pendrives database has been inserted!")
