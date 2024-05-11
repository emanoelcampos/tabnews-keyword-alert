import os
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
from dotenv import load_dotenv

from posts import Posts
from logger import setup_logger

logger = setup_logger()


def get_api_data(page):
    api_url = "https://www.tabnews.com.br/api/v1/contents"
    parameters = {
        "page": page,
        "per_page": 100,
        "strategy": "new"
    }

    response = requests.get(api_url, params=parameters)
    logger.info(f"API response: {response.status_code}.")
    return response.json()


def filter_posts_by_previous_day():
    previous_day_posts = {}
    page = 1

    while True:
        posts = get_api_data(page)
        post_info = Posts.extract_post_info(posts)
        for id_, post in post_info.items():
            if post.is_created_yesterday():
                previous_day_posts[id_] = post

        last_post = list(post_info.values())[-1]
        if not last_post.is_created_yesterday():
            break
        else:
            page += 1

    logger.info(f"Filtered posts from yesterday: {len(previous_day_posts)}.")
    return previous_day_posts


def filter_post_by_keywords(previous_day_posts, keywords):
    posts_with_keywords = {}
    for key, post in previous_day_posts.items():
        if post.contains_keywords(keywords):
            posts_with_keywords[post.id_] = post
    return posts_with_keywords


def format_post_title_link(posts_with_keywords):
    tabnews_url = "https://www.tabnews.com.br"
    post_title_link = {}
    if not posts_with_keywords:
        logger.info("No posts from yesterday with the keywords.")
        sys.exit()
    else:
        logger.info(f"Yesterday's posts found with keyword: {len(posts_with_keywords)}.")
    for id_, post in posts_with_keywords.items():
        post_title_link[post.title] = f'{tabnews_url}/{post.owner_username}/{post.slug}'
    return post_title_link


def format_email_data(post_title_link):
    html_title_link = ''
    for title, link in post_title_link.items():
        html_title_link += f'<li style="margin-bottom: 10px;"><a href="{link}"style="color: #007bff; text-decoration: none; font-size: larger">{title}</a></li>'

    with open("src/templates/email_template.html", "r", encoding="utf-8") as file:
        html_template = file.read()

    html_content = html_template.replace("{html_post}", html_title_link)
    return html_content


def send_alert(html_content):
    load_dotenv()
    try:
        smtp_port = 587
        smtp_server = 'smtp.gmail.com'
        smtp_username = os.environ['FROM']
        smtp_name_from = os.environ['NAME_FROM']
        smtp_password = os.environ['PASSWORD']
        smtp_to = os.environ['TO']

        message = MIMEMultipart()
        message['Subject'] = 'Alerta de Conteúdo no Tabnews!'
        message['From'] = f'{smtp_name_from} <{smtp_username}>'
        message['To'] = smtp_to
        message.attach(MIMEText(html_content, 'html'))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(smtp_username, smtp_to, message.as_string())
            server.quit()
        logger.info("Email sent successfully.")

    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")


def main():
    keywords = ['RPA', 'Automação', 'Python', 'Análise de Negócios', 'Bot', 'Script']

    previous_day_posts = filter_posts_by_previous_day()
    posts_with_keywords = filter_post_by_keywords(previous_day_posts, keywords)
    post_title_link = format_post_title_link(posts_with_keywords)
    html_content = format_email_data(post_title_link)
    send_alert(html_content)


if __name__ == "__main__":
    main()
