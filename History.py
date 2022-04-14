import os
from bs4 import BeautifulSoup as bs
from datetime import datetime, timedelta
from models import *
import random
import Connections

def translate_history(directory):
    count = 0
    total = 0
    delete_these = [] #files to be deleted
    files = os.listdir(directory)
    files.sort()
    for file in files:
        print(file)

    
    for filename in files:
        with open(directory + '/' + file, 'r', errors='ignore') as f:
            if file == 'Windows Portable Devices':
                os.remove(file)
            else:
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

                    
                    if (HS_diameter_after != ('' or '0')) and (TS_diameter_after !=  ('' or 0)) and (mid_diameter_after != ('' or 0)):
                        count += 1
                        grind_end = datetime.strptime(grind_end, '%d_%m_%Y_%H_%M_%S')
                        min_diameter = min_diameter_after * 0.0393701
                        diameter_change = (min_diameter_before - min_diameter_after) * 0.0393701
                        # print(roll_num)
                        # if (roll_num == '16043'):
                        #     pass
                        #     print(min_diameter)
                        roll = db.session.query(Roll).filter_by(roll_num=roll_num)
                        newGrind = Grind(roll_num=roll_num, entry_time=grind_end, HS_before=HS_diameter_before, MD_before=mid_diameter_before, TS_before=TS_diameter_before, HS_after=HS_diameter_after, MD_after=mid_diameter_after,
                        TS_after=TS_diameter_after, diameter_change=diameter_change, max_deviation=0, min_deviation=0, roll_length=0, crowning_length=0, crowning_angle=0, crowning_bevel=0)
                        roll.add_grind(newGrind)   
                        db.session.add(newGrind)#adds the new grind to the database
                    
    
    print(f'Valid entries: {count}')
    print(f'Invalid entries: {total - count}')#should probably log this
    db.session.commit() #]
    # connection.commit()

    



# directory = 'grindFiles'
# translate_history(directory)

