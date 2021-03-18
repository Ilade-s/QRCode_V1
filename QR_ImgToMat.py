from PIL import Image # Gestion d'image

def ImgToMat(ImgName, Debug=True):
    """
    Paramètre d’entrée :
        ImgName : str
            Nom de l'image (stockée dans le dossier "Img_QR") sans l'extension de fichier (.png obligatoire)

	Paramètre de sortie :

		QR_Code : Matrice 21 X 21
			Matrice représentant le Code QR
    """
    img = Image.open(str("Img_QR/"+ImgName+".png"))
    img = img.convert('1')
    (xImg, yImg) = img.size
    # Recherche taille d'un pixel
    ModulePx = TaillePx(xImg)
    
    QuietZone = ModulePx*4 # 4X
    # Rognage pour étude QR_Code
    img = img.crop((QuietZone, QuietZone, xImg-QuietZone, yImg-QuietZone))
    (xImg, yImg) = img.size # Nouvelles dimensions de l'image
    # Remplissage Matrice (list comprehension)
    QR_Code = [[1 if img.getpixel((x*ModulePx+ModulePx/2,y*ModulePx+ModulePx/2))==0 else 0 for x in range(21)] for y in range(21)] 
    if Debug:
        print("x length :",xImg,"// y length :" ,yImg)
        print("Taille module :",ModulePx,"px")
    return QR_Code

def TaillePx(xImg):
    """
    Paramètre d’entrée :

        xImg : Int
            Longueur sur l'axe x de l'image (en pixels)

	Paramètre de sortie :

		ModulePx : Int
			Longueur d'un coté d'un module du QR Code (en pixels)
    """
    iMpx = 1
    iTotalpx = iMpx*21+iMpx*8

    while iTotalpx<xImg:
        iMpx+=1
        iTotalpx = iMpx*21+iMpx*8

    ModulePx = iMpx
    return(ModulePx)
        
# Test
if __name__=='__main__':
    # Demande de l'image de QR Code à étudier
    Name = input("Nom de l'image (sans extension de fichier): ")
    if Name=="": Name = "QR_Exemple"
    # Conversion en matrice
    QR_Code = ImgToMat(Name)
    for i in range(21):
        print(QR_Code[i])

