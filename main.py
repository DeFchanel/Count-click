import requests
import os
from dotenv import load_dotenv,dotenv_values
import argparse


def shorten_link(args, token):
    body = {
        "long_url": args
    }
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.post(
        'https://api-ssl.bitly.com/v4/shorten',
        headers=headers,
        json=body
    )
    response.raise_for_status()
    return response.json()['id']


def count_clicks(args, token):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    clicks_count_url = f"https://api-ssl.bitly.com/v4/bitlinks/{args}/clicks/summary"
    clicks_response = requests.get(
        clicks_count_url,
         headers=headers
    ) 
    clicks_response.raise_for_status()
    return clicks_response.json()["total_clicks"]


def is_bitlink(args, token):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    is_bitlink_url = f'https://api-ssl.bitly.com/v4/bitlinks/{args}'
    response = requests.get(
        is_bitlink_url,
        headers=headers
    )
    return response.ok


if __name__ == "__main__":
    load_dotenv()
    token = os.getenv('BITLY_TOKEN')
    parser = argparse.ArgumentParser(
        description='Программа преобразует ссылку в битлинк или подсчитывают количество переходов по битлинку'
    )
    parser.add_argument('link', help='Ссылка')
    args = parser.parse_args()
    try:
        if is_bitlink(args.link, token):
            print(
                'По вашей ссылке прошли:',
                count_clicks(args.link, token),
                'раз(а)'
            )  
        else:
            print(
                'Битлинк:', shorten_link(args.link, token)
            )
    except requests.HTTPError:
        print(
            "Вы ввели неправильную ссылку или неверный токен."
        )
