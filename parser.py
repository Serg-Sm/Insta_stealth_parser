from config_data.config import InstagramBot
from actions.parsing_posts_of_user import get_posts_of_user
from actions.download_media import download_content
from actions.parsing_followers import get_followers_of_user


def main():
    InstagramBot().login()
    get_posts_of_user()
    download_content()
    get_followers_of_user()
    InstagramBot().close_browser()


if __name__ == '__main__':
    main()

