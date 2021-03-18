"""
Module des fonctions pour décoder un QR code V1 (plus petit mode)
La fonction pricipale est lire_QRCode(QR_code)
Quand lancé en main, proposera une interface avec toutes les fonctionnalités du programme
-----------
Pour utlisation dans un autre programme, utiliser FuncLaunch(ImgName) pour un lancement sans interface ni texte
-----------
"""

from raw_data import get_bits,get_raw_data
from QR_ImgToMat import ImgToMat # Conversion image QR en matrice exploitable
from creer_qr import CreerQR # Création de QR code

def FuncLaunch(ImgName):
    """ Fonction qui permet de lancer le décodage d'un QR code à partir du nom de l'image :
            SANS INTERFACE // SANS TEXTE DE DEBUG

    Paramètre d’entrée :
    -------------------
        ImgName : str
            Nom de l'image (sans extension de fichier), doit être au format .png

    Paramètre de sortie :
    -------------------
        Value : str
            Texte décodé du QR_Code
    """
    QR_code = ImgToMat(ImgName, False)
    value = lire_QRCode(QR_code, False)

    return value

def mask(type) :
    """ Fonction qui génère la matrice de masque en fonction du type
    mat_mask = mask(type)

    Paramètre d’entrée :
    -------------------
        type : code compris entre 0 et 7
            type de masque à générer

    Paramètre de sortie :
    -------------------
        mat_mask : matrice 21X21
            la matrice générée dépend du type
    """
    mat_mask = [[0 for i in range(21)] for j in range(21)] 
    if type==0: # Damier fin
        for i in range(21):
            for j in range(21):
                if (i+j)%2 == 0:
                    mat_mask[j][i] = 1
    elif type==1: # Horizontales
        for i in range(21):
            for j in range(21):
                if j%2 == 0:
                    mat_mask[j][i] = 1
    elif type==2: # Verticales
        for i in range(21):
            for j in range(21):
                if i%3 == 0:
                    mat_mask[j][i] = 1
    elif type==3: # Diagonales   
        for i in range(21):
            for j in range(21):
                if (i+j)%3 == 0:
                    mat_mask[j][i] = 1
    elif type==4: # Damier gros carreaux
        for j in range(21):
            for i in range(21):
                if (j//2+i//3)%2 == 0:
                    mat_mask[j][i] = 1
    elif type==5: # Carreaux avec losanges
        for i in range(21):
            for j in range(21):
                if (i*j)%2+(i*j)%3 == 0:
                    mat_mask[j][i] = 1
    elif type==6: # Très noir
        for i in range(21):
            for j in range(21):
                if ((i*j)%3+i*j)%2 == 0:
                    mat_mask[j][i] = 1
    elif type==7: # Taches éclatées
        for i in range(21):
            for j in range(21):
                if ((i*j)%3+i+j)%2 == 0:
                    mat_mask[j][i] = 1
    return mat_mask

def format(QR_code) :
    """ fonction qui retourn le taux de correction appliqué et le type de masque appliqué au QR code
    (correction, masque) = format(QR_code)

    Paramètre d’entrée :
    -------------------
        QR_code : Matrice 21 X 21
        QR_code à décoder

    Paramètre de sortie :
    -------------------
        (correction, masque) : (int, int)
            correction : int    L 01
                                M 00
                                Q 11
                                H 10
            masque : int de 0 à 7
    """
    # mask = " 10 101 0000010010"

    masque = 0
    correction = 0

    # recherche en colonne 8, de l.16 à l.18 (masque) puis l.19 et l.20 (correction)
    for l in range(3): # Masque
        masque += QR_code[l+16][8]*(2**l)
    masque = masque^5 # Decodage XOR

    for l in range(2): # Correction
        correction += QR_code[l+19][8]*(2**l)
    correction = correction^2 # Decodage XOR

    return (correction, masque)
    
def decode(QR_code,QR_masque) :
    """Fonction qui applique le QR_masque au QR_code
    QR_Decode = decode(QR_code,masque)

    Paramètre d’entrée :
    ------------------
        QR_code : Matrice 21 X 21
            QR_code à décoder
        masque : Matrice 21 X 21
            masque à appliquer au QR_code

    Paramètre de sortie :
    --------------------
        QR_Decode : Matrice 21 X 21
    """
    QR_Decode = QR_code
    # Boucles XOR
    # Haut
    for l in range(8):
        for c in range(9,13):
           QR_Decode[l][c] = QR_code[l][c]^QR_masque[l][c] 
    # Milieu
    for l in range(9,13):
        for c in range(21):
           QR_Decode[l][c] = QR_code[l][c]^QR_masque[l][c] 
    # Bas
    for l in range(13,21):
        for c in range(9,21):
           QR_Decode[l][c] = QR_code[l][c]^QR_masque[l][c] 

    return QR_Decode

def get_mode(raw_data) :
    """
    (mode,nb_car) = get_mode(Raw_Data)

    Paramètre d’entrée :
    ------------------
        Raw_Data : Données brutes issue d’un Qrcode vesrion 1.
            Raw_Data : int contenant les données brutes du QR code
                mode de codage sur 4 bits,
                le nombre de caractères codés sur :
                    8 bits pour l'ASCII,
                    9 bits pour l'alphanumérique,
                    10 bits pour le numérique

    Paramètre de sortie :
    --------------------
        (mode, nb_car) : (int, int)
            Mode : int 
                1 : Numérique
                2 : Alphanumérique
                4 : ASCII
            nb_car : int
                Nombre de caractères encodés.
    """
    mode = get_bits(raw_data,0,4)
    # Recherche nombre caractères en fonction de l'encodage
    if mode==1:
        nb_car = get_bits(raw_data,4,10)
    elif mode==2:
        nb_car = get_bits(raw_data,4,9)
    elif mode==4:
        nb_car = get_bits(raw_data,4,8)
    else:
        nb_car = 0
    #mode = 2
    #nb_car = 2
    return (mode,nb_car)

def lire_ASCII(raw_data,nb_car) :
    """
    Paramètre d’entrée :
    --------------------
        Raw_Data : Données brutes issue d’un Qrcode vesrion 1.
        nb_car : int
            Nombre de caractères à lire

    Paramètre de sortie :
    --------------------
        message : string
            message contenu dans le QR_code
    """
    message = ""
    for i in range(nb_car):
        message += chr(get_bits(raw_data,12+i*8,8))
    return message

def lire_AlphaNum(raw_data,nb_car):
    """
    Paramètre d’entrée :
    --------------------
        Raw_Data : Données brutes issue d’un Qrcode vesrion 1.
        nb_car : int
            Nombre de caractères à lire

    Paramètre de sortie :
    --------------------
        message : str
            message contenu dans le QR_code
    """
    dict_chr = {
        0:"0",
        1:"1",
        2:"2",
        3:"3",
        4:"4",
        5:"5",
        6:"6",
        7:"7",
        8:"8",
        9:"9",
        10:"A",
        11:"B",
        12:"C",
        13:"D",
        14:"E",
        15:"F",
        16:"G",
        17:"H",
        18:"I",
        19:"J",
        20:"K",
        21:"L",
        22:"M",
        23:"N",
        24:"O",
        25:"P",
        26:"Q",
        27:"R",
        28:"S",
        29:"T",
        30:"U",
        31:"V",
        32:"W",
        33:"X",
        34:"Y",
        35:"Z",
        36:" ",
        37:"$",
        38:"%",
        39:"*",
        40:"+",
        41:"-",
        42:".",
        43:"/",
        44:":",
    }
    # Technique :
    # 45*a + b = int(bin) sur 11 bits
    # Donc a = bin/45 arrondi à 0
    # et b = bin%45 (reste)

    message = ""
    
    if nb_car%2==0: # Tous 11 bits (pair)
        passe = 0
        while nb_car>len(message):
            valueBin = get_bits(raw_data,13+passe*11,11)
            message += dict_chr[int(valueBin/45)]\
                        +dict_chr[valueBin%45]
            passe+=1

    else: # Dernier caractère sur 6 bits (impair)
        # Caractères par paire sur 11 bits
        passe = 0
        while nb_car-len(message)>=2:
            valueBin = get_bits(raw_data,13+passe*11,11)
            message += dict_chr[int(valueBin/45)]\
                        +dict_chr[valueBin%45]
            passe+=1
        # Dernier caractère
        message += dict_chr[get_bits(raw_data,13+passe*11,6)]
    return message

def lire_Num(raw_data,nb_car):
    """
    Paramètre d’entrée :
    --------------------
        Raw_Data : Données brutes issue d’un Qrcode version 1.
        nb_car : int
            Nombre de caractères à lire

    Paramètre de sortie :
    --------------------
        message : str
            message contenu dans le QR_code
    """
    message = ""
    if nb_car%3==0: # Uniquement groupes de 3 chiffres (10 bits)
        nGrp = int(nb_car/3)
        for i in range(nGrp):    
            message += str(get_bits(raw_data,14+i*10,10))
        if len(message)<nb_car:
            message = "0"+message

    else: # Dernier groupe en 4 bits (1 chiffre) ou 7 bits (2 chiffres)
        nGrpDe3 = int(nb_car/3)
        nCaracDernierGrp = nb_car%3
        nBitsDernierGrp = 1+nCaracDernierGrp*3
        for i in range(nGrpDe3): 
            Data = str(get_bits(raw_data,14+i*10,10))
            message += Data
        message += str(get_bits(raw_data,14+nGrpDe3*10,nBitsDernierGrp))
        if len(message)<nb_car:
            message = "0"+message
            
    return message

def lire_QRCode(QR_code, Debug=True) :
    CorrDict = {0:"M",1:"L",3:"Q",2:"H"}
    message = ""
    # Recherche format
    (correction, masque) = format(QR_code)
    # Création masque    
    masque_mat = mask(masque)
    # Décodage avec masque 
    QR_decode = decode(QR_code, masque_mat)
    # Récupération données QR code
    Raw_Data = get_raw_data(QR_decode)
    # Récupération encodage
    (mode,nb_car) = get_mode(Raw_Data)
    # Choix def en fonction de l'encodage
    if mode==1: # Numérique
        message = lire_Num(Raw_Data, nb_car)
    elif mode==2: # Alphanumérique
        message = lire_AlphaNum(Raw_Data, nb_car)
    elif mode==4: # ASCII
        message = lire_ASCII(Raw_Data, nb_car)
    else: # mode incorrect
        print("mode incorrect :",mode)
    if Debug:
        print("============================================================================")
        print("\t\tDEBUG")
        print("Niveau de correction :",CorrDict[correction])
        print("Masque :",masque)
        print("Nombre de caractères :",nb_car)
        print("Encodage :",mode)
        print("\t\tDEBUG")
        print("============================================================================")
    return message


if __name__ == "__main__": 
    print("============================================================================")
    print("Bienvenue dans mon programme de decodage d'un QR Code")
    print("Vous pouvez soit :")
    print('\t1 : Decoder un exemple de QR Code (texte : "Exemple")')
    print("\t2 : Decoder un QR Code à partie d'une image de votre choix")
    print("\t    (format png, à mettre dans le dossier 'Img_QR')")
    print("\t3 : Créer un QR code (stocké dans le dossier 'Img_QR') : EXPERIMENTAL")
    print("\t    (format png, encodage non contrôlable, choisira le plus optimal, nom en QR_xxx.png)")
    print("============================================================================")
    print("\a")
    Choix = input("Choix (1, 2 ou 3) : ")
    if Choix=="2": # Décodage à partir d'une image
        ImgName = "QR_"+input("\tNom de l'image (sans extension de fichier, seulement le texte inconnu : QR_xxx.png) : ")
        print("============================================================================")
        print("\t\tIMAGE")
        QR_code = ImgToMat(ImgName)
        print("\t\tIMAGE")
        msg = lire_QRCode(QR_code)
        print("Message :",msg)
    elif Choix=="3": # Création QR Code
        print("============================================================================")
        print("Limite de caractères :")
        print("\tASCII : 11 caractères")
        print("\tAlphanumérique : 16 caractères")
        print("\tNumérique : 27 caractères")
        print("============================================================================")
        Data = input("\tTexte à encoder : ")
        ImgName = "QR_"+input("\tNom de l'image du QR code (sans extension de fichier) (Laisser vide pour nom=data) : ")
        if ImgName=="QR_":
            ImgName += Data
        CreerQR(Data, ImgName)
        print("\t\tFAIT")
    else: # Décodage d'un exemple de QR Code
        QR_code = [ # ASCII "Exemple"
            [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1],
            [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1],
            [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1],
            [0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1],
            [1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1],
            [1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0],
            [1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1],
            [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0],
            [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0],
            [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0],
            ]
        msg = lire_QRCode(QR_code)
        print("Message :",msg)
