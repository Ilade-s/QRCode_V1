# QRCode_V1-Reader-

La fonction pricipale est lire_QRCode(QR_code)
-----------

Quand lancé en main, proposera une interface avec toutes les fonctionnalités du programme :
-----------
    - Lire un QR code V1 à partir d'une image (ASCII, Alphanumérique et Numérique)
    - Lire un 'exemple' de QR Code V1 (test programme)
    - Créer un QR Code V1

Assurez-vous d'avoir toutes les dépandances dans le même dossier que le programme :
-----------
    - QR_ImgToMat.py (lecture d'image vers matrice : peut être utilisé de manière indépendante)
    - raw_data.py (extraction données QR Code)
    - creer_qr.py (création de QR Code V1)
    - Un dossier Img_QR dans le même dossier (stockage des images de QR Code)

Pour utilisation dans un autre programme, utiliser FuncLaunch(ImgName) pour un lancement sans interface ni texte
-----------