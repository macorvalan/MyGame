"""
A login menu using EvMenu.

Original Contribution - Vincent-lg 2016, Griatch 2019 (rework for modern EvMenu)
Modified by MaCorvalan, 2022
    * Add email input
    * Miscellaneous changes

This changes the Evennia login to ask for the account name and password in
sequence instead of requiring you to enter both at once.

To install, add this line to the settings file (`mygame/server/conf/settings.py`):

    CMDSET_UNLOGGEDIN = "AU_Modules.AU_Menu:Logging.AU_MenuLogging.UnloggedinCmdSet"

Reload the server and the new connection method will be active. Note that you must
independently change the connection screen to match this login style, by editing
`mygame/server/conf/connection_screens.py`.

This uses Evennia's menu system EvMenu and is triggered by a command that is
called automatically when a new user connects.

"""

from django.conf import settings

import re
from evennia import Command, CmdSet
from evennia import syscmdkeys
from evennia.utils.evmenu import EvMenu
from evennia.utils.utils import random_string_from_module, class_from_module, callables_from_module

# Variables ------------------------------------------------------------------------------------------------------------

_CONNECTION_SCREEN_MODULE = settings.CONNECTION_SCREEN_MODULE
_GUEST_ENABLED = settings.GUEST_ENABLED
_ACCOUNT = class_from_module(settings.BASE_ACCOUNT_TYPECLASS)
_GUEST = class_from_module(settings.BASE_GUEST_TYPECLASS)

# Help messages --------------------------------------------------------------------------------------------------------

_ACCOUNT_HELP = (
    "                                                                                  |G**********************************************************"
    "                                                                                  |G* |nIf you are a |yNEW|n user, type the desire |yACCOUNT|n name    |G*|n"
    "                                                                                  |G* |nThe |yNAME|n of the account should preferable              |G*|n"
    "                                                                                  |G* |nonly be letters |y(A-Z)|n and numbers |y(0-9)|n,               |G*|n"
    "                                                                                  |G* |nit should |rnot|n contain special characters or spaces.    |G*|n"
    "                                                                                  |G**********************************************************|n"
)
_EMAIL_HELP = (
    "                                                                                  |G**********************************************************"
    "                                                                                  |G* |nThis will be used for password recovery, and must be   |G*|n"
    "                                                                                  |G* |na valid |yEMAIL|n addres.                                  |G*|n"
    "                                                                                  |G**********************************************************|n"
)

_PASSWORD_HELP = (
    "                                                                                  |G**********************************************************"
    "                                                                                  |G* |yPASSWORD|n should be a minimum of |y8|n characters and can   |G*|n"
    "                                                                                  |G* |ncontain a mix of |yletters|n, |ydigits|n and                   |G*|n"
    "                                                                                  |G* |y@/./+/-/_/'/|n, |ronly|n.                                    |G*|n"
    "                                                                                  |G**********************************************************|n"
)

# Login messages -------------------------------------------------------------------------------------------------------

_ACCOUNT_LOGGING = "Enter a new or existing |yACCOUNT|n name to login:"

_EMAIL_LOGGING = "Enter a valid |yEMAIL|n address (empty to abort):"

_SHOW_CS = True


# Menu nodes

def _show_help(caller, raw_string, **kwargs):
    """
    Echo help message, then re-run node that triggered it
    """
    help_entry = kwargs["help_entry"]
    caller.msg(help_entry)

    # re-run calling node
    return None


def node_enter_accountname(caller, raw_text, **kwargs):
    """
    NODO 01
    Start node of menu
    Start login by displaying the connection screen and ask for am account name.
    """

    def _check_input(caller, accountname, **kwargs):
        """
        'Goto-callable', set up to be called from the _default option below.

        Called when user enters a username string. Check if this username already exists and set the flag
        'new_user' if not. Will also directly login if the username is 'guest'
        and GUEST_ENABLED is True.

        The return from this goto-callable determines which node we go to next
        and what kwarg it will be called with.
        """
        accountname = accountname.rstrip("\n").lower()

        if accountname == "guest":
            session = caller
            session.msg("|R{}|n".format("Invalid ACCOUNT name, reservesd word 'guest'."))

            return None  # re-run the username node
        elif ' ' in accountname:
            session = caller
            session.msg("|R{}|n".format("Invalid ACCOUNT name, name contain spaces."))

            return None  # re-run the username node
        elif not accountname.isalnum():
            session = caller
            session.msg("|R{}|n".format("Invalid ACCOUNT name, contain special characters."))

            return None  # re-run the username node
        else:
            # All OK
            pass

        try:
            _ACCOUNT.objects.get(username__iexact=accountname)
        except _ACCOUNT.DoesNotExist:
            new_account = True
            next_node = "node_enter_email"
            email = ""
        else:
            new_account = False
            next_node = "node_enter_password"
            email = ""

        # pass username/new_user into next node as kwargs
        return next_node, {"new_account": new_account, "accountname": accountname, "email": email}

    def _restart_login(caller, *args, **kwargs):
        global _SHOW_CS
        _SHOW_CS = True
        caller.msg("|yCancelled login.|n")
        return "node_enter_accountname"

    callables = callables_from_module(_CONNECTION_SCREEN_MODULE)
    if "connection_screen" in callables:
        connection_screen = callables["connection_screen"]()
    else:
        connection_screen = random_string_from_module(_CONNECTION_SCREEN_MODULE)

    global _SHOW_CS
    if _SHOW_CS:
        m_text = "{}\n\n{}".format(connection_screen, _ACCOUNT_LOGGING)
        _SHOW_CS = False
    else:
        m_text = "\n\n{}".format(_ACCOUNT_LOGGING)

    m_options = (
        {"key": "", "goto": _restart_login},
        {"key": ("quit", "q"), "goto": "node_quit_or_login"},
        {"key": ("help", "h"), "goto": (_show_help, {"help_entry": _ACCOUNT_HELP, **kwargs})},
        {"key": "_default", "goto": _check_input},
    )
    return m_text, m_options


