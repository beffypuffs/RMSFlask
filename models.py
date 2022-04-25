from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import datetime
import matplotlib
import math
import matplotlib.pyplot as plt
db=SQLAlchemy()

class Roll(db.Model):
        __tablename__ = 'roll_new'
        roll_num = db.Column(db.Integer, primary_key=True, autoincrement=False)
        diameter = db.Column(db.Float, nullable=False)
        scrap_diameter = db.Column(db.Float, nullable=False)
        approx_scrap_date = db.Column(db.DateTime, nullable=False, default='12-12-12')
        grinds_left = db.Column(db.Integer, nullable=True)
        mill = db.Column(db.String, nullable=False)
        roll_type = db.Column(db.String, nullable=False)
        avg_grind = db.Column(db.Float, nullable=True)
        days_between_grinds = db.Column(db.Float, nullable=True)
        num_grinds = db.Column(db.Integer, nullable = False)
        scrapped = db.Column(db.Boolean, nullable=False)


        def add_grind(self, grind):
                info = db.session.query(Info).filter_by(mill=self.mill, roll_type=self.roll_type)[0]
                
                

                if self.num_grinds == 0:
                        self.diameter = self.diameter - grind.min_diameter_change
                        self.avg_grind = grind.min_diameter_change
                        db.session.add(grind)
                else: 
                        last_grind = db.session.query(Grind).filter_by(roll_num=self.roll_num)[-1]
                        delta = grind.entry_time - last_grind.entry_time
                        db.session.add(grind)
                        # print(delta)
                        # print(delta.total_seconds()/86400)
                        if self.num_grinds == 1:
                                self.days_between_grinds = delta.total_seconds()/86400
                        else:
                                self.days_between_grinds = ((self.days_between_grinds * self.num_grinds) + (delta.total_seconds()/86400))/(self.num_grinds + 1)
                        
                        self.diameter = self.diameter - grind.min_diameter_change   
                        
                        self.avg_grind = ((self.avg_grind * float(self.num_grinds)) + grind.min_diameter_change) / (float(self.num_grinds + 1))
                        info.avg_grind_diameter = ((info.avg_grind_diameter * info.num_grinds) + grind.min_diameter_change)/ (info.num_grinds + 1)
                        days = ((info.days_between_grinds * info.num_grinds) + (delta/datetime.timedelta(days=1)))/(info.num_grinds + 1)
                        info.days_between_grinds = days
                        info.num_grinds += 1
                        self.update_scrap_date()
                
                self.num_grinds += 1 
                db.session.commit()
                

        def update_scrap_date(self):
                info = db.session.query(Info).filter_by(mill=self.mill, roll_type=self.roll_type)[0]
                grinds = db.session.query(Grind).filter_by(roll_num=self.roll_num).order_by(Grind.entry_time.desc())
                if grinds.count() > 0:  
                        cur_day = grinds[0].entry_time
                        diameter = self.diameter
                        grinds = 0

                        while diameter > info.scrap_diameter:
                                cur_day += datetime.timedelta(days=info.days_between_grinds)
                                diameter -= info.avg_grind_diameter
                                grinds += 1
                        self.approx_scrap_date = cur_day
                        self.grinds_left = grinds
                        if grinds == 0:
                                self.scrapped = True
                        else:
                                self.scrapped = False

        def generate_graphs(self, grinds, info):
                y = []
                x = []
                dates = []
                data_exists = False
                for grind in grinds:
                        data_exists = True
                        x.append(grind.entry_time)
                        y.append(grind.min_diameter)


                fig, ax = plt.subplots()
                other_diameter = self.calculate_12mo_diameter(info.scrap_diameter, info.days_between_grinds, info.avg_grind_diameter)

                if grinds.count() > 0:
                        cur_day = datetime.date(x[-1].year, x[-1].month, x[-1].day)
                        trend_x = []
                        trend_y = []
                        trend2_y = []
                        trend2_x = []
                        diameter_proj = self.diameter

                        while diameter_proj > info.scrap_diameter:#projection based on roll type average grind
                                trend_y.append(diameter_proj)
                                trend_x.append(cur_day)
                                diameter_proj = diameter_proj - info.avg_grind_diameter
                                cur_day = cur_day + datetime.timedelta(days=info.days_between_grinds)

                        trend_y.append(info.scrap_diameter)
                        trend_x.append(cur_day)

                        diameter_proj = self.diameter
                        cur_day = datetime.datetime(x[-1].year, x[-1].month, x[-1].day)
                        if (self.avg_grind != None):
                                while diameter_proj > info.scrap_diameter: #projection based on specific rolls average grind
                                        trend2_y.append(diameter_proj)
                                        trend2_x.append(cur_day)
                                        diameter_proj = diameter_proj - self.avg_grind
                                        cur_day = cur_day + datetime.timedelta(days=self.days_between_grinds)
                                trend2_y.append(info.scrap_diameter)
                                trend2_x.append(cur_day)
                                line1, = plt.plot_date(trend2_x, trend2_y, 'g-')#
                        line2, = plt.plot_date(trend_x,trend_y,'b-')
                        

                markers, = ax.plot_date(x, y, markerfacecolor = 'CornflowerBlue', markeredgecolor = 'Red', zorder=10)
                line3 = plt.axhline(y=other_diameter, color='y', linestyle='-')
                line4 = plt.axhline(y=info.scrap_diameter, color='r', linestyle='-')
                plt.legend([markers, line1, line2, line3, line4], ['Grinds', 'Roll Projection', 'Roll Type Projection', 'One Year Left', 'Scrapped'])
                fig.autofmt_xdate()
                ax.title.set_text(f'Diameter Over Time (All Grinds)')

                plt.xlabel('Date')
                plt.ylabel('Diameter (in.)')
                plt.savefig(f'static/images/Graphs/{self.roll_num} Graph.png', dpi=200)
                return plt
        

        def generate_graphs_2(self, grinds, info, period, projection):
                y = []
                x = []
                dates = []
                data_exists = False
                for grind in grinds:
                        data_exists = True
                        if grind.entry_time > datetime.datetime.today() - period:
                                x.append(grind.entry_time)
                                y.append(grind.min_diameter)


                fig, ax = plt.subplots()
                other_diameter = self.calculate_12mo_diameter(info.scrap_diameter, info.days_between_grinds, info.avg_grind_diameter)

                if len(x) > 0:
                        cur_day = datetime.date(x[-1].year, x[-1].month, x[-1].day)
                        trend_x = []
                        trend_y = []
                        trend2_y = []
                        trend2_x = []
                        diameter_proj = self.diameter

                        while diameter_proj > info.scrap_diameter:#projection based on roll type average grind
                                trend_y.append(diameter_proj)
                                trend_x.append(cur_day)
                                diameter_proj = diameter_proj - info.avg_grind_diameter
                                cur_day = cur_day + datetime.timedelta(days=info.days_between_grinds)
                        trend_y.append(info.scrap_diameter)
                        trend_x.append(cur_day)

                        diameter_proj = self.diameter
                        cur_day = datetime.datetime(x[-1].year, x[-1].month, x[-1].day)
                        line = None
                        if (self.avg_grind != None):
                                while diameter_proj > info.scrap_diameter: #projection based on specific rolls average grind
                                        trend2_y.append(diameter_proj)
                                        trend2_x.append(cur_day)
                                        diameter_proj = diameter_proj - self.avg_grind
                                        cur_day = cur_day + datetime.timedelta(days=self.days_between_grinds)
                                trend2_y.append(info.scrap_diameter)
                                trend2_x.append(cur_day)
                                line1, = plt.plot_date(trend2_x, trend2_y, 'g-')#
                        line2, = plt.plot_date(trend_x,trend_y,'b-')

                markers,  = ax.plot_date(x, y, markerfacecolor = 'CornflowerBlue', markeredgecolor = 'Red', zorder=10)
                line3 = plt.axhline(y=other_diameter, color='y', linestyle='-')
                line4 = plt.axhline(y=info.scrap_diameter, color='r', linestyle='-')
        
                if line2:
                        plt.legend([markers, line1, line2, line3, line4], ['Grinds', 'Roll Projection', 'Roll Type Projection', 'One Year Left', 'Scrapped'])
                else:
                        plt.legend([markers, line1, line3, line4], ['Grinds', 'Roll Type Projection', 'One Year Left', 'Scrapped'])

                fig.autofmt_xdate()
                days = period.days
                months = int(days/30)
                ax.title.set_text(f'Diameter Over Last {months} Months')

                plt.xlabel('Date')
                plt.ylabel('Diameter (in.)')
                if period == datetime.timedelta(weeks=13):
                        plt.savefig(f'static/images/Graphs/{self.roll_num} Graph2.png', dpi=200)
                elif period == datetime.timedelta(weeks=26):
                        plt.savefig(f'static/images/Graphs/{self.roll_num} Graph3.png', dpi=200)
                else:
                        plt.savefig(f'static/images/Graphs/{self.roll_num} Graph4.png', dpi=200)
                return plt
        
        def calculate_12mo_diameter(self, scrap_diameter, days_between, avg_grind):
                if days_between > 180 and days_between < 250:
                        return scrap_diameter + (avg_grind * 2)
                else:
                        thing = math.ceil(365 / days_between)
                        return scrap_diameter + (avg_grind * thing)
       
        def avg_grind_stats(self, period):
                #grinds = Grind.query.filter(Grind.entry_time.between(datetime.datetime.today(), (datetime.datetime.today() - period))).filter_by(roll_num=self.roll_num).all()
                
                # print(str(grind_query))
                all_grinds = db.session.query(Grind).filter_by(roll_num=self.roll_num).all()
                grinds = []
                for grind in all_grinds:
                        if (grind.entry_time >= datetime.datetime.today() - period):
                                grinds.append(grind)
                        
                #print(len(grinds))
                info = db.session.query(Info).filter_by(mill=self.mill, roll_type=self.roll_type)
                num_grinds = 0
                avg_grind = None
                total_min_diameter_lost = 0
                HS_lost = 0
                MD_lost = 0
                TS_lost = 0
                grind_data = []
                for grind in grinds:
                        if num_grinds == 0:
                                avg_grind = float(grind.min_diameter_change)
                                
                        else:
                                avg_grind = float(((avg_grind * num_grinds) + grind.min_diameter_change) / (num_grinds + 1))
                        
                        total_min_diameter_lost += grind.min_diameter_change

                        HS_lost += (grind.HS_before - grind.HS_after)
                        MD_lost += (grind.MD_before - grind.MD_after)
                        TS_lost += (grind.TS_before - grind.TS_after)
                        #print(avg_grind)
                        num_grinds += 1
                
                days_between_grinds = None
                if num_grinds != 0:
                        days_between_grinds = period / num_grinds
                
                
                grind_data.append(avg_grind)
                grind_data.append(total_min_diameter_lost)
                grind_data.append(HS_lost)
                grind_data.append(MD_lost)
                grind_data.append(TS_lost)
                grind_data.append(days_between_grinds)
                grind_data.append(num_grinds)

                #print(grind_data)

                return grind_data
                
                        

                



