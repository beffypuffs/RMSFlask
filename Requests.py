def email_request_data(request):
    badge_number = request.form['badge_number']
    name = request.form['nm']
    email = request.form['email']
    data = [badge_number, name, email]
    return data

def chock_request_data(request):
    date = request.form['date']
    chock_number = request.form['chock-num']
    position = request.form['position']
    reason = request.form['reasons_d_and_i']
    try:
        visible_chock_numbers = request.form['obvi']
    except:
        visible_chock_numbers = 'FALSE'
    try:
        lifting_bolt_thread_condition = request.form['lifting']
    except:
        lifting_bolt_thread_condition = 'FALSE'
    try:
        cover_end_condition = request.form['cover']
    except:
        cover_end_condition = 'FALSE'
    try:
        bell_o_ring_condition = request.form['end-bell']
    except:
        bell_o_ring_condition = 'FALSE'
    try:
        thrust_collar = request.form['thrust']
    except:
        thrust_collar = 'FALSE'
    try:
        lockkeepers = request.form['locks']
    except:
        lockkeepers = 'FALSE'
    try:
        liner_plates = request.form['liner']
    except:
        liner_plates = 'FALSE'
    try:
        inboard_radial_seals_replaced = request.form['num-rep']
    except:
        inboard_radial_seals_replaced = 'FALSE'

    inboard_face_seal = request.form['seals1']
    # outboard_radial_seal = request.form['seals2'],
    outboard_radial_seal = 'NOT REAL'
    load_zone_from_mill = request.form['mill1']
    # load_zone_to_mill = request.form['mill2'],
    load_zone_to_mill = 'NOT IN FORM'
    bearing_grease_condition = request.form['bearing-grease']
    bearing_mfg = request.form['mfg']
    bearing_serial_number = request.form['sn']
    try:
        is_sealed = request.form['sealed']
    except:
        is_sealed = 'FALSE'
    seals_replaced = request.form['seals-rep']
    cup_a = request.form['cupA']
    cup_bd = request.form['cupB']
    cup_e = request.form['cupE']
    race_a = request.form['raceA']
    race_b = request.form['raceB']
    race_d = request.form['raceD']
    race_e = request.form['raceE']
    bearing_status = request.form['bearing-condition']
    try:
        different_bearing_installed = request.form['diff-bearing']
    except:
        different_bearing_installed = 'FALSE'
    bearing_mfg_new = request.form['textMFG']
    serial_number_new = request.form['MFGsn']
    try:
        sealed_new = request.form['sealed2']
    except:
        sealed_new = 'FALSE'
    try:
        chock_bore_round = request.form['chockBoreRound']
    except:
        chock_bore_round = 'FALSE'
    try:
        chock_bore = request.form['chockBoreOOR']
    except:
        chock_bore = 'FALSE'
    try:
        no_rust = request.form['wearOrRust']
    except:
        no_rust = 'FALSE'
    try:
        grease_purged = request.form['purgeGrease']
    except:
        grease_purged = 'FALSE'
    try:
        spots_dings = request.form['spots-dings']
    except:
        spots_dings = 'FALSE'
    try:
        manual_pack = request.form['manual-pack']
    except:
        manual_pack = 'FALSE'
    try:
        lube_bore = request.form['lube-bore']
    except:
        lube_bore = 'FALSE'

    try: 
        grease_packed_bearings = request.form['dropped']
    except:
        grease_packed_bearings = 'FALSE'
    height_shoulder = request.form['droppedA']
    bearing_depth = request.form['droppedB']
    shims_needed = request.form['droppedDifference']
    try:
        was_paper_used = request.form['paper-used']
    except: 
        was_paper_used = 'FALSE'
    try:
        by_hand = request.form['shim']
    except:
        by_hand = 'FALSE'
    try:
        was_torqued = request.form['phases']
    except:
        was_torqued = 'FALSE'
    try:
        ancillary_installed = request.form['ancillary']
    except:
        ancillary_installed = 'FALSE'
    try:
        grease_pack_sealed = request.form['greasePack']
    except:
        grease_pack_sealed = 'FALSE'
    try:
        chock_ready_for_installation = request.form['ready']
    except:
        chock_ready_for_installation = 'FALSE'

    comments  = request.form['comments']
    mill = request.form['roll_mill']
    badge_number = request.form['badge_number']
    roll_type = request.form['roll_type']
    data = [date,
        chock_number, position, reason, visible_chock_numbers, lifting_bolt_thread_condition, cover_end_condition, bell_o_ring_condition, thrust_collar, lockkeepers, liner_plates, inboard_radial_seals_replaced,inboard_face_seal, outboard_radial_seal, load_zone_from_mill, load_zone_to_mill, bearing_grease_condition, bearing_mfg,
        bearing_serial_number,
        is_sealed, seals_replaced, cup_a, cup_bd, cup_e, race_a, race_b, race_d, race_e, bearing_status, different_bearing_installed, bearing_mfg_new, serial_number_new, sealed_new, chock_bore_round, chock_bore, no_rust,
        grease_purged, spots_dings, manual_pack, lube_bore, grease_packed_bearings, height_shoulder, bearing_depth, shims_needed, was_paper_used, by_hand, was_torqued, ancillary_installed, grease_pack_sealed,
        chock_ready_for_installation, comments, mill, badge_number, roll_type]
    return data