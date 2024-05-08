# Tabnews Alert

Tabnews Alert is a Python-based project that automatically fetches data from the Tabnews API, filters posts titles based on specific keywords, and sends an email alert with the posts. The main purpose of this project is to automate the process of monitoring Tabnews for specific content and alerting the user when such content is published.

## Technologies Used

- Python: The main programming language used for this project.
- pip: A package installer for Python, used to manage project dependencies.
- requests: A Python library for making HTTP requests.
- smtplib: A Python library for sending emails using the Simple Mail Transfer Protocol (SMTP).
- dotenv: A Python library for handling environment variables.

## Lessons Learned

During the development of this project, I learned how to interact with APIs using the requests library, how to send emails using smtplib, and how to manage environment variables using dotenv. I also gained experience in filtering and processing data in Python.

## How to Use

1. Clone the repository to your local machine.
2. Install the required dependencies using pip: `pip install -r requirements.txt`.
3. Set up your environment variables in a `.env` file. You will need to specify the following variables: `FROM`, `PASSWORD`, and `TO`.
4. Run the main script: `python src/app.py`.
