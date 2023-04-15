## Info

> Tested only on MacOS

Requires Python > 3.7

## Setup

There is a chance that your machine might block `setup.sh` file from being executed so you have to make it executable.

1. Make `setup.sh` executable by running `chmod 755 ./setup.sh`
2. Run `./setup.sh`
3. Activate virtualenv `source ./venv/bin/activate`.
4. Go to Github account -> Settings -> Developer settings -> Personal access tokens -> Tokens (Classic)
5. Click Generate new token -> Generate new token (classic)
6. Fill `Note`
7. Click `Generate Token` (Do not check anything from permissions. Not needed.)
8. Paste your token on `.env.local` file on `GITHUB_ACCESS_TOKEN` variable.
9. Execute `flask run --host=0.0.0.0 --port=8000`

## Improvements and enhancements

1. `src/log.py` -> We can improve logging by implementing DataDog service.
2. `src/endpoints/github.py` -> The validation on `/fork` endpoint can be enhanced by implementing `JsonSchema` or `Cerberus` library.
3. `src/ghub.py list_repositories()` -> To improve the speed whe can cache the list of repos, either in DB or Redis.
4. Unit-Test and integration test.