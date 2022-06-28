import os
import re
import shutil
import subprocess

from buildtest.defaults import console
from buildtest.exceptions import BuildTestError
from buildtest.utils.file import resolve_path


def is_emacs(emacs_editor):
    """Check whether editor is emacs by running ``emacs --version`` and checking regular expression for output. Shown below
    is an expected output. We will check if output contains "GNU Emacs"

    .. code-block:: console

         ~/ emacs --version
        GNU Emacs 28.1
        Copyright (C) 2022 Free Software Foundation, Inc.
        GNU Emacs comes with ABSOLUTELY NO WARRANTY.
        You may redistribute copies of GNU Emacs
        under the terms of the GNU General Public License.
        For more information about these matters, see the file named COPYING.

    Args:
        editor (str): Path to editor

    Returns:
        bool: True if editor is nano otherwise returns False
    """
    cmd = subprocess.run(
        [emacs_editor, "--version"], capture_output=True, universal_newlines=True
    )

    match = re.match("^(GNU Emacs)", cmd.stdout)
    return match


def is_vi(editor):
    """Check whether editor is vi by running ``vi --version`` and checking regular expression for output. Shown below
    is the expected output, we will checkout if output contains "VIM -"

    .. code-block:: console

         ~/ vi --version
        VIM - Vi IMproved 8.2 (2019 Dec 12, compiled May  8 2021 05:44:12)
        macOS version
        Included patches: 1-2029
        Compiled by root@apple.com
        Normal version without GUI.  Features included (+) or not (-):
        +acl               -farsi             +mouse_sgr         +tag_binary
        -arabic            +file_in_path      -mouse_sysmouse    -tag_old_static
        +autocmd           +find_in_path      -mouse_urxvt       -tag_any_white
        +autochdir         +float             +mouse_xterm       -tcl
        -autoservername    +folding           +multi_byte        -termguicolors
        -balloon_eval      -footer            +multi_lang        +terminal
        -balloon_eval_term +fork()            -mzscheme          +terminfo
        -browse            -gettext           +netbeans_intg     +termresponse
        +builtin_terms     -hangul_input      +num64             +textobjects
        +byte_offset       +iconv             +packages          +textprop
        +channel           +insert_expand     +path_extra        +timers
        +cindent           -ipv6              -perl              +title
        -clientserver      +job               +persistent_undo   -toolbar
        +clipboard         +jumplist          +popupwin          +user_commands
        +cmdline_compl     -keymap            +postscript        -vartabs
        +cmdline_hist      +lambda            +printer           +vertsplit
        +cmdline_info      -langmap           -profile           +virtualedit
        +comments          +libcall           +python/dyn        +visual
        -conceal           +linebreak         -python3           +visualextra
        +cryptv            +lispindent        +quickfix          +viminfo
        +cscope            +listcmds          +reltime           +vreplace
        +cursorbind        +localmap          -rightleft         +wildignore
        +cursorshape       -lua               +ruby/dyn          +wildmenu
        +dialog_con        +menu              +scrollbind        +windows
        +diff              +mksession         +signs             +writebackup
        +digraphs          +modify_fname      +smartindent       -X11
        -dnd               +mouse             -sound             -xfontset
        -ebcdic            -mouseshape        +spell             -xim
        -emacs_tags        -mouse_dec         +startuptime       -xpm
        +eval              -mouse_gpm         +statusline        -xsmp
        +ex_extra          -mouse_jsbterm     -sun_workshop      -xterm_clipboard
        +extra_search      -mouse_netterm     +syntax            -xterm_save
           system vimrc file: "$VIM/vimrc"
             user vimrc file: "$HOME/.vimrc"
         2nd user vimrc file: "~/.vim/vimrc"
              user exrc file: "$HOME/.exrc"
               defaults file: "$VIMRUNTIME/defaults.vim"
          fall-back for $VIM: "/usr/share/vim"
        Compilation: gcc -c -I. -Iproto -DHAVE_CONFIG_H   -DMACOS_X_UNIX  -g -O2 -U_FORTIFY_SOURCE -D_FORTIFY_SOURCE=1
        Linking: gcc   -L/usr/local/lib -o vim        -lm -lncurses  -liconv -framework Cocoa

    Args:
        editor (str): Path to editor

    Returns:
        bool: True if editor is nano otherwise returns False
    """

    cmd = subprocess.run(
        [editor, "--version"], capture_output=True, universal_newlines=True
    )

    match = re.match("^(VIM -)", cmd.stdout)
    return match


def is_nano(editor):
    """Check whether editor is nano by running ``nano --version`` and checking regular expression for output. Shown below is the
    expected output, we will check if output contains "GNU nano"

    .. code-block:: console

         ~/ nano --version
         GNU nano version 2.0.6 (compiled 02:06:59, May  8 2021)
         Email: nano@nano-editor.org	Web: http://www.nano-editor.org/
         Compiled options: --disable-nls --enable-color --enable-extra --enable-multibuffer --enable-nanorc --enable-utf8

    Args:
        editor (str): Path to editor

    Returns:
        bool: True if editor is nano otherwise returns False
    """
    cmd = subprocess.run(
        [editor, "--version"], capture_output=True, universal_newlines=True
    )
    match = re.match("( GNU nano)", cmd.stdout)
    return match


def set_editor(editor=None):
    """Set the editor used for editing files. The editor can be set based on environment ``EDITOR`` or passed as argument
    ``buildtest --editor``. The editor must be one of the following: vi, vim, emacs, nano.

    We check the path to editor before setting value to editor.

    Args:
        editor (str, optional): Select choice of editor specified via ``buildtest --editor``

    Returns:
        str: Return full path to editor
    """
    # prefer command line

    default_editor = shutil.which("vi")

    valid_editors = ["vim", "vi", "emacs", "nano"]

    for editor_name in valid_editors:
        buildtest_editor = shutil.which(editor_name)
        if buildtest_editor:
            break

    # environment variable
    if os.environ.get("EDITOR"):
        buildtest_editor = resolve_path(shutil.which(os.environ["EDITOR"]))

        if not buildtest_editor:
            console.print(
                f"[red]Unable to resolve path via environment EDITOR: {os.environ['EDITOR']}"
            )

    # command line option --editor is specified
    if editor:
        buildtest_editor = resolve_path(shutil.which(editor))
        if not buildtest_editor:
            console.print(
                f"[red]Unable to resolve path to editor specified via command line argument --editor: {editor}"
            )

    # if editor is not found return the default editor which is vi
    if not buildtest_editor:
        return default_editor

    if not (
        is_emacs(buildtest_editor)
        or is_vi(buildtest_editor)
        or is_nano(buildtest_editor)
    ):
        raise BuildTestError(
            f"Invalid editor please select one of the following editors: {valid_editors}"
        )

    return buildtest_editor
