"""
All pc/npc from the Call of Cthulhu 7th version - 1920

"""
from AU_Modules.AU_RPGSystem.AU_RPGCommunications import AURPGRPCharacter


class CoCCharacter(AURPGRPCharacter):
    """
    Main character, investigator, used by the player
    """

    def at_object_creation(self):
        super(CoCCharacter, self).at_object_creation()

        # Main characteristics
        self.db._STR = 0  # Strength - (3D6 * 5) - INTEGER
        self.db._CON = 0  # Constitution - (3D6 * 5) - INTEGER
        self.db._INT = 0  # Intelligence - ((2D6 + 6) * 5) - INTEGER
        self.db._SIZ = 0  # Size - ((2D6 + 6) * 5) - INTEGER
        self.db._DEX = 0  # Dexterity - (3D6 *5) - INTEGER
        self.db._APP = 0  # Appearance - (3D6 * 5) - INTEGER
        self.db._POW = 0  # Power - (3D6 * 5) - INTEGER
        self.db._EDU = 0  # Education - ((2D6 +6) * 5) - INTEGER

        # Derived characteristics
        self.db._idea = 0  # Idea - INT - INTEGER
        self.db._luck = 0  # Luck - (3D6 * 5) - INTEGER
        self.db._know = 0  # Know - EDU - INTEGER

        # Personal characteristics
        self.db._race = 0  # Race - from table - INTEGER
        self.db._name = ""  # Fantasy name - max len 30 chars - STRING
        self.db._sex = 0  # Sex - from Table (F:0/M:1/H:2) - INTEGER
        self.db._age = 0  # Age - min/max set by race- INTEGER
        self.db._gender = 0  # Gender - from table - INTEGER

        self.db._birthplace = ""  # Birthplace - max len 30 chars - STRING
        self.db._residence = ""  # Current residence - max 30 chars - STRING
        self.db._occupation = 0  # Occupation - from table . INTEGER
        self.db._sexOrientation = 0  # Sex orientation - from table - INTEGER

        # Body and Mind characteristics
        self.db._damageBonus = ""  # Damage bonus - from table, formula to parser - STRING
        self.db._build = 0  # Build - from table - INTEGER
        self.db._hitPoints = 0  # Hit points - ceil((CON + SIZ) / 10) - INTEGER
        self.db._magicPoints = 0  # Magic Points - ceil(POW / 5) - INTEGER
        self.db._movementRate = 0  # Movement rate - (STR + DEX) from table mod. by age - INTEGER
        self.db._sanity = 0  # Sanity - POW - INTEGER

        # Status FLAGS
        pass
