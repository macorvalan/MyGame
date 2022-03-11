"""
At_initial_setup module template

Custom at_initial_setup method. This allows you to hook special
modifications to the initial server startup process. Note that this
will only be run once - when the server starts up for the very first
time! It is called last in the startup process and can thus be used to
overload things that happened before it.

The module must contain a global function at_initial_setup().  This
will be called without arguments. Note that tracebacks in this module
will be QUIETLY ignored, so make sure to check it well to make sure it
does what you expect it to.

"""
from evennia.utils import search, dedent, create


def at_initial_setup():
    chargen_room = create.create_object(typeclass='CoC.CoC_Rooms.CoCCharGenRoom', key='Investigator Room')
    chargen_room.db.desc = dedent('Here you con create your investigator.')
    chargen_room.tags.add('default_chargen', category='rooms')

    pass
