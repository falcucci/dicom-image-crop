def secret() -> str:
    """
    This function returns a secret string from the library.

    Returns:
    str: A secret string.
    """
    from lib import SECRET
    return SECRET

def _hash(data: dict = {}, encrypted: bool = False) -> str:
    """
    Generate a token string.

    Returns:
    str: a token string generated from the lib.generate_token()
    function with a unique id.
    """
    import uuid   
    from lib import generate_token
    _id: str = str(uuid.uuid4())  
    return (
        generate_token(data.get("PatientID", _id))  
        if encrypted
        else _id
    )

def edges(image) -> str:
    """
    This function takes an image as input and returns
    a string describing the edges of the image.

    Parameters:
    image (str): a string representing the image

    Returns:
    str: a string describing the edges of the image
    """
    from lib import AutoCrop, open_
    binary_function  = open_(image)
    _bytes = binary_function(image)
    img_crop: AutoCrop = AutoCrop(_bytes)
    coordinates: tuple[int, int, int, int] = img_crop.new_image_coordinates()
    return "{}".format(coordinates)

def crop(image, output='', encrypted=True):
    """
    This function takes an image and an output
    directory as parameters and crops the image to a
    specified size.

    Parameters
    ----------
    image : str - The path of the image to be cropped.
    output : str, optional - The output directory to
    save the cropped image.
    """
    import os
    from PIL import Image
    from lib import AutoCrop, generate_token, OUT_JPG_FILES, open_
    output = output or OUT_JPG_FILES 
    binary_function = open_(image)
    _bytes, _objects = binary_function(image)
    img_crop: AutoCrop = AutoCrop(_bytes)
    coordinates: tuple[int, int, int, int] = img_crop.new_image_coordinates()
    if not os.path.exists(output):
        os.makedirs(output, exist_ok=True)

    print("Cropping area " + str(coordinates))
    cropped: Image.Image = _bytes.crop(coordinates) 
    encoded_id: str = _hash(_objects, encrypted)
    cropped.save('{0}/__{1}.jpg'.format(
        output,
        encoded_id
    ))

    print("Cropped image saved to {0}/__{1}.jpg".format(
        output or OUT_JPG_FILES,
        encoded_id
    ))

def crop_images(directory, output=''):
    """
    This function crops images from a specified
    directory and outputs them to the desired output
    directory.

    Parameters:
    directory (str): the directory of the images to be
    cropped
    output (str): the desired output directory for the
    cropped images (default is '')
    """
    import os 
    import glob 
    from lib import create_output_dir, OUT_JPG_FILES
    import multiprocessing
    cpu_count: int = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(cpu_count)
    create_output_dir(output or OUT_JPG_FILES)
    images: list[str] = glob.glob(os.path.join(directory, '*.DCM'))
    pool.map(crop, images)
    pool.close()   

if __name__ == '__main__':
    import fire
    fire.Fire({
        '--dir': crop_images,
        '--image': crop,
        '--edges': edges,
        '--secret': secret,
        '--token': _hash
    })
