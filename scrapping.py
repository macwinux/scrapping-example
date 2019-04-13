from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client

# URl to web scrap from.
# in this example we web scrap graphics cards from Newegg.com
page_url = "https://www.carrefour.es/portatiles/cat410364/c?ic_source=portal-y-corporativo&ic_medium=menu-links&ic_content=portal-home"

# opens the connection and downloads html page from url
uClient = uReq(page_url)

# parses html into a soup data structure to traverse html
# as if it were a json data type.
page_soup = soup(uClient.read(), "html.parser")
uClient.close()

paginacion = page_soup.findAll("span", {"class": "pagination__results--bold"})
# name the output file to write to local disk
out_filename = "protatiles.csv"
# header of csv file to be written
headers = "nombre_producto,precio_anterior,precio_actual \n"

# opens file, and writes headers
f = open(out_filename, "w")
f.write(headers)

# loops over each product and grabs attributes about
# each product

pagina = '0'
limite = int(paginacion[2].text)

while int(pagina) < limite:

    page_url = "https://www.carrefour.es/portatiles/cat410364/c?ic_source=portal-y-corporativo&ic_medium=menu-links&ic_content=portal-home&offset=" + pagina
    uClient = uReq(page_url)
    # parses html into a soup data structure to traverse html
    # as if it were a json data type.
    page_soup = soup(uClient.read(), "html.parser")
    items = page_soup.findAll("li", {"class": "product-card-list__item"})
    uClient.close()
    for item in items:
    # Grabs the text within the second "(a)" tag from within
    # the list of queries.
        nombre_producto = item.img["alt"]

        precios = item.find("div", {"class": "product-card__prices-container"})
        try:
            precio_actual = precios.find("span", {"class": "product-card__price--current"}).text.strip()
            precio_anterior = precios.find("span", {"class": "product-card__price--striketrough"}).text.strip()
        except:
            precio_actual = precios.find("span", {"class": "product-card__price"}).text.strip()
            precio_anterior = ''

        f.write(nombre_producto + ", " + precio_anterior + ", " + precio_actual + "\n")


    paginacion = page_soup.findAll("span", {"class": "pagination__results--bold"})
    pagina = paginacion[1].text
    print(pagina)



f.close()  # Close the file

