from google.cloud import vision
from PIL import Image, ImageDraw, ImageFont
# C:\Users\clayt\AppData\Local\Google\Cloud SDK>gcloud auth application-default login
# Credentials saved to file: [C:\Users\clayt\AppData\Roaming\gcloud\application_default_credentials.json]
# These credentials will be used by any library that requests Application Default Credentials (ADC).
# Quota project "blissful-sled-405206" was added to ADC which can be used by Google client libraries for billing and quota. Note that some services may still bill the project owning the resource.
def textdetect(input_image_path):
    # Detect document features in the image
    client = vision.ImageAnnotatorClient()
    with open(input_image_path, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)

    # Initialize lists for function return
    words = []
    x_boundary = []
    y_boundary = []

    # Iterate through the response to find and replace the specified word
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    word_text = "".join([symbol.text for symbol in word.symbols])

                    # Extract bounding box vertices
                    vertices = word.bounding_box.vertices
                    x_coordinates = [vertex.x for vertex in vertices]
                    y_coordinates = [vertex.y for vertex in vertices]

                    # Add work and coorindates for future use
                    words.append(word_text)
                    x_boundary.append(x_coordinates)
                    y_boundary.append(y_coordinates)
    return words, x_boundary, y_boundary

# def textreplace(noTextImage, outputImage, words, bounds):
#     # Open the image using Pillow
#     img = Image.open(noTextImage)
#     draw = ImageDraw.Draw(img)

#     for i, word in enumerate(words):
#         # Check if the bounds list has enough elements for the given index i
#         if i < len(bounds):
#             # Get the boundary box vertices for the current word
#             x_coordinates, y_coordinates = zip(*bounds[i])

#             # Calculate the box height
#             box_height = y_coordinates[2] - y_coordinates[0]

#             # Load a font and set the font size based on the box height
#             font_size = int(box_height * 0.8)  # Adjust the factor as needed
#             font = ImageFont.truetype(".fonts/YuGothR.ttc", font_size)

#             replacement_word = words[i]

#             # Draw the replacement word with a border
#             border_size = int(font_size*(5/30))  # Adjust this value for the desired border size
#             for offset in range(1, border_size + 1):
#                 draw.text((x_coordinates[0] - offset, y_coordinates[0]), replacement_word, font=font, fill="black")
#                 draw.text((x_coordinates[0] + offset, y_coordinates[0]), replacement_word, font=font, fill="black")
#                 draw.text((x_coordinates[0], y_coordinates[0] - offset), replacement_word, font=font, fill="black")
#                 draw.text((x_coordinates[0], y_coordinates[0] + offset), replacement_word, font=font, fill="black")

#             draw.text((x_coordinates[0], y_coordinates[0]), replacement_word, font=font, fill="white")
#         else:
#             print(f"Warning: Not enough bounds provided for word '{word}' (index {i}). Skipping replacement.")

#     # Convert the image to RGB mode before saving as JPEG
#     img = img.convert("RGB")

#     # Save the modified image
#     img.save(outputImage)

def textreplace2(noTextImage, outputImage, words, bounds):
    # Open the image using Pillow
    img = Image.open(noTextImage)
    draw = ImageDraw.Draw(img)

    for i, word in enumerate(words):
        # Check if the bounds list has enough elements for the given index i
        if i < len(bounds):
            # Get the boundary box vertices for the current word
            x_coordinates, y_coordinates = zip(*bounds[i])

            # Calculate the box height
            box_height = y_coordinates[2] - y_coordinates[0]

            # Load a font and set the font size based on the box height
            font_size = int(box_height * 0.8)  # Adjust the factor as needed
            font = ImageFont.truetype(".fonts/YuGothR.ttc", font_size)

            replacement_word = words[i]

            # Define the outline size
            outline_size = int(font_size * 0.1)  # Adjust this value for the desired outline size

            # Draw the replacement word with a border
            for offset in range(1, outline_size + 1):
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        draw.text((x_coordinates[0] + dx * offset, y_coordinates[0] + dy * offset),
                                  replacement_word, font=font, fill="white")

            draw.text((x_coordinates[0], y_coordinates[0]), replacement_word, font=font, fill="black")
        else:
            print(f"Warning: Not enough bounds provided for word '{word}' (index {i}). Skipping replacement.")

    # Convert the image to RGB mode before saving as JPEG
    img = img.convert("RGB")

    # Save the modified image
    img.save(outputImage)


if __name__ == '__main__':
    # Example usage
    input_image_path = r"C:\Users\clayt\Downloads\Patrick-Mom-come-pick-me-up-Im-scared.png"
    # input_image_path = r"C:\Users\clayt\Pictures\Screenshots\Screenshot 2023-03-26 231819.png"
    # noTextImage = 'result.png'
    # translated_words = ['Do','you','know','the','muffin','man,','the','one','from','Crystal','Lantern?']
    output = textdetect(input_image_path)
    print(output)
    # TODO: add thresholding and grayscale for image processing to get rid of artifacts
    # Convert the frame to grayscale
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # # Apply thresholding to obtain a binary image
    # _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

    # textreplace(noTextImage,'hooray.jpg',output[0],translated_words,output[1],output[2])