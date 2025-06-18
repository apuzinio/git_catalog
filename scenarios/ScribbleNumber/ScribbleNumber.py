import random
import argparse
from PIL import Image, ImageDraw, ImageFont

def create_handwritten_number(number, image_size=(64, 64), font_name=None, font_size=24, draw_offset_fixed=(0,0), draw_offset_rand=(0,0), draw_rotate_rand=0):
    """
    Creates an image of a handwritten-style number.

    Args:
        number (int): The number to draw.
        image_size (tuple): The size of the output image (width, height).
        font_size (int): The size of the font.
        font_path (str, optional): Path to a specific font file. If None, uses a default.

    Returns:
        PIL.Image.Image: The image of the handwritten number.
    """
    image = Image.new("L", image_size, "white")
    draw = ImageDraw.Draw(image)

    if font_name:
        font = ImageFont.truetype(font_name, font_size)
    else:
        font = ImageFont.load_default()

    # Get the bounding box of the text
    bbox = draw.textbbox((0, 0), str(number), font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Calculate position with some random variation
    x = (int(0.5*(image_size[0] - text_width)) +
         draw_offset_fixed[0] +
         random.randint(-draw_offset_rand[0], draw_offset_rand[0]))
    y = (int(0.5*(image_size[1] - text_height)) +
         draw_offset_fixed[1] +
         random.randint(-draw_offset_rand[1], draw_offset_rand[1]))
    
    # Draw the text with slight variation in position
    draw.text((x, y), str(number), font=font, fill="black")
    angle = random.randint(-draw_rotate_rand, draw_rotate_rand)
    rotated_image = image.rotate(angle, fillcolor="white")                  
    
    return (rotated_image, number)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="python ScribbleNumber.py --font_name=None --font_size=24 --draw_offset_fixed=(0,-10) --draw_offset_rand=(5,5) --draw_rotate_rand=20)")
    parser.add_argument('--font_name', type=str, default=None, help="Chk for avaiable fonts in /Library/Fonts/, /System/Library/Fonts/")
    parser.add_argument('--font_size', type=int, default=24)
    parser.add_argument('--draw_offset_fixed_x', type=int, default=0)
    parser.add_argument('--draw_offset_fixed_y', type=int, default=0)
    parser.add_argument('--draw_offset_rand_x', type=int, default=0)
    parser.add_argument('--draw_offset_rand_y', type=int, default=0)
    parser.add_argument('--draw_rotate_rand', type=int, default=0)
    args = parser.parse_args()
    print(args)
    print("ScribbleNumber: labels will be stored in labels.txt")
    label_fd = open('labels.txt', 'w')
    for i in range(10):
        print(f"ScribbleNumber: Working on handwritten_{i}.png...")
        (image, number) = create_handwritten_number(
            random.randint(0, 9), 
            font_name= args.font_name,
            font_size=args.font_size,
            draw_offset_fixed=(args.draw_offset_fixed_x,args.draw_offset_fixed_y),
            draw_offset_rand=(args.draw_offset_rand_x,args.draw_offset_rand_y),
            draw_rotate_rand=args.draw_rotate_rand)
        image.save(f"handwritten_{i}.png")
        label_fd.write(f"{number}\n")
    label_fd.close()