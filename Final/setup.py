from cx_Freeze import setup, Executable
includefiles = ["music1.wav", "music2.wav", "music3.wav"]
includes = ["sqlite3"]
setup(name="Fightclub", version="1.0", description="Fightclub is a game developed by Halil Bilen, Kevin Chiu, Vincent Pruijn and Floris-Jan Willemsen.", executables=[Executable("Game.py")])