
import os

def getenviron(var, default):
    return os.environ[var] if var in os.environ else default
