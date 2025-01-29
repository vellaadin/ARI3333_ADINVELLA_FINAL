import subprocess
import sys

def ensure_module_installation(module_name, pip_name=None):
    try:
        __import__(module_name)
        print(f"'{module_name}' found on the machine")
    except ImportError:
        print(f"!!WARNING: {module_name} is not installed on your machine !!\nInstallation will take place now.")
        pip_name = pip_name or module_name
        subprocess.check_call([sys.executable, "-m", "pip", "install", pip_name])
        print(f"!! {module_name} installed successfully !!")

def ensure_streamlit_installation():
    ensure_module_installation("streamlit")

def ensure_requests_installation():
    ensure_module_installation("requests")

def ensure_dotenv_installation():
    ensure_module_installation("dotenv", "python-dotenv")

def installPrereq():
    ensure_streamlit_installation()
    ensure_requests_installation()
    ensure_dotenv_installation()

def combine_inputs(main_idea, genre, theme, tone, key_character, setting):
    return (
        f"Main Idea: {main_idea}\n"
        f"Genre: {genre}\n"
        f"Theme: {theme}\n"
        f"Tone: {tone}\n"
        f"Key Character: {key_character}\n"
        f"Setting: {setting}"
    )

def generate_prompt(main_idea, genre, theme, tone, key_character, setting):
    return (
        f"Assume you are a narrative story writer. You will output an entire narrative story only. "
        f"Write a {tone.lower()} {genre.lower()} story. "
        f"The main idea is: {main_idea}. "
        f"The story revolves around a {key_character.lower()} in a {setting.lower()}. "
        f"The theme of the story is {theme.lower()}. "
        "Ensure the story has a clear beginning, middle, and end. "
        "Ensure also that the story is as long as possible. "
        "Also, give the story a title."
    )


def installPrereq():
    ensure_streamlit_installation()
    ensure_requests_installation()
    ensure_dotenv_installation()