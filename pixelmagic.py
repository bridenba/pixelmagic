"""

Functions for reading and transforming images.

CPE 101

Section: 3

Project 5

Name: Brandon Ridenbaugh

Cal Poly User: bridenba@calpoly.edu

"""
import sys


def main():
    """Main function for utiliing Pixelmagic.
    """
    user_input = sys.argv
    if len(user_input) < 3 or len(user_input) > 6:
        print("Usage: python pixelmagic.py <mode> <image>")
        return
    if 'decode' not in user_input and 'fade' not in user_input and 'denoise' not in user_input:
        print("Error: Invalid Mode")
        return

    if 'decode' in user_input:
        decoding_image = True
        user_input.remove('decode')
    else:
        decoding_image = False

    if 'fade' in user_input:
        fading_image = True
        user_input.remove('fade')
        if len(user_input) != 5:
            print("Usage: python pixelmagic.py fade <image> <row> <col> <radius>")
    else:
        fading_image = False

    if 'denoise' in user_input:
        denoising_image = True
        user_input.remove('denoise')
        if len(user_input) != 4:
            print("Usage: python pixelmagic.py denoise <image> <reach> <beta>")
    else:
        denoising_image = False

    try:
        image_data = read_image(user_input[1])
        header_info = image_data[0:3]
        del image_data[0:3]
        pixel_list = pixel_sep(image_data)
        if decoding_image:
            decoded_image = find_image(pixel_list)
            write_image('decoded.ppm', decoded_image, header_info)
        if fading_image:
            faded_image = fade_image(pixel_list, header_info[0],
                                     sys.argv[2], sys.argv[3], sys.argv[4])
            write_image('faded.ppm', faded_image, header_info)
        if denoising_image:
            pass
    except FileNotFoundError:
        print("Unable to open {0}".format(user_input[1]))


def read_image(file_name):
    """Helper function for reading a provided .ppm file.
    Args:
        file_name (string): The name of a .ppm file.
    Returns:
        image_data (list): A list of values read from the input file.
    """
    temp = open(file_name, 'r')
    temp.readline()

    image_data = []
    while True:
        line = temp.readline()
        if line == '':
            break
        line_data = line.split()
        for value in line_data:
            image_data.append(int(value))
    temp.close()
    return image_data


def write_image(file_name, filtered_pixels, header_info):
    """Helper function for writing a .ppm file of filtered pixels.
    Args:
        file_name (string): The desired name of the output file.
        filtered_pixels (list): A list of pixel values to be outputted.
        header_info (list): A list containing values for the height, width,
            and max RGB value of pixels.
    """
    temp = open(file_name, 'w')
    temp.write('P3\n')
    temp.write('{0} {1}\n'.format(header_info[0], header_info[1]))
    temp.write('{0}\n'.format(header_info[2]))
    for pixel_list in filtered_pixels:
        temp.write('{0:d} {1:d} {2:d}\n'.format(pixel_list[0], pixel_list[1], pixel_list[2]))
    temp.close()


def find_image(pixel_list):
    """Returns decoded pixels. Corresponds to the filter mode 'decode'.
    Args:
        pixel_list (list): A list of lists, each with containing 3 values for RGB designation.
    Returns:
        pixel_list (list): An updated pixel list with the decode filter applied.
    """
    for pixels in pixel_list:
        pixels[0] = pixels[0] * 10
        if pixels[0] > 255:
            pixels[0] = 255
        pixels[1] = pixels[0]
        pixels[2] = pixels[0]
    return pixel_list


def fade_image(pixel_list, width, row, col, radius):
    """Returns faded pixels. Corresponds to the filter mode 'fade'.
    Args:
        pixel_list (list): A list of lists, each with containing 3 values for RGB designation.
        width (int): An integer value for the width of the image in pixels.
        row (int): The y-value for the center of the fade.
        col (int): The x-value for the center of the fade.
        radius (int): The radius of the region to be faded.
    Returns:
        pixel_list (list): An updated pixel list with the fade filter applied.
    """
    for i, pixels in enumerate(pixel_list):
        pixel_y = i / width
        pixel_x = i % width
        dist_y = pixel_y - int(row)
        dist_x = pixel_x - int(col)
        distance = (dist_x ** 2 + dist_y ** 2) ** 0.5
        scale = (int(radius) - distance) / int(radius)
        if scale < 0.2:
            scale = 0.2
        pixels[0] = int(pixels[0] * scale)
        pixels[1] = int(pixels[1] * scale)
        pixels[2] = int(pixels[2] * scale)
    return pixel_list


def denoise_image(pixel_list, width, height, reach, beta):
    """Returns denoised pixels. Corresponds to the filter mode 'denoise'.
    Args:
        pixel_list (list): A list of lists, each with containing 3 values for RGB designation.
        width (int): An integer value for the width of the image in pixels.
        height (int): An integer value for the height of the image in pixels.
        reach (int): An integer value for the size of the denoise window.
        beta (float): A value to reference in determining if a pixel needs to be replaced.
    """
    for i, pixels in pixel_list:
        reach_x1 = 0
        reach_y1 = 0
        reach_x2 = 0


def pixel_sep(raw_pixels):
    """Separates a raw list of pixels into a list of lists containing data for individual pixels.
    Args:
        raw_pixels (list): A list of raw pixel data.
    Returns:
        pixel_list (list): A list of lists, each with containing 3 values for RGB designation.
    """
    i = 0
    index = 0
    pixel_list = []
    pixel_data = []
    for value in raw_pixels:
        index += 1
        i += 1
        if i <= 3:
            if index == (len(raw_pixels)):
                pixel_data.append(value)
                pixel_list.append(pixel_data)
            else:
                pixel_data.append(value)
        else:
            pixel_list.append(pixel_data)
            pixel_data = [value]
            i = 1
    return pixel_list


if __name__ == '__main__':
    main()