class Grind(db.Model):
        __tablename__ = 'Grinds'
        roll_num = db.Column(db.Integer, primary_key=True)
        entry_time = db.Column(db.DateTime, primary_key=True)
        HS_before = db.Column(db.Float, nullable=False)
        MD_before = db.Column(db.Float, nullable=False)
        TS_before = db.Column(db.Float, nullable=False)
        HS_after = db.Column(db.Float, nullable=False)
        MD_after = db.Column(db.Float, nullable=False)
        TS_after = db.Column(db.Float, nullable=False)
        min_diameter_change = db.Column(db.Float, nullable=False)
        max_deviation = db.Column(db.Float, nullable=False)
        min_deviation = db.Column(db.Float, nullable=False)
        roll_length = db.Column(db.Float, nullable=False)
        crowning_length = db.Column(db.Float, nullable=False)
        crowning_angle = db.Column(db.Float, nullable=False)
        crowning_bevel = db.Column(db.Float, nullable=False)
        min_diameter = db.Column(db.Float, nullable=False)
        operator = db.Column(db.String, nullable=False)
        program_no = db.Column(db.String, nullable=False)
        shape_no = db.Column(db.String, nullable=False)
        target_diameter = db.Column(db.Float, nullable=False)
        TS_Hardness = db.Column(db.Float, nullable=True)
        MD_Hardness = db.Column(db.Float, nullable=True)
        HS_Hardness = db.Column(db.Float, nullable=True)
        TS_Roughness = db.Column(db.Float, nullable=True)
        MD_Roughness = db.Column(db.Float, nullable=True)
        HS_Roughness = db.Column(db.Float, nullable=True)
        formTolerance = db.Column(db.Float, nullable=False)



