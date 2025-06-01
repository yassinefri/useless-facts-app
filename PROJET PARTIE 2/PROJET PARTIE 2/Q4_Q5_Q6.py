
from PIL import Image, ImageOps

# Étape 4 : Utiliser une image fournie (représentant le contenu du livre)
image1 = Image.open("0403.jpg").convert("RGB")  # Assurez-vous que ce fichier est dans le même dossier

# Étape 5 : Recadrer et redimensionner l'image à 300x300 pixels
image1 = ImageOps.fit(image1, (300, 300))

# Étape 6 : Générer un logo noir et blanc, le faire pivoter et le coller
logo = Image.new("L", (100, 100), 255)  # Image blanche
logo = ImageOps.invert(logo)           # Devient noire
logo = logo.rotate(45)                 # Pivot de 45 degrés
image1.paste(logo.convert("RGB"), (20, 20), logo)

# Enregistrement de l'image finale
image1.save("image_finale.jpg")
print("Image enregistrée sous : image_finale.jpg")
