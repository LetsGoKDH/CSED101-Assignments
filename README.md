# CSED101-Assignments

This repository is a collection of my coursework code for **CSED101 (Programming & Problem Solving)**.  
The goal is to keep my assignments organized in one place and to leave short, readable notes so that I (and others) can understand what each project is about without needing the original handouts.

> Academic Integrity Notice  
> This repository is for learning/record-keeping (and optional portfolio) purposes.  
> Please do not copy/paste for coursework submissions.  
> I intentionally do **not** include the original assignment PDFs, official test cases, or grading scripts.

---

## Repository Structure

- `assignments/assn1/` : Assignment 1 source code
- `assignments/assn2/` : Assignment 2 source code
- `assignments/assn3/` : Assignment 3 source code
- `assignments/assn4/` : Assignment 4 source code

Each assignment is separated into its own folder to keep the repository easy to browse.  
Only my implementation code is included.

---

## Contents

### Assn 1 — Horse Race (CLI)
A text-based, menu-driven program that updates internal state based on user input and runs a simple simulation.  
I focused on building clean control flow (menus and loops), validating inputs, and organizing the logic into small functions instead of writing everything in one block.

**Keywords:** control flow, input validation, modular functions, CLI

---

### Assn 2 — Connect Four (CLI)
A playable Connect Four game in the terminal. It includes the core game logic (board updates, turn handling, win checking), a structured menu flow, and basic save/load functionality. The computer player behaves differently depending on the selected difficulty, ranging from simple random choices to basic tactical decisions (e.g., immediate win/block when possible).

**Keywords:** game state, board logic, simple AI, save/load, CLI

---

### Assn 3 — Text RPG / OOP (“Ponix”)
An object-oriented text-based game centered around a “player” and related game systems. The code is structured around classes and methods, and the gameplay loop manages progression through actions such as upgrades, inventory/storage management, and shop-like interactions.  
This assignment was mainly about designing a clean class structure and keeping responsibilities separated across components.

**Keywords:** OOP, class design, game loop, state management

---

### Assn 4 — Chimp Memory Test (Tkinter GUI)
A GUI memory game inspired by “chimp test” mechanics, implemented using Tkinter. The program manages multiple phases (showing targets vs. user input), tracks score/lives, and updates the UI in response to events (mouse clicks).  
This assignment emphasized GUI state management, event-driven programming, and keeping the interface logic organized rather than scattered across callbacks.

**Keywords:** Tkinter, GUI, event handling, state machine, user interaction
