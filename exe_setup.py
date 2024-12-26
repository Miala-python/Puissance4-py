from cx_Freeze import Executable, setup
#pr entrer dans un dossier: cd <nom_dossier>
#python setup.py build
#pr crée l'executable
setup(
    name = "Puissance 4",
    version = "1.02.0",
    description = "Le jeu du Puissance 4 par Miala",
    executables = [Executable("index.py")]
)



