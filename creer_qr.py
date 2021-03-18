import qrcode

def CreerQR(Data,ImgName):
    """
    Paramètre d’entrée :

		Data : str
			Texte à encoder dans le QR Code
		ImgName : str
			Nom de fichier de l'image

	Paramètre de sortie :

		Aucun 
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=4,
        border=4,
    )
    qr.add_data(Data, 0)
    qr.make()

    img = qr.make_image(fill_color="black", back_color="white")

    img.save("Img_QR/"+ImgName+".png")

# Test
if __name__=='__main__':
    CreerQR("Test", "QR_Test")