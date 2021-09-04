# Fastest code wins
Fight to be on top of the leaderboard.

## Running locally
- Install the api requirements with `pip install -r requirements.txt`
- Build the docker images for the runtimes. ie: for js `docker build . -f javascript.Dockerfile  -t javascript_runtime`
- Start the server with `uvicorn api:app --host 0.0.0.0 --reload`

## Adding a test
- Copy the example `add.json` in `questions/`

## Adding a runtime
- Create a docker runtime
- Create a `soln.lang` and matching `lang_soln.jinja` in `/solvers`
- add the extension mapping in `api.py`
- add the template solution to the js map in `templates/question.html`
