import requests

frieren = requests.get('https://api.jikan.moe/v4/anime/52991/full').json()

print(f"Anime Title: {frieren['data']['title_english']}")
print(f"Episodes: {frieren['data']['episodes']}")
print(frieren['data']['status'])
print(frieren['data']['duration'])