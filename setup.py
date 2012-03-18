from cx_Freeze import setup, Executable

setup(
        name = "mazerun",
        version = "0.1",
        description = "MazeRun",
        executables = [Executable("mazerun.py")],
        includes = ('game',)
)
