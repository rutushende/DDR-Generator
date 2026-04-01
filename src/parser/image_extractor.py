import fitz
import os

def extract_images(pdf_path, output_folder="outputs/images"):
    os.makedirs(output_folder, exist_ok=True)
    doc = fitz.open(pdf_path)

    image_paths = []

    for page_index in range(len(doc)):
        page = doc[page_index]
        images = page.get_images(full=True)

        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]

            filename = f"img_{page_index}_{img_index}.png"
            path = os.path.join(output_folder, filename)

            with open(path, "wb") as f:
                f.write(image_bytes)

            image_paths.append(path)

    return image_paths
