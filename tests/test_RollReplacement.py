"""
Testing file for RMS Roll Lifespan Prediction
ONLY WORKS ON KAISER NETWORK (as of 11/17/2021)
Written By - Joshua Seward
"""
import RollReplacement as r

# test the predictive function using the values in the Kaiser rms database
# associated with the roll id '1001'
def test_remaining_roll_life():
    cur_diameter = 54.5
    scrap_diameter = 51.5
    avg_grind_diameter = 0.093
    days_btwn_rolls = 186
    remaining_roll_life = r.remaining_roll_life(cur_diameter, scrap_diameter,
        avg_grind_diameter, days_btwn_rolls)
    assert remaining_roll_life == 6000

# test that the values are properly taken from the database and used in the
# predictive function
def test_days_until_replacement():
    remaining_roll_life = r.days_until_replacement(1001)
    assert remaining_roll_life == 6000