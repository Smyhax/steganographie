from PIL import Image
import os

def validate_file_extension(file_path):
    """Valide que le chemin contient une extension .png."""
    if not file_path.lower().endswith('.png'):
        raise ValueError("Le fichier doit avoir une extension .png. Exemple : 'dossier/image.png'")

def hide_message(input_image_path, output_image_path, secret_message):
    """Cache le message secret dans l'image d'entrée et sauvegarde dans l'image de sortie."""
    validate_file_extension(input_image_path)
    validate_file_extension(output_image_path)

    image = Image.open(input_image_path)
    if image.mode != 'RGB':
        print("L'image n'est pas en mode RGB. Conversion en cours...")
        image = image.convert('RGB')

    encoded_image = image.copy()

    # Convertir le message secret en binaire et ajouter un marqueur de fin
    binary_message = ''.join(format(ord(char), '08b') for char in secret_message) + '1111111111111110'

    if len(binary_message) > image.width * image.height * 3:
        raise ValueError("Le message est trop long pour être caché dans cette image.")

    binary_index = 0
    pixels = list(image.getdata())
    new_pixels = []

    for pixel in pixels:
        if not isinstance(pixel, tuple):
            pixel = (pixel, pixel, pixel)  # Convertir en tuple RGB si nécessaire
        new_pixel = list(pixel)
        for i in range(3):
            if binary_index < len(binary_message):
                new_pixel[i] = (new_pixel[i] & ~1) | int(binary_message[binary_index])
                binary_index += 1
        new_pixels.append(tuple(new_pixel))

    encoded_image.putdata(new_pixels)
    encoded_image.save(output_image_path)
    print(f"Message caché dans l'image {output_image_path}")


def reveal_message(image_path):
    """Extrait le message caché dans l'image."""
    validate_file_extension(image_path)

    image = Image.open(image_path)
    if image.mode != 'RGB':
        print("L'image n'est pas en mode RGB. Conversion en cours...")
        image = image.convert('RGB')

    pixels = list(image.getdata())

    binary_message = ''
    for pixel in pixels:
        if not isinstance(pixel, tuple):
            pixel = (pixel, pixel, pixel)  # Convertir en tuple RGB si nécessaire
        for i in range(3):
            binary_message += str(pixel[i] & 1)

    # Chercher la position exacte du marqueur de fin
    end_index = binary_message.find('1111111111111110')
    if end_index != -1:
        binary_message = binary_message[:end_index]  # Tronquer les bits après le marqueur

    # Diviser par blocs de 8 bits valides
    chars = [binary_message[i:i+8] for i in range(0, len(binary_message), 8) if len(binary_message[i:i+8]) == 8]
    message = ''.join(chr(int(char, 2)) for char in chars)

    print("Message révélé :", message)
    return message


def interactive_cli():
    while True:
        print("\nMenu Stéganographie :")
        print("1. Cacher un message")
        print("2. Révéler un message")
        print("3. Quitter")

        choice = input("Choisissez une option : ")
        if choice == '1':
            while True:
                input_image = input("Entrez le chemin de l'image d'entrée (doit être .png, ex: 'input/image.png') : ")
                try:
                    validate_file_extension(input_image)
                    break
                except ValueError as e:
                    print(f"Erreur : {e}")

            while True:
                output_image = input("Entrez le chemin de l'image de sortie (doit être .png, ex: 'output/image.png') : ")
                try:
                    validate_file_extension(output_image)
                    break
                except ValueError as e:
                    print(f"Erreur : {e}")

            secret_message = input("Entrez le message à cacher : ")
            try:
                hide_message(input_image, output_image, secret_message)
            except Exception as e:
                print(f"Erreur : {e}")

        elif choice == '2':
            while True:
                input_image = input("Entrez le chemin de l'image contenant le message (doit être .png, ex: 'output/image.png') : ")
                try:
                    validate_file_extension(input_image)
                    break
                except ValueError as e:
                    print(f"Erreur : {e}")

            try:
                reveal_message(input_image)
            except Exception as e:
                print(f"Erreur : {e}")

        elif choice == '3':
            print("Au revoir !")
            break
        else:
            print("Option invalide. Veuillez réessayer.")

if __name__ == "__main__":
    interactive_cli()
