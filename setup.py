import sys

from cx_Freeze import Executable, setup

try:
    from cx_Freeze.hooks import get_qt_plugins_paths
except ImportError:
    include_files = []
else:
    # Inclusion of extra plugins (new in cx_Freeze 6.8b2)
    # cx_Freeze imports automatically the following plugins depending of the
    # use of some modules:
    # imageformats - QtGui
    # platforms - QtGui
    # mediaservice - QtMultimedia
    # printsupport - QtPrintSupport
    #
    include_files = get_qt_plugins_paths("PyQt5", "platforms")

# base="Win32GUI" should be used only for Windows GUI app
base = None
if sys.platform == "win32":
    base = "Win32GUI"

build_exe_options = {
    "excludes": ["tkinter"],
    "include_files": include_files,
}

executables = [Executable("main.py", base=base, target_name="Lissajous.exe")]

setup(
    name="Lissajous",
    version="0.1.1",
    description="Qt5 + matplotlib Lissahous curve generator",
    options={
        "build_exe": build_exe_options
    },
    executables=executables,
)
