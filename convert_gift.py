from PIL import Image
import os

def convert_gif_to_frames(gif_path, output_folder):
    gif = Image.open(gif_path)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for frame in range(gif.n_frames):
        gif.seek(frame)
        frame_image = gif.convert("RGBA")
        frame_image.save(f"{output_folder}/frame_{frame}.png")

convert_gif_to_frames("imagenes/zombie.gif", "frames")
