import yagmail
yag = yagmail.SMTP({'footrshoes@gmail.com': 'Footr'}, '6&gdIHgds^$7')

def order_confirmation(destination, name, ordernum):
    try:
        contents = ["""
            <h1>Order confirmation</h1>
            <p>Thanks for your order """ + name + """. It will be with you soon!</p>

            <h3>Details:</h3>
            <p>Order number: """ + ordernum + """</p><br>
            <p>Name: """ + name + """</p><br>
            """]

        yag.send('benjybum2003@outlook.com', 'Order confirmation', contents)
        print("email successful")
    except:
        print("Email failed to send. Destination:" + destination)
