from dotenv import load_dotenv

from voidex.app import run_chat_interface

def main():
    # Load environment variables
    load_dotenv()

    # Run the Streamlit chat interface
    run_chat_interface()

if __name__ == '__main__':
    main()