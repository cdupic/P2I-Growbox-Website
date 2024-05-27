from dotenv import load_dotenv
from src.main import GrowBoxApp

if __name__ == '__main__':
    load_dotenv()
    app = GrowBoxApp()
    app.run()
