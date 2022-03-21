"""

"""

from evennia import utils

# English definition
english_key = 'english'
english_phonemes = (
    "ea oh ae aa eh ah ao aw ai er ey ow ia ih iy oy ua uh uw a e i u y p b t d f v t dh "
    "s z sh zh ch jh k ng g m n l r w"
)
english_grammar = "v cv vc cvv vcc vcv cvcc vccv cvccv cvcvcc cvccvcv vccvccvc cvcvccvv cvcvcvcvv"
english_word_length_variance = 0
english_noun_translate = False
english_noun_prefix = ""
english_noun_postfix = ""
english_vowels = "aeiouy"
english_manual_translations = None
english_auto_translations = utils.get_game_dir_path() + '/AU_Langs/AU_Words.txt'
english_force = False
