from PIL import Image
import os
import pillow_heif


pillow_heif.register_heif_opener()

def removeFile(file):
    try:
        os.remove(file)
    except FileNotFoundError:
        print(f"Original file {file} not found. Skipping deletion.")

def convertHeicToJpg(heic_file, jpg_file):
  try:
    image = Image.open(heic_file)
    image = image.convert('RGB')
    image.save(jpg_file, format='jpeg')
    print(f"Converted {heic_file} to {jpg_file}")
    removeFile(heic_file)
    return jpg_file
  except Exception as e:
    print(f"Error converting {heic_file}: {e}")

def resizeImages(files, max_width=1920, prefix=''):
    # Loop through each file
    for file in files:
        # Check if it's an image file
        if file.lower().endswith((".jpg", ".jpeg", ".png", ".heic")):
            try:
                # Convet to jpg first if its .heic file
                if file.lower().endswith(".heic"):
                    jpg_file = os.path.splitext(file)[0] + ".jpg"
                    file = convertHeicToJpg(file, jpg_file)
                
                # Open the image
                image = Image.open(file)
                # Get original width and height
                width, height = image.size

                # Check if width is already less than max
                if width <= max_width:
                    continue  # Skip if already within limit

                # Calculate new height based on aspect ratio
                new_width = max_width
                new_height = int(height * (max_width / float(width)))

                # Generate new filename with prefix (optional)
                new_filename = os.path.join(os.path.dirname(file), str(prefix + file).lower())

                # Resize the image with LANCZOS resampling for antialiasing
                resized_image = image.resize((new_width, new_height), Image.LANCZOS)

                # Save the resized image with the same filename (optional: add prefix/suffix)
                resized_image.save(new_filename)

                # Remove the original file after successful resize
                removeFile(file)

                print(f"Resized {file} => {new_filename} to maximum width of {max_width}")
            except Exception as e:
                print(f"Error processing {file}: {e}")

    print("Finished resizing images!")


# Define the maximum width
MAX_WIDTH = int(input("Enter the max width: "))
PREFIX = str(input("Enter the file prefix: "))

# Get all files in the current directory
all_files = os.listdir()
resizeImages(all_files, MAX_WIDTH, PREFIX)
