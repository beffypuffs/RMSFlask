import os
from bs4 import BeautifulSoup as bs
from datetime import datetime, timedelta
import random
import Connections

def translate_history(db, Grinds, directory):
    count = 0
    total = 0
    connection, message = Connections.sql_connect()
    cur = connection.cursor()
    delete_these = [] #files to be deleted
    for filename in os.listdir(directory):
        #print(filename)
        with open(directory + '/' + filename, 'r', errors='ignore') as f:
            total += 1
            data = f.read()

            before = data.find('<RollDiameterAfterGrindingTailstock>')
            after = data.find(']]></RollDiameterAfterGrindingTailstock>')
            TS_diameter_after = data[before + 103:after].replace(" ", "")

        
            before = data.find('<RollDiameterAfterGrindingMiddle>')
            after = data.find(']]></RollDiameterAfterGrindingMiddle>')
            mid_diameter_after = data[before + 103:after].replace(" ", "")
            
            before = data.find('<RollDiameterAfterGrindingHeadstock>')
            after = data.find(']]></RollDiameterAfterGrindingHeadstock>')
            HS_diameter_after = data[before + 102:after].replace(" ", "")
            # print(len(TS_diameter_after))
            # print('--------------------------------')
            # print(len(mid_diameter_after))
            # print('--------------------------------')
            # print(len(HS_diameter_after))

            if (TS_diameter_after == '0' or TS_diameter_after == '' or len(TS_diameter_after) > 100) or (mid_diameter_after == '0' or mid_diameter_after == '' or len(mid_diameter_after) > 100) or (HS_diameter_after == '0' or HS_diameter_after == '' or len(HS_diameter_after) > 100):
                None
            else:
                before = data.find('<ProcessDone><!--Indicates that the machining process is completed--')
                after = data.find(']]></ProcessDone>')
                process_done = data[before + 78:after].replace(" ", "")

                before = data.find('<ProcessInterrupted><!--Indicates that the machining')
                after = data.find(']]></ProcessInterrupted>')
                process_interrupted = data[before + 87:after].replace(" ", "")

                before = data.find('<RollSerialNumber><!--Unique Roll Identifier-->')
                after = data.find(']]></RollSerialNumber>')
                roll_num = data[before + 56:after].replace(" ", "")

                before = data.find('<RollType><!--Roll type identifier e.g. BACKUP ROLL--><![')
                after = data.find(']]></RollType>')
                roll_type = data[before + 63:after].replace(" ", "")

                before = data.find('<GrindId><!--Used grind id, combination of process cycles and roll shape--><![CDATA[')
                after = data.find(']]></GrindId>')
                grind_id = data[before + 84:after].replace(" ", "")

                before = data.find('<Operator><!--The machine operator--><![CDATA[')
                after = data.find(']]></Operator>')
                operator = data[before + 46:after].replace(" ", "")
                
                before = data.find('<StartGrind><!--Start date & time of machining process--><![')
                after = data.find(']]></StartGrind>')
                grind_start = data[before +66 :after].replace(" ", "")

                before = data.find('<EndGrind><!--End date & time of machining process--><![CDATA[')
                after = data.find(']]></EndGrind>')
                grind_end = data[before + 62:after].replace(" ", "")
                    
                #grind_end = datetime.date(grind_end)
                ##needed for sql


                before = data.find('<ProgramNo><!--The used process cycles program name--><![CDATA[')
                after = data.find(']]></ProgramNo>')
                program_no = data[before + 63:after].replace(" ", "")

                before = data.find('<ShapeNo><!--The used roll shape name--><![CDATA[')
                after = data.find(']]></ShapeNo>')
                shape_no = data[before + 49:after].replace(" ", "")
                
                before = data.find('<TargetDiameter><!--The target diameter of the roll--><![CDATA[')
                after = data.find(']]></TargetDiameter>')
                target_diameter = data[before + 63:after].replace(" ", "")
            
                before = data.find('<RollDiameterBeforeGrindingTailstock>')
                after = data.find(']]></RollDiameterBeforeGrindingTailstock>')
                TS_diameter_before = data[before + 104:after].replace(" ", "")
                
                before = data.find('<RollDiameterBeforeGrindingMiddle>')
                after = data.find(']]></RollDiameterBeforeGrindingMiddle>')
                mid_diameter_before = data[before + 105:after].replace(" ", "")

                before = data.find('<RollDiameterBeforeGrindingHeadstock><!--Roll diameter before grinding at the headstock side--><![CDATA[')
                after = data.find(']]></RollDiameterBeforeGrindingHeadstock>')
                HS_diameter_before = data[before + 104:after].replace(" ", "")

                before = data.find('<FormTolerance><!--Target shape tolerance--><![CDATA[')
                after = data.find(']]></FormTolerance>')
                tolerance = data[before + 53:after].replace(" ", "")

                before = data.find('<ZDistance><!--Distance between measuring points--><![CDATA[')
                after = data.find(']]></ZDistance>')
                Zdistance = data[before + 60:after].replace(" ", "")

                before = data.find('<ZRefData><!--Reference roll shape z-Axis positions, Expect "Zpoints" data points--><![CDATA[')
                after = data.find(']]></ZRefData>')
                Z_ref_data = data[before + 93:after].replace(" ", "")

                before = data.find('<ShapeBeforeGrinding><!--Measured roll shape before grinding, Expect "Zpoints" data points--><![CDATA[')
                after = data.find(']]></ShapeBeforeGrinding>')
                shape_before_grinding = data[before + 102:after].replace(" ", "")

                before = data.find('<ShapeAfterGrinding><!--Measured roll shape after grinding, Expect "Zpoints" data points--><![CDATA[')
                after = data.find(']]></ShapeAfterGrinding>')
                shape_after_grinding = data[before + 100:after].replace(" ", "")

                before = data.find('<DeviationBeforeGrinding><!--Measured roll shape deviation before grinding, Expect "Zpoints" data points--><![CDATA[')
                after = data.find(']]></DeviationBeforeGrinding>')
                deviation_before_grinding = data[before + 116:after].replace(" ", "")

                before = data.find('<DeviationAfterGrinding><!--Measured roll shape deviation before grinding, Expect "Zpoints" data points--><![CDATA[')
                after = data.find(']]></DeviationAfterGrinding>')
                deviation_after_grinding = data[before + 115:after].replace(" ", "")

                min_diameter_before = 0
                min_diameter_after = 0
                
                # if(roll_num == '16043'):
                #     print(TS_diameter_after)
                #     print(mid_diameter_after)
                #     print(HS_diameter_after)
                # if (TS_diameter_after is not 0 or '' and mid_diameter_after is not 0 or '' and HS_diameter_after is not 0 or ''):
                #     min_diameter_before = min(float(TS_diameter_before), float(mid_diameter_before), float(HS_diameter_before))
                #     min_diameter_after = min(float(TS_diameter_after), float(mid_diameter_after), float(HS_diameter_after))

                
                if (HS_diameter_after is not '' or '0') and (TS_diameter_after is not '' or 0) and (mid_diameter_after is not '' or 0) and before is not -1:
                    count += 1
                    grind_end = datetime.strptime(grind_end, '%d_%m_%Y_%H_%M_%S')
                    min_diameter = min_diameter_after * 0.0393701
                    diameter_change = (min_diameter_before - min_diameter_after) * 0.0393701
                    # print(roll_num)
                    if (roll_num == '16043'):
                        pass
                        print(min_diameter)
                    
                    newGrind = Grinds(roll_num=roll_num, entry_time=grind_end, HS_before=HS_diameter_before, MD_before=mid_diameter_before, TS_before=TS_diameter_before, HS_after=HS_diameter_after, MD_after=mid_diameter_after,
                    TS_after=TS_diameter_after, diameter_change=diameter_change, max_deviation=0, min_deviation=0, roll_length=0, crowning_length=0, crowning_angle=0, crowning_bevel=0)
                    # cur.execute(f'DELETE FROM grind_new WHERE grind_end = \'{str(grind_end)}\'')
                    # try:
                    #     cur.execute(f'INSERT INTO grind_new VALUES({roll_num}, {min_diameter}, \'{str(grind_end)}\', {diameter_change})')
                    # except:
                    #     pass
                    #try:
                    print(filename)
                    db.session.add(newGrind)
                    
                    # cur.execute(f'UPDATE roll_new SET diameter = ROUND({min_diameter_after * 0.0393701},4) WHERE roll_num = {roll_num}')
                    # connection = Connections.sql_connect()
                    #cur = connection.cursor()
                    #cur.execute(f'INSERT INTO Grind_Raw VALUES({roll_num}, {grind_id}, {grind_start}, {grind_end}, {program_no}, {shape_no}, {TS_diameter_before}, {TS_diameter_after}, {mid_diameter_before}, {mid_diameter_after}, {HS_diameter_before}, {HS_diameter_after}, {average_diameter_before}, {average_diameter_after},'
                    #     f'{target_diameter}, {ZDistance}, {Z_ref_data}, {shape_before_grinding}, {shape_after_grinding}, {tolerance}, {deviation_before_grinding}, {deviation_after_grinding})')
    print(f'Valid entries: {count}')
    print(f'Invalid entries: {total - count}')
    db.session.commit()
    # connection.commit()


