# Project README

## Project Description

This project is a combination of Rust and Python applications that work together to provide a service. The service
allows users to record audio, transcribe it into text, and then generate a shopping list item from the transcribed text.

## How the Service Works

1. The Rust application records audio from the user's microphone for a specified duration and saves it as a `.wav` file.
2. The Rust application sends a request to the Python application, passing the name of the `.wav` file as a parameter.
3. The Python application receives the file name, loads the file from disk, and transcribes the audio into text using
   the Whisper ASR model from OpenAI.
4. The transcribed text is then passed to a language model, which generates a new shopping list item.
5. The new shopping list item is returned to the Rust application, which then adds the item to the shopping list using
   the `bring` command.

## Prerequisites

This project only works on Windows.
You will need to install my bring cli tool to run this project. You can find
it [here](https://github.com/ViktorWelbers/Bring-CLI).

I am currently working on distributing part of the CLI as a library so that it can be used on other platforms and it
doesn't have to be called as a subprocess.

## Running the Project

To run the project, you need to start both the Rust and Python applications. The Python application should be started
first, as it needs to be running when the Rust application sends the request.

To start the Python application, navigate to the Python directory and run the following command:

```bash
pip install -r requirements.txt
python python/main.py
```

To start the Rust application, navigate to the Rust directory and run the following command:

```bash
cargo run
```

## Dependencies

The project has several dependencies, which are listed in the `Cargo.lock` file for the Rust application and in
the `requirements.txt` file for the Python application. The dependencies include several crates and Python packages for
handling audio, making HTTP requests, and working with machine learning models.

## Todo

1. Export the functionality of the Bring! Client to Python so that it can be used on other platforms.
2. Scrap the Rust application and use Python for the whole project.
3. Add a Wakeword detection model to the project.
