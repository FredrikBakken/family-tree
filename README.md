# Family Tree
Build your family tree.

This application scrapes the Geni website for all direct parents of an individual, before visualizing the results.

**Be aware:** This is a web scrapes - which means that if the layout of the Geni pages changes, this application may no longer function as intended.

# Prerequists
## Visualization with Graphviz
Graphviz is necessary for creating the image: `sudo apt install graphviz`

## Python
Application was developed in Python v3.9.5, however previous Python 3 versions should work fine.

### Setup a Virtual Environment and Install the Requirements
```
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements
```

# Application Execution
The application requires that the user provides the URL for the root node as an input argument, e.g.:
```
python3 app.py https://www.geni.com/people/Petter-Dass/349753054790012626
python3 app.py <URL>
```

**Note:** A two second delay is added between every web request to avoid server instabilities for the service provider.
