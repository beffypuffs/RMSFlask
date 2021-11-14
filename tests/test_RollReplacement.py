"""
Testing file for RMS Roll Lifespan Prediction
(Has to be run on the Kaiser network)
Written By - Joshua Seward
"""
import RollReplacement as r

# test the predictive function using a roll id of 1001
def test_days_until_replacement():
    remaining_roll_life = r.days_until_replacement(1001)
    assert remaining_roll_life == 0