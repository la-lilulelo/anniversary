from PIL import Image, ImageDraw, ImageFont
import random
import os

def boxes_overlap(boxA, boxB):
    # box: (x1, y1, x2, y2)
    Ax1, Ay1, Ax2, Ay2 = boxA
    Bx1, By1, Bx2, By2 = boxB
    return (Ax1 < Bx2 and Ax2 > Bx1 and Ay1 < By2 and Ay2 > By1)

def generate_card(
    message_text="Happy Anniversary, my love! Here's to many more years together.",
    output_filename="card.png",
    width=800,
    height=600,
    pixel_art_count=20
):
    rows = message_text.count('\n')
    # Define some color choices for the background (monochromatic but pick one)
    color_choices = {
        "blue": "#00BFFF",
        "purple": "#9b59b6",
        "yellow": "#f1c40f",
        "pink": "#ff69b4",
        "seafoam": "#2ecc71"
    }

    chosen_color = random.choice(list(color_choices.values()))

    # Create a new image with the chosen background color
    img = Image.new("RGBA", (width, height), chosen_color + "FF")
    draw = ImageDraw.Draw(img)

    # Load a font
    # Make sure 'arial.ttf' or a similar font file is in the fonts/ directory
    font_choices = ['Dreamingland', 'Wasted-Vindey']
    font = random.choice(font_choices)
    
    font_path = os.path.join("fonts", font+".ttf")
    fontsize = 35
    if not os.path.isfile(font_path):
        # Fallback to a default PIL font if custom font not found
        font = ImageFont.load_default()
    else:
        font = ImageFont.truetype(font_path, size=fontsize)

    # Split the message by lines
    lines = message_text.split('\n')

    # Calculate maximum line width and total height
    line_widths = [draw.textlength(line, font=font) for line in lines]
    max_width = max(line_widths) if line_widths else 0

    # Approximate line height using font size
    # You can also use font.getmetrics() for a more precise calculation:
    # ascent, descent = font.getmetrics()
    # line_height = ascent + descent
    line_height = fontsize  
    total_height = line_height * len(lines)

    text_x = (width - max_width) // 2
    text_y = (height - total_height) // 2

    # Text bounding box
    text_box = (text_x, text_y, text_x + max_width, text_y + total_height)

    # Pixel art assets directory
    pixel_art_dir = "assets"
    # List pixel art files you have (make sure they are small pixel icons)
    pixel_art_files = ["animal-7764712_1280.png", "cookie-9181659_1280.png", "heart-7764716_1280.png", "leg-9181658_1280.png", "pixel-3316924_1280.png",
                       "pixel-cells-3699332_1280.png", "pixel-cells-3974182_1280.png", "raccoon-7723089_1280.png", "shooting-star-147722_1280.png", "star-152893_1280.png"]

    # Load pixel arts into memory
    scale_factor = 0.05
    pixel_arts = []
    for paf in pixel_art_files:
        fpath = os.path.join(pixel_art_dir, paf)
        if os.path.isfile(fpath):
            art = Image.open(fpath).convert("RGBA")
            new_width = int(art.width * scale_factor)
            new_height = int(art.height * scale_factor)
            resized_art = art.resize((new_width, new_height), Image.Resampling.NEAREST)
            pixel_arts.append(resized_art)

    max_attempts = 50

    for _ in range(pixel_art_count):
        if pixel_arts:
            art = random.choice(pixel_arts)
            art_w, art_h = art.width, art.height
            placed = False

            for attempt in range(max_attempts):
                max_x = width - art_w
                max_y = height - art_h

                if max_x < 0 or max_y < 0:
                    # art doesn't fit at all
                    break

                pos_x = random.randint(0, max_x)
                pos_y = random.randint(0, max_y)

                # Check if this placement overlaps text_box
                art_box = (pos_x, pos_y, pos_x + art_w, pos_y + art_h)
                if not boxes_overlap(art_box, text_box):
                    # Place the art here
                    img.alpha_composite(art, (pos_x, pos_y))
                    placed = True
                    break


     # Write the message text in a contrasting color (e.g., white)
    current_y = text_y
    for i, line in enumerate(lines):
        line_width = line_widths[i]
        line_x = (width - line_width) // 2
        draw.text((line_x, current_y), line, font=font, fill="black")
        current_y += line_height
    
    # Save the final image
    img.save(output_filename)

if __name__ == "__main__":
    # You can customize the text as you like
    
    message = "To my dearest Sunga,\nHappy anniversary!\nEvery single day with you is a treasure\nand feels just as intoxicating as our first moments\ntogether in Brisbane.\nI can't wait to spend the rest of my life with you.\nYou deserve so much, and I can't wait to see you\nachieve it all.\nAll my love,\nJames xxo"
    generate_card(message_text=message)
    print("Card generated: card.png")
