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
from AU_RPGSystem import AU_RPGLanguages
import AU_Langs


def at_initial_setup():
    # Setup the idioms of the game
    AU_RPGLanguages.add_language(key='English',
                                 phonemes=AU_Langs.english_phonemes,
                                 grammar=AU_Langs.english_grammar,
                                 word_length_variance=AU_Langs.english_word_length_variance,
                                 noun_postfix=AU_Langs.english_noun_postfix,
                                 vowels=AU_Langs.english_vowels,
                                 manual_translations=AU_Langs.english_manual_translations,
                                 auto_translation=AU_Langs.english_words_list)

    # Create the main character generation room
    chargen_room = create.create_object(typeclass='CoC.CoC_Rooms.CoCCharGenRoom', key='Investigator Room')
    chargen_room.db.desc = dedent('Here you con create your investigator.')
    chargen_room.tags.add('default_chargen', category='rooms')

    pass
