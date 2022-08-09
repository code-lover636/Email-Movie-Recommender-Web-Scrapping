import smtplib, ssl, os
from dotenv import load_dotenv
from email.message import EmailMessage

load_dotenv()
sender = os.environ.get("sender")
password = os.environ.get("password")
reciever = os.environ.get("reciever")
msg = EmailMessage()

def mkhtml(mlist):
    with open("template.html",'r') as f:
        content = f.read()
        content = content.replace("Name","Here are your movie recommendations from IMDB:")
        tag  = ""
        for movie in mlist:
            tag += f"""
                    <br>
                    ----------------------------------------------------------------
                    <br><br>
                    <img src="{movie[3]}" style="
                                          width: auto; 
                                          height: 250px;
                                          " 
                                          alt="Poster Image"">
                    <br><br>
                    <a href="https://www.imdb.com{movie[4]}" style="
                                        color: blue;
                                        font-family: sans-serif;
                                        text-decoration: none;
                                        ">
                        Movie: {movie[0]}
                    </a>
                    <p style="
                        color: black;
                        font-family: sans-serif;
                        ">
                        Released Year: {movie[1]}
                    </p>
                    <p style="
                        color: black;
                        font-family: sans-serif;
                        ">
                        IMDB Rating: ⭐{movie[2]}
                    </p>
                    """
        content = content.replace("<p></p>",tag)
        return content
        
        

def send(mlist):
    msg['From'] = sender
    msg['To'] = reciever
    msg['Subject'] = "Movie Recommendations"
    msg.add_alternative(mkhtml(mlist), subtype='html')
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com",465, context=context) as server:
        server.login(sender, password)
        server.send_message(msg)
     