# directory = 'grindFiles/X files'
# translate_history(directory) #change user)
def add_grind(db, Grinds, roll_num, grind_end, HS_diameter_before, mid_diameter_before, TS_diameter_before, HS_diameter_after, mid_diameter_after, TS_diameter_after, diameter_change):
    newGrind = Grinds(roll_num=roll_num, entry_time=grind_end, HS_before=HS_diameter_before, MD_before=mid_diameter_before, TS_before=TS_diameter_before, HS_after=HS_diameter_after, MD_after=mid_diameter_after,
                    TS_after=TS_diameter_after, diameter_change=diameter_change, max_deviation=0, min_deviation=0, roll_length=0, crowning_length=0, crowning_angle=0, crowning_bevel=0)
    db.session.add(newGrind)

# def temp_function_delete(db, Roll, Info):
#     rolls = db.session.query(Roll).all()
#     for roll in rolls:
#         info = db.session.query(Info).filter_by(mill=roll.mill, roll_type=roll.roll_type).first()
#         roll.avg_grind = info.avg_grind_diameter
#         roll.days_between_grinds = info.days_between_rolls
#     db.session.commit()

def update_data(db, Roll, Grinds, Info, cur_date, diameter_change):
    grinds = db.session.query(Grinds).filter_by(roll_num=Roll.roll_num).order_by(Grinds.entry_time.desc())
    if (grinds.count() > 1):
        last_grind = grinds[1]
        delta = cur_date - last_grind.entry_time
        if grinds.count() == 1:
            Roll.days_between_grinds = delta
        else:
            Roll.days_between_grinds = ((Roll.days_between_grinds * Roll.num_grinds) + delta.days) / (Roll.num_grinds+1)
        Roll.num_grinds = Roll.num_grinds + 1
        Roll.avg_grind = ((Roll.avg_grind * (Roll.num_grinds - 1)) + diameter_change)/Roll.num_grinds
        Info.num_grinds = Info.num_grinds + 1
        Info.avg_grind_diameter = ((Info.avg_grind_diameter * (Info.num_grinds - 1) + diameter_change)/Info.num_grinds)
    else:
        Roll.num_grinds = 1
        Info.num_grinds = Info.num_grinds + 1
        Info.avg_grind_diameter = ((Info.avg_grind_diameter * (Info.num_grinds - 1) + diameter_change)/Info.num_grinds)
        Roll.avg_grind = diameter_change

