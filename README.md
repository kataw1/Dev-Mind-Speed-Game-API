# Dev-Mind-Speed-Game-API


# Dev Mind Speed Game (Backend)

A backend-only math game API where players solve math equations quickly by calling REST APIs. Built with Django & DRF.

## Features
- Start game with selected difficulty (1–4)
- Solve math equations via POST requests
- Tracks accuracy and speed
- Ends game and returns score, history, best question

## API Endpoints

- `POST /game/start`
- `POST /game/{game_id}/submit`
- `GET /game/{game_id}/end`

## Difficulty Levels

| Level | Operands | Digits | Operations     |
|-------|----------|--------|----------------|
| 1     | 2        | 1-digit | + - * /        |
| 2     | 2        | 2-digit | + - * /        |
| 3     | 4        | 3-digit | + - * /        |
| 4     | 5        | 4-digit | + - * /        |

## Design Decisions

- SQLite used for local dev; MySQL recommended for production
- Game & Question models normalized for performance
- Stateless API, allows easy Postman/Curl testing
- Time tracking for each question, prevents submission after game ends

## Setup

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
