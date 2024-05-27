import pathlib
from dotenv import load_dotenv
from src.main import GrowBoxApp

if __name__ == '__main__':
    load_dotenv()
    app = GrowBoxApp(root_path=str(pathlib.Path(__file__).parent.resolve()))
    app.run()
