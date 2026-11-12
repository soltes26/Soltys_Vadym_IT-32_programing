import qrcode

NAME = "Vadym Soltys"
GROUP = "IT-32"
EMAIL = "vadym.soltys@example.com"  # ЗАМІНІТЬ НА СВІЙ EMAIL

print(f"{NAME}, {GROUP}")

# дані студента — латиницею
text = f"{NAME}, {GROUP}, {EMAIL}"
image = qrcode.make(text)
image.save("contact.png")
print("saved: contact.png")
