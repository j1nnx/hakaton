import uvicorn
from api import app  # Импортируем FastAPI приложение

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