def node_enter_email(caller, raw_text, **kwargs):
    """
    Node 02
    Handle the input of email.
    """

    def _check_input(caller, e_mail, **kwargs):
        """
        'Goto-callable', set up to be called from the _default option below.

        Called when user enters an email string when the account is created.
        Check email is valid and if it passes, then ask for the password.

        The return from this goto-callable determines which node we go to next
        and what kwarg it will be called with.
        """
        accountname = kwargs["accountname"]
        new_account = kwargs["new_account"]
        e_mail = e_mail.rstrip("\n")
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

        if not re.search(regex, e_mail):
            session = caller
            session.msg("|R{}|n".format("Invalid EMAIL address."))

            return None  # re-run the username node

        next_node = "node_enter_password"

        # pass username/new_user into next node as kwargs
        return next_node, {"new_account": new_account, "accountname": accountname, "email": e_mail}

    def _restart_login(caller, *args, **kwargs):
        global _SHOW_CS
        _SHOW_CS = True
        caller.msg("|yCancelled login.|n")
        return "node_enter_accountname"

    m_text = _EMAIL_LOGGING

    m_options = (
        {"key": "", "goto": _restart_login},
        {"key": ("quit", "q"), "goto": "node_quit_or_login"},
        {"key": ("help", "h"), "goto": (_show_help, {"help_entry": _EMAIL_HELP, **kwargs})},
        {"key": "_default", "goto": (_check_input, kwargs)},
    )
    return m_text, m_options


def node_enter_password(caller, raw_string, **kwargs):
    """
    Handle password input.
    """

    def _check_input(caller, password, **kwargs):
        """
        'Goto-callable', set up to be called from the _default option below.

        Called when user enters a password string. Check username + password
        viability. If it passes, the account will have been created and login
        will be initiated.

        The return from this goto-callable determines which node we go to next
        and what kwarg it will be called with.
        """
        # these flags were set by the goto-callable
        accountname = kwargs["accountname"]
        new_account = kwargs["new_account"]
        email = kwargs["email"]
        password = password.rstrip("\n")

        global _SHOW_CS
        _SHOW_CS = True

        session = caller
        address = session.address
        if new_account:
            # create a new account
            account, errors = _ACCOUNT.create(
                username=accountname, email=email, password=password, ip=address, session=session
            )
        else:
            # check password against existing account
            account, errors = _ACCOUNT.authenticate(
                username=accountname, password=password, ip=address, session=session
            )

        if account:
            if new_account:
                session.msg("|gA new account |g{}|g was created. Welcome!|n".format(accountname))
            # pass login info to login node
            return "node_quit_or_login", {"login": True, "account": account}
        else:
            # restart due to errors
            session.msg("|R{}".format("\n".join(errors)))
            kwargs["retry_password"] = True
            return "node_enter_password", kwargs

    def _restart_login(caller, *args, **kwargs):
        global _SHOW_CS
        _SHOW_CS = True
        caller.msg("|yCancelled login.|n")
        return "node_enter_accountname"

    accountname = kwargs["accountname"]
    if kwargs["new_account"]:

        if kwargs.get("retry_password"):
            # Attempting to fix password
            text = "Enter a new password:"
        else:
            text = "Creating a new account |g{}|n. Enter a password (empty to abort):".format(accountname)
    else:
        text = "Enter the password for account |g{}|n (empty to abort):".format(accountname)

    options = (
        {"key": "", "goto": _restart_login},
        {"key": ("quit", "q"), "goto": "node_quit_or_login"},
        {"key": ("help", "h"), "goto": (_show_help, {"help_entry": _PASSWORD_HELP, **kwargs})},
        {"key": "_default", "goto": (_check_input, kwargs)},
    )
    return text, options


def node_quit_or_login(caller, raw_text, **kwargs):
    """
    Exit menu, either by disconnecting or logging in.
    """
    global _SHOW_CS
    session = caller
    if kwargs.get("login"):
        account = kwargs.get("account")
        session.msg("|gLogging in ...|n")
        session.sessionhandler.login(session, account)
    else:
        session.sessionhandler.disconnect(session, "Goodbye! Logging off.")
        _SHOW_CS = True

    return "", {}


# EvMenu helper function

def _node_formatter(nodetext, optionstext, caller=None):
    """
    Do not display the options, only the text.

    This function is used by EvMenu to format the text of nodes. The menu login
    is just a series of prompts so we disable all automatic display decoration
    and let the nodes handle everything on their own.
    """
    return nodetext


# Commands and CmdSets

class UnloggedinCmdSet(CmdSet):
    """
    Cmdset for the unloggedin state.
    """
    key = "DefaultUnloggedin"
    priority = 0

    def at_cmdset_creation(self):
        """
        Called when cmdset is first created.
        """
        self.add(CmdUnloggedinLook())


class CmdUnloggedinLook(Command):
    """
    An unloggedin version of the look command. This is called by the server
    when the account first connects. It sets up the menu before handing off
    to the menu's own look command.
    """
    key = syscmdkeys.CMD_LOGINSTART
    locks = "cmd:all()"
    arg_regex = r"^$"

    def func(self):
        """
        Run the menu using the nodes in this module.
        """
        EvMenu(
            self.caller,
            "AU_Modules.AU_Menu_Logging.AU_MenuLogging",
            startnode="node_enter_accountname",
            auto_look=False,
            auto_quit=False,
            cmd_on_exit=None,
            node_formatter=_node_formatter,
        )
