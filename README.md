# diploma-webapp

Diploma project which uses CNN to classify images. It uses Flask as a base for web application.

# Usage

First, you need to clone this project using git.

When downloaded, `cd` into the project folder and install the required packages:

```
pip install -r requirements.txt
```

After installation is complete, run this commands:

```
flask db upgrade
flask seed
```

First command will create a default SQLite database in the folder.

Also, you **HAVE** to create a folder `img` in `app/static/` to successfully run and use the application.

To run application, run this command:

```
flask run
```

It will start the server to host the application, and will also show you the address in the terminal, which you need to enter into the browser.
