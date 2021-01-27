from dotenv import load_dotenv
import os

# Load API keys from .env file

load_dotenv()

shodan_key = os.getenv('SHODAN_KEY')


