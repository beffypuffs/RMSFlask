import flask_testing
import tempfile
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
import unittest
from flask import Flask
from models import *
from Requests import *
from Connections import *
from datetime import datetime, timedelta
import responses
from responses import GET, POST
import random


# class test_Server_Connection(flask_testing.TestCase):
#     def create_app(self):
#         return create_app(self, 'mssql+pymssql://RMS:trpJ63iGY4F7mRj@rmssql.database.windows.net/RMSSQL')

#     def setUp(self):
#         Base = automap_base() #Makes a class for all tables in the database
#         Base.prepare(db.engine, reflect = True)
#         Roll = Base.classes.roll_new
#         Grind = Base.classes.grind_new #what is displayed
#         Grinds = Base.classes.Grinds #closer to what the final grind class should look like
#         Info = Base.classes.roll_info

#     def test_grab_roll(self):
#         rolls = db.session.query(Roll).all()
#         print(roll.first())

#     def tearDown(self):
#         db.session.remove()
#         #db.drop_all()


class test_Fake_Server(flask_testing.TestCase):
    def create_app(self):
        return create_app(self, "sqlite:////tmp/test.db")

    # def test_add_roll(self):
    #     newRoll = Roll(roll_num = 1, diameter = 1.1)
    #     db.session.add(newRoll)
    #     rolls = db.session.query(Roll).all()
    #     assert len(rolls) == 1
    #     assert rolls[0].roll_num == 1
    #     assert rolls[0].diameter == 1.1
    

    def test_add_rollgrind(self):
        newRoll = Roll(roll_num = 1, diameter = 80, scrap_diameter=70, approx_scrap_date = datetime(2012, 12, 12), grinds_left=0, mill='80', roll_type='IMR', avg_grind=0, days_between_grinds=0, num_grinds=0, scrapped = False)
        db.session.add(newRoll)
        newRoll.avg_grind_stats(timedelta(weeks = 52))
        newInfo = Info(mill='80', roll_type='IMR', scrap_diameter = 70, avg_grind_diameter=.1, days_between_grinds=10, num_grinds=2)
        db.session.add(newInfo)
        grinds = db.session.query(Grind).all()
        rolls = db.session.query(Roll).all()
        info = db.session.query(Info).filter_by(mill=rolls[0].mill, roll_type=rolls[0].roll_type)[0]
       
        
        assert info.avg_grind_diameter==.1
        assert len(rolls) == 1
        assert len(grinds) == 0

        newGrind = Grind(roll_num = 1, entry_time = datetime(2021, 12, 1), HS_before = rolls[0].diameter, MD_before = rolls[0].diameter, TS_before = rolls[0].diameter, HS_after = rolls[0].diameter - .05, MD_after = rolls[0].diameter - .05, TS_after = rolls[0].diameter - .05,   min_diameter_change = .05, max_deviation=0, min_deviation=0, roll_length=0, crowning_length=0, crowning_angle=0, crowning_bevel=0, min_diameter = rolls[0].diameter - .05)
        rolls[0].add_grind(newGrind)
        grinds = db.session.query(Grind).all()
        assert info.avg_grind_diameter == .1
        assert info.num_grinds == 2
        assert info.days_between_grinds == 10
        assert len(grinds)== 1
        assert grinds[0].roll_num == 1
        assert grinds[0].entry_time == datetime(2021, 12, 1)
        assert grinds[0].min_diameter_change == .05
        assert grinds[0].min_diameter == 79.95


        newGrind = Grind(roll_num = 1, entry_time = datetime(2021, 12, 10), HS_before = rolls[0].diameter, MD_before = rolls[0].diameter, TS_before = rolls[0].diameter, HS_after = rolls[0].diameter - .05, MD_after = rolls[0].diameter - .05, TS_after = rolls[0].diameter - .05,   min_diameter_change = .05, max_deviation=0, min_deviation=0, roll_length=0, crowning_length=0, crowning_angle=0, crowning_bevel=0, min_diameter = rolls[0].diameter - .05)
        rolls[0].add_grind(newGrind)

        grinds = db.session.query(Grind).all()
        assert len(grinds) == 2
        assert info.num_grinds == 3
        self.assertAlmostEqual(info.avg_grind_diameter, .0833, 4)
        self.assertAlmostEqual(info.days_between_grinds, 9.666, 0) # roll type info is succesfully updated

        assert rolls[0].num_grinds == 2
        assert rolls[0].avg_grind == .05
        assert rolls[0].diameter == 79.9 #roll info is succesfully updated

        newGrind = Grind(roll_num = 1, entry_time = datetime(2017, 12, 1), HS_before = rolls[0].diameter, MD_before = rolls[0].diameter, TS_before = rolls[0].diameter, HS_after = rolls[0].diameter - .05, MD_after = rolls[0].diameter - .05, TS_after = rolls[0].diameter - .05,   min_diameter_change = .05, max_deviation=0, min_deviation=0, roll_length=0, crowning_length=0, crowning_angle=0, crowning_bevel=0, min_diameter = rolls[0].diameter - .05)
        stats = rolls[0].avg_grind_stats(timedelta(weeks=52))


    def test_scrap_date(self):
        newInfo = Info(mill='80', roll_type='IMR', scrap_diameter = 70, avg_grind_diameter=.1, days_between_grinds=10, num_grinds=2)
        db.session.add(newInfo)


    def test_roll_stats(self):
        newRoll = Roll(roll_num = 1, diameter = 80, scrap_diameter=70, approx_scrap_date = datetime(2012, 12, 12), grinds_left=0, mill='80', roll_type='IMR', avg_grind=0, days_between_grinds=0, num_grinds=0, scrapped = False)
        db.session.add(newRoll)
        newInfo = Info(mill='80', roll_type='IMR', scrap_diameter = 70, avg_grind_diameter=.1, days_between_grinds=10, num_grinds=2)
        db.session.add(newInfo)

        today = datetime.today()

        #within 24 months

        new_grind = Grind(roll_num=1, entry_time = today - timedelta(weeks=101), HS_before = newRoll.diameter, MD_before=newRoll.diameter, TS_before=newRoll.diameter, HS_after=newRoll.diameter - .2, MD_after=newRoll.diameter - .2, TS_after=newRoll.diameter - .2, min_diameter_change= .2,max_deviation=0, min_deviation=0, roll_length=0, crowning_length=0, crowning_angle=0, crowning_bevel=0, min_diameter = newRoll.diameter - .2)
        newRoll.add_grind(new_grind)
        #print(newRoll.avg_grind)
        new_grind = Grind(roll_num=1, entry_time = today - timedelta(weeks=100), HS_before = newRoll.diameter, MD_before=newRoll.diameter, TS_before=newRoll.diameter, HS_after=newRoll.diameter - .2, MD_after=newRoll.diameter - .2, TS_after=newRoll.diameter - .2, min_diameter_change= .2,max_deviation=0, min_deviation=0, roll_length=0, crowning_length=0, crowning_angle=0, crowning_bevel=0, min_diameter = newRoll.diameter - .2)
        newRoll.add_grind(new_grind)
        #print(newRoll.avg_grind)
        new_grind = Grind(roll_num=1, entry_time = today - timedelta(weeks=90), HS_before = newRoll.diameter, MD_before=newRoll.diameter, TS_before=newRoll.diameter, HS_after=newRoll.diameter - .2, MD_after=newRoll.diameter - .2, TS_after=newRoll.diameter - .2, min_diameter_change= .2,max_deviation=0, min_deviation=0, roll_length=0, crowning_length=0, crowning_angle=0, crowning_bevel=0, min_diameter = newRoll.diameter - .2)
        newRoll.add_grind(new_grind)
        #print(newRoll.avg_grind)
        new_grind = Grind(roll_num=1, entry_time = today - timedelta(weeks=80), HS_before = newRoll.diameter, MD_before=newRoll.diameter, TS_before=newRoll.diameter, HS_after=newRoll.diameter - .2, MD_after=newRoll.diameter - .2, TS_after=newRoll.diameter - .2, min_diameter_change= .2,max_deviation=0, min_deviation=0, roll_length=0, crowning_length=0, crowning_angle=0, crowning_bevel=0, min_diameter = newRoll.diameter - .2)
        newRoll.add_grind(new_grind)
        #print(newRoll.avg_grind)
        new_grind = Grind(roll_num=1, entry_time = today - timedelta(weeks=70), HS_before = newRoll.diameter, MD_before=newRoll.diameter, TS_before=newRoll.diameter, HS_after=newRoll.diameter - .2, MD_after=newRoll.diameter - .2, TS_after=newRoll.diameter - .2, min_diameter_change= .2,max_deviation=0, min_deviation=0, roll_length=0, crowning_length=0, crowning_angle=0, crowning_bevel=0, min_diameter = newRoll.diameter - .2)
        newRoll.add_grind(new_grind)
        #print(newRoll.avg_grind)
        new_grind = Grind(roll_num=1, entry_time = today - timedelta(weeks=60), HS_before = newRoll.diameter, MD_before=newRoll.diameter, TS_before=newRoll.diameter, HS_after=newRoll.diameter - .2, MD_after=newRoll.diameter - .2, TS_after=newRoll.diameter - .2, min_diameter_change= .2,max_deviation=0, min_deviation=0, roll_length=0, crowning_length=0, crowning_angle=0, crowning_bevel=0, min_diameter = newRoll.diameter - .2)
        newRoll.add_grind(new_grind)

        #print(newRoll.avg_grind)

        

        


        #within 12 months

        new_grind = Grind(roll_num=1, entry_time = today - timedelta(weeks=47), HS_before = newRoll.diameter, MD_before=newRoll.diameter, TS_before=newRoll.diameter, HS_after=newRoll.diameter - .5, MD_after=newRoll.diameter - .5, TS_after=newRoll.diameter - .5, min_diameter_change= .5,max_deviation=0, min_deviation=0, roll_length=0, crowning_length=0, crowning_angle=0, crowning_bevel=0, min_diameter = newRoll.diameter - .5)
        newRoll.add_grind(new_grind)
        new_grind = Grind(roll_num=1, entry_time = today - timedelta(weeks=46), HS_before = newRoll.diameter, MD_before=newRoll.diameter, TS_before=newRoll.diameter, HS_after=newRoll.diameter - .5, MD_after=newRoll.diameter - .5, TS_after=newRoll.diameter - .5, min_diameter_change= .5,max_deviation=0, min_deviation=0, roll_length=0, crowning_length=0, crowning_angle=0, crowning_bevel=0, min_diameter = newRoll.diameter - .5)
        newRoll.add_grind(new_grind)
        new_grind = Grind(roll_num=1, entry_time = today - timedelta(weeks=45), HS_before = newRoll.diameter, MD_before=newRoll.diameter, TS_before=newRoll.diameter, HS_after=newRoll.diameter - .5, MD_after=newRoll.diameter - .5, TS_after=newRoll.diameter - .5, min_diameter_change= .5,max_deviation=0, min_deviation=0, roll_length=0, crowning_length=0, crowning_angle=0, crowning_bevel=0, min_diameter = newRoll.diameter - .5)
        newRoll.add_grind(new_grind)
        new_grind = Grind(roll_num=1, entry_time = today - timedelta(weeks=44, hours = 1), HS_before = newRoll.diameter, MD_before=newRoll.diameter, TS_before=newRoll.diameter, HS_after=newRoll.diameter - .5, MD_after=newRoll.diameter - .5, TS_after=newRoll.diameter - .5, min_diameter_change= .5,max_deviation=0, min_deviation=0, roll_length=0, crowning_length=0, crowning_angle=0, crowning_bevel=0, min_diameter = newRoll.diameter - .5)
        newRoll.add_grind(new_grind)
        new_grind = Grind(roll_num=1, entry_time = today - timedelta(weeks=40), HS_before = newRoll.diameter, MD_before=newRoll.diameter, TS_before=newRoll.diameter, HS_after=newRoll.diameter - .5, MD_after=newRoll.diameter - .5, TS_after=newRoll.diameter - .5, min_diameter_change= .5,max_deviation=0, min_deviation=0, roll_length=0, crowning_length=0, crowning_angle=0, crowning_bevel=0, min_diameter = newRoll.diameter - .5)
        newRoll.add_grind(new_grind)
        new_grind = Grind(roll_num=1, entry_time = today - timedelta(weeks=34), HS_before = newRoll.diameter, MD_before=newRoll.diameter, TS_before=newRoll.diameter, HS_after=newRoll.diameter - .5, MD_after=newRoll.diameter - .5, TS_after=newRoll.diameter - .5, min_diameter_change= .5,max_deviation=0, min_deviation=0, roll_length=0, crowning_length=0, crowning_angle=0, crowning_bevel=0, min_diameter = newRoll.diameter - .5)
        newRoll.add_grind(new_grind)

        #within 6 months
        new_grind = Grind(roll_num=1, entry_time = today - timedelta(weeks= 20), HS_before = newRoll.diameter, MD_before=newRoll.diameter, TS_before=newRoll.diameter, HS_after=newRoll.diameter - .2, MD_after=newRoll.diameter - .2, TS_after=newRoll.diameter - .2, min_diameter_change= .2, max_deviation=0, min_deviation=0, roll_length=0, crowning_length=0, crowning_angle=0, crowning_bevel=0, min_diameter = newRoll.diameter - .2)
        newRoll.add_grind(new_grind)
        new_grind = Grind(roll_num=1, entry_time = today - timedelta(weeks = 12), HS_before = newRoll.diameter, MD_before=newRoll.diameter, TS_before=newRoll.diameter, HS_after=newRoll.diameter - .2, MD_after=newRoll.diameter - .2, TS_after=newRoll.diameter - .2, min_diameter_change= .2,max_deviation=0, min_deviation=0, roll_length=0, crowning_length=0, crowning_angle=0, crowning_bevel=0, min_diameter = newRoll.diameter  - .2)
        newRoll.add_grind(new_grind)
        new_grind = Grind(roll_num=1, entry_time = today - timedelta(weeks= 8), HS_before = newRoll.diameter, MD_before=newRoll.diameter, TS_before=newRoll.diameter, HS_after=newRoll.diameter - .2, MD_after=newRoll.diameter - .2, TS_after=newRoll.diameter - .2, min_diameter_change= .2,max_deviation=0, min_deviation=0, roll_length=0, crowning_length=0, crowning_angle=0, crowning_bevel=0, min_diameter = newRoll.diameter - .2)
        newRoll.add_grind(new_grind)
        new_grind = Grind(roll_num=1, entry_time = today - timedelta(weeks= 6), HS_before = newRoll.diameter, MD_before=newRoll.diameter, TS_before=newRoll.diameter, HS_after=newRoll.diameter - .2, MD_after=newRoll.diameter - .2, TS_after=newRoll.diameter - .2, min_diameter_change= .2,max_deviation=0, min_deviation=0, roll_length=0, crowning_length=0, crowning_angle=0, crowning_bevel=0, min_diameter = newRoll.diameter - .2)
        newRoll.add_grind(new_grind)
        new_grind = Grind(roll_num=1, entry_time = today - timedelta(weeks=5), HS_before = newRoll.diameter, MD_before=newRoll.diameter, TS_before=newRoll.diameter, HS_after=newRoll.diameter - .2, MD_after=newRoll.diameter - .2, TS_after=newRoll.diameter - .2, min_diameter_change= .2,max_deviation=0, min_deviation=0, roll_length=0, crowning_length=0, crowning_angle=0, crowning_bevel=0, min_diameter = newRoll.diameter - .2)
        newRoll.add_grind(new_grind)
        new_grind = Grind(roll_num=1, entry_time = today - timedelta(weeks=4), HS_before = newRoll.diameter, MD_before=newRoll.diameter, TS_before=newRoll.diameter, HS_after=newRoll.diameter - .2, MD_after=newRoll.diameter - .2, TS_after=newRoll.diameter - .2, min_diameter_change= .2,max_deviation=0, min_deviation=0, roll_length=0, crowning_length=0, crowning_angle=0, crowning_bevel=0, min_diameter = newRoll.diameter - .2)
        newRoll.add_grind(new_grind)




        print(newRoll.avg_grind_stats(timedelta(weeks = 25)))
        print("------------------------")
        print(newRoll.avg_grind_stats(timedelta(weeks = 52)))
        print("------------------------")
        print(newRoll.avg_grind_stats(timedelta(weeks = 104)))
        print("------------------------")
        # print(newRoll.avg_grind)


    def test_add_info(self):
        newInfo = Info(mill=80, roll_type = 'Work', scrap_diameter=80, avg_grind_diameter=0, days_between_grinds=0, num_grinds=0)
        db.session.add(newInfo)
        info = db.session.query(Info).filter_by(mill=80, roll_type = 'Work')
        assert info.count() == 1
        assert info[0].roll_type == 'Work'
        assert info[0].scrap_diameter == 80
        assert info[0].avg_grind_diameter == 0
        assert info[0].days_between_grinds == 0
        assert info[0].num_grinds == 0

    # def test_graph(self):
    #     newRoll = Roll(roll_num = 10, diameter = 85, scrap_diameter = 75, mill = 80, roll_type = 'Work', num_grinds = 0)
    #     db.session.add(newRoll)
    #     cur_day = datetime.today()
    #     days_between_grinds = 44.6
    #     diameter_change = .5
    #     roll = db.session.query(Roll).filter_by(roll_num=10)[0]
    #     last_diameter = roll.diameter

    #     while cur_day < (datetime.today() + timedelta(days=365)):
    #         newGrind = Grind(roll_num = 10, entry_time = cur_day, diameter_change=diameter_change, min_diameter = last_diameter - diameter_change)
    #         last_diameter = last_diameter - diameter_change
    #         cur_day = cur_day + timedelta(days=days_between_grinds)
    #         db.session.add(newGrind)
    #     grinds = db.session.query(Grind).filter_by(roll_num=10)
    #     newInfo = Info(mill=80, roll_type = 'Work', scrap_diameter = 75, avg_grind_diameter = .6, days_between_grinds = 40, num_grinds = 10)
    #     db.session.add(newInfo)
    #     info = db.session.query(Info).filter_by(mill=roll.mill, roll_type=roll.roll_type)[0]
    #     update_data(db, roll, Grind, info)
    #     plt = generate_graphs(roll, grinds, info)
    #     assert roll.avg_grind == .5
    #     plt.savefig('static/images/Sample Graph.png')

    def test_add_chock(self):
        reports = db.session.query(Report).all()
        assert len(reports) == 0
        data = valid_chock_form(self)
        db.session.add(Report(data))
        reports = db.session.query(Report).all()
        assert len(reports) == 1 

    def test_add__invalid_chock(self):
        reports = db.session.query(Report).all()
        data = invalid_chock_form(self)
        assert len(reports) == 0
        try:
            db.session.add(Report(data))
        except:
            pass
        reports = db.session.query(Report).all()
        assert reports == []

    def test_remove_chock(self):
        reports = db.session.query(Report).all()
        assert len(reports) == 0
        data = valid_chock_form(self)
        db.session.add(Report(data))
        reports = db.session.query(Report).all()
        assert len(reports) == 1 
        db.session.query(Report).filter_by(date = reports[0].date, chock_number = reports[0].chock_number).delete()
        reports = db.session.query(Report).all()
        assert len(reports) == 0

    def test_edit_chock(self):
        reports = db.session.query(Report).all()
        assert len(reports) == 0
        data = valid_chock_form(self)
        db.session.add(Report(data))
        reports = db.session.query(Report).all()
        assert len(reports) == 1 
        assert reports[0].chock_number == "NOT NULL"
        reports[0].chock_number = "EDITED CHOCK NUMBER"
        assert reports[0].chock_number == "EDITED CHOCK NUMBER"

    

    def test_translate_history(self):
        pass #write a test for the translate history function

    # def test_roll_stats(self):
    #     newRoll = Roll(roll_num=1, diameter = 55.5, scrap_diameter = 50.5, approx_scrap_date = '12-12-12', grinds_left = 0, mill = '112', roll_type = 'BU', avg_grind = 0, days_between_grinds = 0, num_grinds = 0, scrapped = False)
    #     db.session.add(newRoll)
    #     newRoll = Roll(roll_num=1, diameter = 26, scrap_diameter = 25.984, approx_scrap_date = '12-12-12', grinds_left = 0, mill = '112', roll_type = 'WORK', avg_grind = 0, days_between_grinds = 0, num_grinds = 0, scrapped = False)
    #     db.session.add(newRoll)
    #     newRoll = Roll(roll_num=1, diameter = 60, scrap_diameter = 51.5, approx_scrap_date = '12-12-12', grinds_left = 0, mill = '132', roll_type = 'BU', avg_grind = 0, days_between_grinds = 0, num_grinds = 0, scrapped = False)
    #     db.session.add(newRoll)
    #     newRoll = Roll(roll_num=1, diameter = 37.5, scrap_diameter = 37, approx_scrap_date = '12-12-12', grinds_left = 0, mill = '132', roll_type = 'WORK', avg_grind = 0, days_between_grinds = 0, num_grinds = 0, scrapped = False)
    #     db.session.add(newRoll)

    #     avg1 = None
    #     avg2 = None
    #     avg3 = None
    #     avg4 = None
        

    #     rolls = db.session.query(Roll).all()
    #     for roll in rolls:
    #         cur_day = datetime.today()
    #         while (cur_day < '2025-01-01') and (roll.scrapped == False):
    #             diameter_change = .1 * random.randrange(5, 10)
    
    # def test_update_average(self):
    #     newRoll = Roll(roll_num=1, diameter = 55.5, scrap_diameter = 50.5, approx_scrap_date = datetime(2012, 12, 12), grinds_left = 0, mill = '112', roll_type = 'BU', avg_grind = 0, days_between_grinds = 0, num_grinds = 0, scrapped = False)
    #     db.session.add(newRoll)
    #     avg = None

    #     roll = db.session.query(Roll).filter_by(roll_num=1).first()
    #     newGrind = Grind(roll_num=1, )

        

        
    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()



def create_app(self, uri):
    app = Flask(__name__)
    self.app = app.app.test_client()
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    app.config['TESTING'] = True
    app.config["SQLALchemy_TRACK_MODIFICATIONS"] = False
    db.init_app(app)    
    return app

def test_index(self):
    response = self.app.get("/")
    print(response)



def valid_chock_form(self):
    data = ['2021-01-01']
    for i in range(53):
        data.append('NOT NULL')
    return data


def invalid_chock_form(self):
    data = ['NOT', 'VALID']


if __name__ == "__main__":
    unittest.main()