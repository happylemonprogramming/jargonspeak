import qrcode

def QR_Code(data, filepath):
  # Generate QR Code
  img = qrcode.make(data)
  imgpath = filepath
  img.save(imgpath)

  # Read the image file as binary data
  with open(imgpath, 'rb') as f:
      image_data = f.read()
  return image_data