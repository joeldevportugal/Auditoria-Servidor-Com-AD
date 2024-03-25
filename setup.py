import sys
from cx_Freeze import setup, Executable
import os

# Dependências são detectadas automaticamente, mas pode ser necessário ajuste fino.
build_exe_options = {
    "packages": ["os", "pyad", "reportlab"],
    "includes": ["tkinter", "tkinter.messagebox"],
    "include_files": [(os.path.join(sys.base_prefix, "DLLs", "tk86t.dll"), "DLLs/tk86t.dll"),
                      (os.path.join(sys.base_prefix, "DLLs", "tcl86t.dll"), "DLLs/tcl86t.dll")],
}

# Aplicações GUI requerem uma base diferente no Windows (o padrão é para uma aplicação de console).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="AuditoriaActiveDirectory",
    version="0.1",
    description="Auditoria de Servidor Active Directory",
    options={"build_exe": build_exe_options},
    executables=[Executable("Auditoria.py", base=base)],
)

