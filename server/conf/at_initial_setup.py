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

from evennia.utils import create, search

from AU_Modules.AU_RPGSystem import AU_RPGLanguages
from AU_Modules.AU_Langs import AU_Languages


def at_initial_setup():
    # Definition of the english language
    AU_RPGLanguages.add_language(key=AU_Languages.english_key,
                                 phonemes=AU_Languages.english_phonemes,
                                 grammar=AU_Languages.english_grammar,
                                 word_length_variance=AU_Languages.english_word_length_variance,
                                 noun_translate=AU_Languages.english_noun_translate,
                                 noun_prefix=AU_Languages.english_noun_prefix,
                                 noun_postfix=AU_Languages.english_noun_postfix,
                                 vowels=AU_Languages.english_vowels,
                                 manual_translations=AU_Languages.english_manual_translations,
                                 auto_translations=AU_Languages.english_auto_translations,
                                 force=AU_Languages.english_force)

    # Definition of all languages used in the mud.
    # TODO: add the languages

    # Creation of the initial CharGen Room and its objects
    # Room creation
    # TODO: create chargen room

    # objects Creation
    # TODO: Create object in room


    # Create the main character generation room
    chargen_room = create.create_object(typeclass='CoC.CoC_Rooms.CoCCharGenRoom', key='Investigator Room')
    chargen_room.db.desc = 'Here you con create your investigator.'
    chargen_room.tags.add('default_chargen', category='rooms')
    chargen_room.save()
    limboroom=search.object_search('Limbo')[0]
    silla = create.create_object(typeclass='CoC.CoC_Objects.CoCObject', key='silla', location=limboroom)
    silla.save()
    pass


"""
    # Create the main character generation room
    #chargen_room = create.create_object(typeclass='CoC.CoC_Rooms.CoCCharGenRoom', key='Investigator Room')
    #chargen_room.db.desc = dedent('Here you con create your investigator.')
    #chargen_room.tags.add('default_chargen', category='rooms')
"""
