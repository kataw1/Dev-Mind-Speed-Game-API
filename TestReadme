# DevMind Game API - Test Suite

This repository contains automated tests for the DevMind Game API built using Django REST Framework (DRF). The tests ensure correct behavior for starting a game, submitting answers, handling game termination, and retrieving a game summary.

It is not work verywell because it is beyond my experiance

## 📁 File Structure

## ✅ Covered Endpoints

| Method | Endpoint             | Description                      |
|--------|----------------------|----------------------------------|
| POST   | `/game/start`        | Starts a new game                |
| POST   | `/game/{id}/submit`  | Submits an answer to the game    |
| GET    | `/game/{id}/end`     | Ends the game and returns summary|

---

## 🧪 Tests Overview

### `test_start_game`

Starts a new game and checks:

- Response status is `200 OK`
- Response includes:
  - `question`: the initial question
  - `submit_url`: URL for submitting answers

---

### `test_submit_answer_and_get_next_question`

Simulates:

1. Starting a game
2. Submitting an answer
3. Verifying:
   - Answer submission is accepted (`200 OK`)
   - Response includes `result`, `next_question`, and `current_score`

---

### `test_end_game_blocks_submission`

Checks behavior after ending the game:

- After calling `/game/{id}/end`, further submissions to `/game/{id}/submit` are blocked
- Submission after end returns `400 Bad Request` with an `error` field

---

### `test_end_game_summary_output`

Confirms the summary returned by `/game/{id}/end` contains:

- `name`
- `difficulty`
- `current_score`
- `total_time_spent`
- `history`

---

## 🚀 Running the Tests

Make sure you have the Django environment set up and the test database migrated.

```bash
python manage.py test