class Employee(db.Model):
        __tablename__= 'employee'
        badge_number = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String, nullable=False)
        email = db.Column(db.String, nullable=False)


class Info(db.Model):
    __tablename__ = 'roll_info'
    mill = db.Column(db.String, primary_key=True)
    roll_type = db.Column(db.String, primary_key=True)
    scrap_diameter = db.Column(db.Float, nullable=False)
    avg_grind_diameter = db.Column(db.Float, nullable=False)
    days_between_grinds = db.Column(db.Float, nullable=False)
    num_grinds = db.Column(db.Integer, nullable=False)


class Report(db.Model):
        __tablename__ = 'report'
        date = db.Column(db.String, nullable=False)
        chock_number = db.Column(db.String, nullable=False)
        position = db.Column(db.String, nullable=False)
        reason = db.Column(db.String, nullable=False)
        visible_chock_numbers = db.Column(db.String, nullable=False)
        lifting_bolt_thread_condition = db.Column(db.String, nullable=False)
        cover_end_condition = db.Column(db.String, nullable=False)
        bell_o_ring_condition = db.Column(db.String, nullable=False)
        thrust_collar   = db.Column(db.String, nullable=False)
        lockkeepers = db.Column(db.String, nullable=False)
        liner_plates = db.Column(db.String, nullable=False)
        inboard_radial_seals_replaced = db.Column(db.String, nullable=False)
        inboard_face_seal = db.Column(db.String, nullable=False)
        outboard_radial_seal = db.Column(db.String, nullable=False)
        load_zone_from_mill = db.Column(db.String, nullable=False)
        load_zone_to_mill = db.Column(db.String, nullable=False)
        bearing_grease_condition = db.Column(db.String, nullable=False)
        bearing_mfg = db.Column(db.String, nullable=False)
        bearing_serial_number = db.Column(db.String, nullable=False)
        is_sealed = db.Column(db.String, nullable=False)
        seals_replaced = db.Column(db.String, nullable=False)
        cup_a = db.Column(db.String, nullable=False)
        cup_bd = db.Column(db.String, nullable=False)
        cup_e = db.Column(db.String, nullable=False)
        race_a = db.Column(db.String, nullable=False)
        race_b = db.Column(db.String, nullable=False)
        race_d = db.Column(db.String, nullable=False)
        race_e = db.Column(db.String, nullable=False)
        bearing_status = db.Column(db.String, nullable=False)
        different_bearing_installed = db.Column(db.String, nullable=False)
        bearing_mfg_new = db.Column(db.String, nullable=False)
        serial_number_new = db.Column(db.String, nullable=False)
        sealed_new = db.Column(db.String, nullable=False)
        chock_bore_round = db.Column(db.String, nullable=False)
        chock_bore = db.Column(db.String, nullable=False)
        no_rust = db.Column(db.String, nullable=False)
        grease_purged = db.Column(db.String, nullable=False)
        spots_dings = db.Column(db.String, nullable=False)
        manual_pack = db.Column(db.String, nullable=False)
        lube_bore = db.Column(db.String, nullable=False)
        grease_packed_bearings = db.Column(db.String, nullable=False)
        height_shoulder = db.Column(db.String, nullable=False)
        bearing_depth = db.Column(db.String, nullable=False)
        shims_needed = db.Column(db.String, nullable=False)
        was_paper_used = db.Column(db.String, nullable=False)
        by_hand = db.Column(db.String, nullable=False)
        was_torqued = db.Column(db.String, nullable=False)
        ancillary_installed = db.Column(db.String, nullable=False)
        grease_pack_sealed = db.Column(db.String, nullable=False)
        chock_ready_for_installation = db.Column(db.String, nullable=False)
        comments = db.Column(db.String, nullable=False)
        mill = db.Column(db.String, nullable=False)
        badge_number = db.Column(db.String, nullable=False)
        roll_type = db.Column(db.String, nullable=False)
        ID = db.Column(db.Integer, nullable=False, primary_key=True)

        def __init__(self, data, **kwargs):
                super(Report, self).__init__(**kwargs)
                self.date = data[0]
                self.chock_number = data[1]
                self.position = data[2]
                self.reason = data[3]
                self.visible_chock_numbers = data[4]
                self.lifting_bolt_thread_condition = data[5]
                self.cover_end_condition = data[6]
                self.bell_o_ring_condition = data[7]
                self.thrust_collar = data[8]
                self.lockkeepers = data[9]
                self.liner_plates = data[10]
                self.inboard_radial_seals_replaced = data[11]
                self.inboard_face_seal = data[12]
                self.outboard_radial_seal = data[13]
                self.load_zone_from_mill = data[14]
                self.load_zone_to_mill = data[15]
                self.bearing_grease_condition = data[16]
                self.bearing_mfg = data[17]
                self.bearing_serial_number = data[18]
                self.is_sealed = data[19]
                self.seals_replaced = data[20]
                self.cup_a = data[21]
                self.cup_bd = data[22]
                self.cup_e = data[23]
                self.race_a = data[24]
                self.race_b = data[25]
                self.race_d = data[26]
                self.race_e = data[27]
                self.bearing_status = data[28] 
                self.different_bearing_installed = data[29]
                self.bearing_mfg_new = data[30]
                self.serial_number_new = data[31]
                self.sealed_new = data[32]
                self.chock_bore_round = data[33]
                self.chock_bore = data[34]
                self.no_rust = data[35]
                self.grease_purged = data[36]
                self.spots_dings = data[37]
                self.manual_pack = data[38]
                self.lube_bore = data[39]
                self.grease_packed_bearings = data[40]
                self.height_shoulder = data[41]
                self.bearing_depth = data[42]
                self.shims_needed = data[43]
                self.was_paper_used = data[44]
                self.by_hand = data[45]
                self.was_torqued = data[46]
                self.ancillary_installed = data[47]
                self.grease_pack_sealed = data[48]
                self.chock_ready_for_installation = data[49]
                self.comments = data[50]
                self.mill = data[51]
                self.badge_number = data[52]
                self.roll_type = data[53]
        
        def edit(self, data):
                self.date = data[0]
                self.chock_number = data[1]
                self.position = data[2]
                self.reason = data[3]
                self.visible_chock_numbers = data[4]
                self.lifting_bolt_thread_condition = data[5]
                self.cover_end_condition = data[6]
                self.bell_o_ring_condition = data[7]
                self.thrust_collar = data[8]
                self.lockkeepers = data[9]
                self.liner_plates = data[10]
                self.inboard_radial_seals_replaced = data[11]
                self.inboard_face_seal = data[12]
                self.outboard_radial_seal = data[13]
                self.load_zone_from_mill = data[14]
                self.load_zone_to_mill = data[15]
                self.bearing_grease_condition = data[16]
                self.bearing_mfg = data[17]
                self.bearing_serial_number = data[18]
                self.is_sealed = data[19]
                self.seals_replaced = data[20]
                self.cup_a = data[21]
                self.cup_bd = data[22]
                self.cup_e = data[23]
                self.race_a = data[24]
                self.race_b = data[25]
                self.race_d = data[26]
                self.race_e = data[27]
                self.bearing_status = data[28] 
                self.different_bearing_installed = data[29]
                self.bearing_mfg_new = data[30]
                self.serial_number_new = data[31]
                self.sealed_new = data[32]
                self.chock_bore_round = data[33]
                self.chock_bore = data[34]
                self.no_rust = data[35]
                self.grease_purged = data[36]
                self.spots_dings = data[37]
                self.manual_pack = data[38]
                self.lube_bore = data[39]
                self.grease_packed_bearings = data[40]
                self.height_shoulder = data[41]
                self.bearing_depth = data[42]
                self.shims_needed = data[43]
                self.was_paper_used = data[44]
                self.by_hand = data[45]
                self.was_torqued = data[46]
                self.ancillary_installed = data[47]
                self.grease_pack_sealed = data[48]
                self.chock_ready_for_installation = data[49]
                self.comments = data[50]
                self.mill = data[51]
                self.badge_number = data[52]
                self.roll_type = data[53]

                db.session.commit()
