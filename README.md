A small image inspector

**Prerequisites**
Python 3.8+ (Recommended 3.11), pip, Homebrew.

## Setting up the environment

Follow these steps once to create and use a Python virtual environment for this project.

1) Check Python and venv availability

```zsh
python3 --version
python3 -m venv --help
```

2) (Optional) Install/upgrade Python via Homebrew

If you don't have a recent Python 3, install it with Homebrew:

```zsh
brew install python
```

3) Create a virtual environment (from the project root)

```zsh
cd /Users/roope/Desktop/osint
python3 -m venv .venv
```

4) Activate the virtual environment (zsh)

```zsh
source .venv/bin/activate
# prompt shows (.venv)
```

5) Upgrade pip and install dependencies

```zsh
pip install --upgrade pip
pip install -r src/requirements.txt
```