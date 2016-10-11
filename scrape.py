import credentials
import smtplib
from lxml import etree

url = "http://www.audiomusica.com/catalogo/controlador-dj-mixdeck-quad-4-canales.html"
#XPath to the price
xp = '''//*[@id="product_addtocart_form"]/div[2]/div/div/div[1]/div[4]/div[1]/div[2]/div/span'''
price_file = "old_price.txt"

def scrape():
    htmlparser = etree.HTMLParser()
    tree = etree.parse(url, htmlparser)
    price = tree.xpath(xp)[0].text
    price = int(price.replace("$", "").replace(".", ""))
    check, old_price = check_price(price)
    if check:
        send_mail(old_price, price)
        save_new_price(price)
        print ("Mail sent")
    else:
        print ("No change")

def save_new_price(price):
    with open(price_file, "w") as f:
        f.write(str(price))

def check_price(price):
    with open(price_file, "r") as f:
        old_price = int(f.read())
        if price < old_price:
            return True, old_price
        else:
            return False, old_price

def send_mail(old_price, price):
    fromaddr = 'santiagolarrain@gmail.com'
    toaddrs  = 'jtlarraine@gmail.com'
    subject = "El precio de su producto ha cambiado"
    msg = '\n \
    Estimado Cliente,\n\n \
    El producto al que Ud. se ha suscrito, ha experimentado una baja en su precio.\n\n \
    Precio Antiguo: ${0}\n \
    Precio Actual: ${1}\n\n \
    Esperamos que esta informacion le sea de utilidad.\n\n \
    Sin otro particular, saluda muy atentamente a Ud.,\n\n \
    Santiago Larrain\n \
    CEO\n \
    PacificLabs.cl'.format(old_price, price)

    message = 'Subject: %s\n\n%s' % (subject, msg)
    # Credentials (if needed)
    username = credentials.username
    password = credentials.password

    # The actual mail send
    server_addr = 'smtp.gmail.com:587'
    server = smtplib.SMTP(server_addr)
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, message)
    server.quit()

if __name__ == '__main__':
    scrape()
