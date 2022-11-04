# Grab app from main
from main import app

# DEFINE API root
API_ROOT = "/api/v1"

# Import api routes
from . import game
from . import matchmaking
from . import user