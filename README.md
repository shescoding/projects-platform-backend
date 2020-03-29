## How to contribute
Create or pick a feature from https://github.com/shescoding/projects-platform-backend/projects/1.

## Community
Join our slack space at She's Coding #projects channel to discuss this projects or ask questions.


## Installation guide

### Mac OS X Only - Setup Homebrew

These project installation instructions assume that Mac users have [Homebrew](https://brew.sh/) installed.

To install Homebrew, run the following in a terminal window:

```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```
---

### Windows 10 Only - Setup Ubuntu on WSL

If you're on Windows 10, we recommend (and base these instructions on) using Ubuntu on WSL (Windows Subsystem for Linux)

To install WSL, follow the [Windows Subsystem for Linux Installation Guide for Windows 10](https://docs.microsoft.com/en-us/windows/wsl/install-win10) (Note that in the step where you open the Microsoft Store and choose your favorite Linux distribution, choose **Ubuntu 18.04 LTS**)

When you run commands in the below instructions, you should do so in an Ubuntu window. To open an Ubuntu Window, search for "Ubuntu" next to the start button in Windows 10 and click on **Ubuntu 18.04 LTS**

---

### Add Project to Local Machine

Fork this repository by clicking the **Fork** button in the upper right hand corner of the repository's GitHub page. (You can skip this step and instead clone this repository instead of your fork in the next step if you've been added as a collaborator for this project)

Click the green **Clone or Download** button on your fork of the repository on GitHub and copy the URL under **Clone with HTTPS**.
In a terminal window, navigate to the directory where you want to install the project and run `git clone https://github.com/username/projects-platform-backend.git` (replace the URL with the one you copied--the only difference may be that _username_ is replaced with your GitHub username)

Change to the `projects-platform-backend` directory: 
```
cd projects-platform-backend
```
---

### Install pipenv

[pipenv](https://pipenv.readthedocs.io/en/latest/) is used in this project to manage dependencies/virtual environments.

#### Mac

```
brew install pipenv
```

#### Windows 10 WSL / Ubuntu

Update Path to avoid ImportError (see [this pipenv issue](https://github.com/pypa/pipenv/issues/2122#issuecomment-386207878))

```
echo 'export PATH="${HOME}/.local/bin:$PATH"' >> ~/.bashrc
```

Install pip

```
sudo apt install python3-pip
```

Install pipenv

```
python3 -m pip install --user pipenv
```

Note: Installing `pipenv` currently breaks `pip`. If you use pip and get an error that mentions `ImportError: cannot import name main`, then you can try reinstalling pip:

```
sudo apt remove python3-pip
sudo rm -rf ~/.local/lib/python3.8/site-packages/pip*
sudo apt install python3-pip
```

#### Other Operating Systems

See [Installing pipenv in documentation](https://pipenv.kennethreitz.org/en/latest/install/#installing-pipenv)

---

### Install pyenv

 You may have multiple versions of Python installed on your system and we recommend using [pyenv](https://github.com/pyenv/pyenv) to manage multiple versions of Python. We use pyenv in this project to set the local version of Python for the project to be 3.8.0.

#### Mac

```
brew install pyenv
```

Note: If you use a different shell than bash and/or don't use terminal, you may need to update the command below by changing `.bash_profile` to the file for your shell. See the [documentation](https://github.com/pyenv/pyenv/blob/master/README.md#basic-github-checkout).

```
echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bash_profile
```

#### Windows 10 WSL / Ubuntu

```
sudo apt-get update; sudo apt-get install --no-install-recommends make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

git clone https://github.com/pyenv/pyenv.git ~/.pyenv

echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc

echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bashrc
```

#### Other Operating Systems

See [Installation in pyenv documentation](https://github.com/pyenv/pyenv#installation)

---

The rest of the commands below should work on all Operating Systems. Make sure you're in the root directory for the project before running them.

### Install Python 3.8-dev

```
pyenv install 3.8-dev
```

### Set local version of Python to 3.8-dev

This will set the version of Python used for the project to be 3.8-dev

```
pyenv local 3.8-dev
```

_You can verify which version of Python you're using  by running `python --version`._

### Install Dependencies

This will install the packages listed in `Pipfile` to be used for this project only.

```
pipenv install
```
or 
```
pipenv install requirements.txt
```
or 
```
pip install requirements.txt
```
or 
```
pip3 install requirements.txt
```
or try installing individually. Ex:
```
pip install asgiref==3.2.3
```

Install psycopg2 separately:

```
sudo apt-get install python3-psycopg2
```

### Start Local Development Server

```
./manage.py runserver     
```

### Install Postgres
Notes for installing Postgres - https://github.com/shescoding/projects-platform-backend/pull/9

### View Local Version of App
Once the local development server is up and running, it will provide a URL that you can open in your web browser. This is what you will likely see:
> Starting development server at http://127.0.0.1:8000/

# Get Environment Variables from Google Drive
It contains all the passwords and secret keys needed for the project. Note: you might need to request access for this file - https://drive.google.com/file/d/1x5-7mNvgJk7efDfr1iwLV7SwDjZcdfEC/view?usp=sharing

