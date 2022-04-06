"""
Call of Cthulhu dictionary with materials properties.

Properties:
            [00] Flammability           FL      bool (True or False)        True
            [01] Conductivity           CD      float (0 - +2)              0
            [02] Soundproofing          SP      float (0 - +2)              0
            [03] Magnetic               MG      float (0 - +2)              0
            [04] Radioactive            RD      float (0 - +2)              0
            [05] Luminosity             LU      float (0 - +2)              0
            [06] Photosensitivity       PS      float (0 - +2)              0
            [07] Toughness              TH      float (-3 - +3)             0
            [08] Freezing Point         FP      float (-inf - +inf)         0
            [09] Melting Point          MP      float (-inf - +inf)         0
            [10] Evaporation Point      EP      float (-inf - +inf)         0
            [11] Condensation Point     CP      float (-inf - +inf)         0
            [12] Deposition Point       DP      float (-inf - +inf)         0
            [13] Sublimation Point      SP      float (-inf - +inf)         0
            [14] Vaporization Point     VP      float (-inf - +inf)         0
            [15] Ionization Point       IP      float (-inf - +inf)         0
            [16] Fire Resistance        FR      float (-5 - +3)             0
            [17] Cold Resistance        CR      float (-5 - +3)             0
            [18] Water Resistance       WR      float (-5 - +3)             0
            [19] Shock Resistance       SR      float (-5 - +3)             0
            [20] Acid Resistance        AR      float (-5 - +3)             0
            [21] Plasma Resistance      PR      float (-5 - +3)             0
            [22] Explosive Resistance   ER      float (-5 - +3)             0
            [23] Kinect Resistance      KR      float (-5 - +3)             0
            [24] Color                  CL      string                      white
            [25] Reflectivity           RF      float (0 - +1)              0
            [26] Transparency           TR      float (0 - +1)              0


Materials:
            * wood
            * cloth
            * vegetable hair
            * iron

"""

PROPERTIES_DICT = {'Flammable': ['FL', True],
                   'Conductivity': ['CD', 0.0],
                   'Soundproofing': ['SP', 0.0],
                   'Magnetic': ['MG', 0.0],
                   'Radioactive': ['RD', 0.0],
                   'Luminosity': ['LU', 0.0],
                   'Photosensitivity': ['PS', 0.0],
                   'Toughness': ['TH', 0.0],
                   'Freezing Point': ['FP', 0.0],
                   'Melting Point': ['MP', 0.0],
                   'Evaporation Point': ['EP', 0.0],
                   'Condensation Point': ['CP', 0.0],
                   'Deposition Point': ['DP', 0.0],
                   'Sublimation Point': ['SP', 0.0],
                   'Vaporization Point': ['VP', 0.0],
                   'Ionization Point': ['IP', 0.0],
                   'Fire Resistance': ['FR', 0.0],
                   'Cold Resistance': ['CR', 0.0],
                   'Water Resistance': ['WR', 0.0],
                   'Shock Resistance': ['SR', 0.0],
                   'Acid Resistance': ['AR', 0.0],
                   'Plasma Resistance': ['PR', 0.0],
                   'Explosive Resistance': ['ER', 0.0],
                   'Kinect Resistance': ['KR', 0.0],
                   'Color': ['CL', 'white'],
                   'Reflectivity': ['RF', 0.0],
                   'Transparency': ['TR', 0.0],
                   }

MATERIALS_PROPERTIES_DICT = {'wood': ['SP:0.5', 'TH:-1.0', 'FR:2.0', 'CR:0.9', 'WR:1.5', 'SR:-2.5', 'AR:-2.1', 'PR:3.0', 'ER:3.0', 'KR:1.0', 'CR:brown'],
                             'cloth': ['FL:True'],
                             'vegetable hair': ['FL:True'],
                             'iron': ['FL:False'],
                             }