def make_data(db, Roll, Grinds, Info):
    db.session.query(Grinds).delete()
    rolls = db.session.query(Roll).all()
    double_grind_chance = 20

    for roll in rolls:
        info = db.session.query(Info).filter_by(mill=roll.mill, roll_type=roll.roll_type).first()
        roll.diameter = info.scrap_diameter + 1
        cur_date = datetime.today()
        double_grind_chance = 20 
        while cur_date < datetime(2028, 1, 1) and roll.diameter > info.scrap_diameter:
            double_result = random.randrange(1, 100)
           # print(cur_date)
            diameter_change = (random.randrange(5, 15) / 10) * info.avg_grind_diameter
            day_change = (random.randrange(5, 15)/ 10) * info.days_between_rolls
            roll.diameter = roll.diameter - diameter_change
            newGrind = Grinds(roll_num=roll.roll_num, entry_time=cur_date, HS_before=roll.diameter + diameter_change, MD_before=roll.diameter + diameter_change, TS_before=roll.diameter + diameter_change, HS_after=roll.diameter, MD_after=roll.diameter,
                    TS_after=roll.diameter, min_diameter_change=diameter_change, max_deviation=0, min_deviation=0, roll_length=0, crowning_length=0, crowning_angle=0, crowning_bevel=0, min_diameter=roll.diameter)
            db.session.add(newGrind)
            update_data(db, roll, Grinds, info, cur_date, diameter_change)
            if double_result <= double_grind_chance:
                double_grind_chance + 3
                cur_date = cur_date + timedelta(minutes=5)
                roll.diameter = roll.diameter - diameter_change
                newGrind = Grinds(roll_num=roll.roll_num, entry_time=cur_date, HS_before=roll.diameter + diameter_change, MD_before=roll.diameter + diameter_change, TS_before=roll.diameter + diameter_change, HS_after=roll.diameter, MD_after=roll.diameter,
                     TS_after=roll.diameter, min_diameter_change=diameter_change, max_deviation=0, min_deviation=0, roll_length=0, crowning_length=0, crowning_angle=0, crowning_bevel=0, min_diameter=roll.diameter)
                db.session.add(newGrind)
                update_data(db, roll, Grinds, info, cur_date, diameter_change)
            
            cur_date = cur_date + timedelta(days=day_change)
    db.session.commit()

    


# directory = 'grindFiles/y files'
# translate_history(directory)

