from mangum import Mangum
from .api.server.app import app

handler = Mangum(app)
