import os
import pandas
import datetime as dt
import random
import smtplib

my_email = os.environ.get("MY_EMAIL")
password = os.environ.get("MY_PASSWORD")

udaje = pandas.read_csv("birthdays.csv")
udaje_slovnik = udaje.to_dict(orient="records")
list_listov = []

for poradie in range(1, 4):
    with open(f"letter_templates/letter_{poradie}.txt", encoding="utf-8") as letter:
        riadky = letter.read()
        list_listov.append(riadky)

now = dt.datetime.now()
rok = now.year
mesiac = now.month
den = now.day
dnes = now.weekday()
dnesny_datum = dt.datetime(year=rok, month=mesiac, day=den)

for clovek in udaje_slovnik:
    den_narodenia = dt.datetime(
        year=rok, month=clovek["month"], day=clovek["day"]
    )
    if den_narodenia == dnesny_datum:
        random_list = random.choice(list_listov)
        finalny_text = random_list.replace("[NAME]", clovek["name"])
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=clovek["email"],
                msg=f"Subject: Happy BDay\n\n{finalny_text}",
            )
    else:
        print(f"{clovek['name']} nemá narodeniny")
