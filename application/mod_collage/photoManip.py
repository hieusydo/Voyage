import cv2, numpy, urllib, boto3, os
from cStringIO import StringIO
from werkzeug import generate_password_hash
from flask import Flask
app = Flask(__name__)

# Generates a collage of New York given two image urls
# Returns the url to the uploaded collage
def generateCollage(url1, url2):
    # Load the urls as images
    image1 = loadImage(url1)
    image2 = loadImage(url2)

    print "generateCollage: loaded pics fine"

    dim = (654, 253)

    # Resize
    resized1 = cv2.resize(image1, dim, interpolation=cv2.INTER_AREA)
    resized2 = cv2.resize(image2, dim, interpolation=cv2.INTER_AREA)

    print "generateCollage: resized fine"   

    # Concatenate vertically (one on top of another)
    concat_file = numpy.concatenate((resized1, resized2), axis=0)
    concat_file = cv2.bitwise_not(concat_file)

    print "generateCollage: concatenate vertically (one on top of another)"

    # Read mask
    mask = getMask()

    print "generateCollage: got mask"

    # Apply mask
    masked_file = cv2.bitwise_and(concat_file, concat_file, mask=mask)
    masked_file = cv2.bitwise_not(masked_file)

    print "generateCollage: applied mask"

    # Encode final result
    result,encimg = cv2.imencode('.png',masked_file, [cv2.IMWRITE_PNG_COMPRESSION,0])
    if not result:
        print 'could not encode image!'
        return ''

    print "generateCollage: encoded img"

    finalimg = StringIO(encimg.tostring())

    # Upload image
    filename = generate_password_hash(url1+url2).split('$')[-1] + '.png'
    uploadImage(filename, finalimg)

    print "generateCollage: uploaded img to S3"

    # Return url
    return 'https://{}.s3.amazonaws.com/{}'.format(os.environ.get('AWS_S3_BUCKET'), filename)

# Downloads the image from the url and returns it as an image
def loadImage(url):
    resp = urllib.urlopen(url)
    image = numpy.asarray(bytearray(resp.read()), dtype="uint8")
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

# Reads the mask stored inside the application
def getMask():
    # Read the image
    img_str = ''
    with app.open_resource('ny_map.png') as f:
        img_str = f.read()

    # Decode the image
    nparr = numpy.fromstring(img_str, numpy.uint8)
    img_np = cv2.imdecode(nparr, 0)
    return img_np