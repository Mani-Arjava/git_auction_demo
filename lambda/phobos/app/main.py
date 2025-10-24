from mangum import Mangum
from app.api.server.app import app

# Lambda handler - this is what AWS Lambda will call
handler = Mangum(app)

# For local development, you can also run:
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)