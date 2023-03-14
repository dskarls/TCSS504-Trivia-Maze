# TCSS504-Trivia-Maze
Main group group project for TCSS504

This repository contains an implementation of the Trivia Maze Dungeon Adventure course project for TCSS504 (Software Engineering and Development Techniques, Winter 2023) at the University of Washington, Tacoma.

## Installation requirements
- Any python3 installation with the `tkinter` module should be sufficient to run the game.
- This game is designed to run on macOS. If run in windowsOS, its GUI will likely not appear properly.
- If you wish to run the included unit tests, `pytest` is required

## How to run
- From the command line, run `python3 main.py` in the top-level directory of the repo.

## Repository Contents

- db/

  Contains the raw data used to construct the trivia question & answer database. Every time the game is run, a SQLite database is created in memory.
  
- doc/

  Contains the app.diagrams.net source XML file and an up-to-date PDF rendering of it.
  
- test/

  Contains the pytest unit test files relevant to the Model of the MVC pattern implemented.
