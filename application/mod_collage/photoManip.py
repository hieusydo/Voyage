import cv2, numpy, urllib, boto3, os
from werkzeug import generate_password_hash

# Generates a collage of New York given two image urls
# Returns the url to the uploaded collage
def generateCollage(url1, url2):
    # Load the urls as images
    image1 = loadImage(url1)
    image2 = loadImage(url2)

    dim = (654, 253)

    # Resize
    resized1 = cv2.resize(image1, dim, interpolation=cv2.INTER_AREA)
    resized2 = cv2.resize(image2, dim, interpolation=cv2.INTER_AREA)

    # Concatenate vertically (one on top of another)
    concat_file = numpy.concatenate((resized1, resized2), axis=0)

    # Read mask
    mask = cv2.imread("ny_map.png",0)

    # Apply mask
    masked_file = cv2.bitwise_and(concat_file, concat_file, mask=mask)

    # Upload image
    filename = generate_password_hash(url1+url2).split('$')[-1] + '.png'
    uploadImage(filename, masked_file)

    # Return url
    return 'https://{}.s3.amazonaws.com/{}'.format(os.environ.get('AWS_S3_BUCKET'), filename)

# Downloads the image from the url and returns it as an image
def loadImage(url):
    resp = urllib.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    return image

# Uploads an image under the given filename
def uploadImage(filename, image):
    try:
        s3 = boto3.client('s3')
        s3.upload_fileobj(image, os.environ.get('AWS_S3_BUCKET'), filename, ExtraArgs={
            "ContentType": 'image/png'
        })
    except Exception as e:
        print e