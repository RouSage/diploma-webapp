from flask_babel import lazy_gettext as _l

DATA = {"CLASSES": [_l('aeroplane'), _l('bicycle'), _l('bird'), _l('boat'), _l('bottle'), _l('bus'),
                    _l('car'), _l('cat'), _l('chair'), _l('cow'), _l(
                        'diningtable'), _l('dog'), _l('horse'),
                    _l('motorbike'), _l('person'), _l(
                        'pottedplant'), _l('sheep'), _l('sofa'),
                    _l('train'), _l('tvmonitor')],
        "NUM": 20}

# model
MODEL = {"ANCHORS": [[(1.25, 1.625), (2.0, 3.75), (4.125, 2.875)],  # Anchors for small obj
                     # Anchors for medium obj
                     [(1.875, 3.8125), (3.875, 2.8125), (3.6875, 7.4375)],
                     [(3.625, 2.8125), (4.875, 6.1875), (11.65625, 10.1875)]],  # Anchors for big obj
         "STRIDES": [8, 16, 32],
         "ANCHORS_PER_SCLAE": 3
         }

# test
TEST = {
    "TEST_IMG_SIZE": 544,
    "BATCH_SIZE": 1,
    "NUMBER_WORKERS": 0,
    "CONF_THRESH": 0.01,
    "NMS_THRESH": 0.5,
    "MULTI_SCALE_TEST": False,
    "FLIP_TEST": False
}
