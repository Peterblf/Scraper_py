import os
import re
import unicodedata
import requests
import pandas as pd
from scrapy import Selector

BASE_URL = "http://books.toscrape.com/"
HEADERS = {"User-Agent": "Mozilla/5.0"}
TIMEOUT = 10

# dossiers de sortie
os.makedirs("outputs/csv", exist_ok=True)
os.makedirs("outputs/img", exist_ok=True)

session = requests.Session()
session.headers.update(HEADERS)

r = session.get(BASE_URL, timeout=TIMEOUT)  # creer la session
r.raise_for_status()

sel = Selector(text=r.text)
categories = {}

links = sel.css(
    "div.side_categories ul li ul li a"
)  # recup les categories en parcourant les liens

for a in links:
    name = (
        a.css("::text").get().strip()
    )  # for chaque lien qu'on trouve --> on recup le nom de la categorie
    href = a.attrib["href"]
    url = BASE_URL + href
    categories[name] = url  # dictionnaire des categories avec nom et url

print("Nombre de catégories trouvées :", len(categories))

for name, url in categories.items():
    print("-", name, ":", url)


for cat_name, cat_url in categories.items():  # boucle pour les caté
    print(
        "\nCatégorie :",
        cat_name,
    )
    all_books = []
    page_url = cat_url

    # boucle pour parcourir les pages (pagination)
    while True:
        r = session.get(page_url, timeout=TIMEOUT)
        r.raise_for_status()
        sel = Selector(text=r.text)

        # liens des livres
        book_links = sel.css("h3 a::attr(href)").getall()
        full_links = [
            BASE_URL + "catalogue/" + link.replace("../", "") for link in book_links
        ]

        for link in full_links:  # test les liens des livres
            r = session.get(link, timeout=TIMEOUT)
            r.raise_for_status()
            sel = Selector(text=r.text)

            title = sel.css("div.product_main h1::text").get()
            price = sel.css("p.price_color::text").get()
            stock = sel.css("p.instock.availability::text").getall()
            stock = [s.strip() for s in stock if s.strip()]
            stock = stock[0] if stock else "?"
            rating = sel.css("p.star-rating::attr(class)").get().split()[-1]
            upc = sel.css("table tr:nth-child(1) td::text").get()
            img_rel = sel.css("div.item.active img::attr(src)").get()
            img_url = BASE_URL + img_rel.replace("../../", "")
            category = cat_name

            safe_title = re.sub(
                r'[\\/*?:"<>|]', "_", title
            )  # verif des nom de fichiers (netoyage)
            safe_title = (
                unicodedata.normalize("NFKD", safe_title)
                .encode("ascii", "ignore")
                .decode("ascii")
            )
            safe_title = safe_title[:150]

            img_folder = os.path.join("outputs/img", category)
            os.makedirs(img_folder, exist_ok=True)
            img_path = os.path.join(img_folder, safe_title + ".jpg")

            img_data = session.get(img_url, timeout=TIMEOUT)  # dl l'image
            if img_data.status_code == 200:
                with open(img_path, "wb") as f:
                    f.write(img_data.content)

            all_books.append(  # infos du livre
                {
                    "title": title,
                    "price": price,
                    "stock": stock,
                    "rating": rating,
                    "upc": upc,
                    "category": category,
                    "url": link,
                    "image": img_url,
                }
            )

            print(title, "-", price)

        next_page = sel.css("li.next a::attr(href)").get()  # page suivante ?
        if next_page:

            base = page_url.rsplit("/", 1)[0]  # l’URL suivante
            page_url = base + "/" + next_page
        else:
            break

    # enregistrer les livres de la catégorie dans le CSV
    if all_books:
        df = pd.DataFrame(all_books)
        cat_slug = cat_name.lower().replace(" ", "_")
        csv_path = os.path.join("outputs/csv", f"category_{cat_slug}.csv")
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")
        print(f"{len(all_books)} livres enregistrés dans {csv_path}")
