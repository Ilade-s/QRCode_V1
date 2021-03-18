"""
Module d'extraction de données d'un QRcode non masqué
"""

def get_raw_data(matrice) :
    """ Extrait les données brutes d'une matrice QR code V1 dans un entier
        Data_brutes = get_raw_data(QR_decode)
        entree
        ------
            QR_decode : matrice 21 X 21 d'un QR_code non masque
        Sortie
        ------
            Data_brutes : entier codé sur 22 octets 
            Remarque : en python les entiers ont une longueur non limitée.
    """
    mat = matrice  # copie de la matrice d'entree pour ne pas la modifier
    del mat[6]     # supprimer la ligne 6 qui ne contient pas de données
    powerbit = 1   # rang du bit en lecture  
    data = 0      
    # listes pour  scruter la matrice QR code
    x =[0, -1] 
    y =[0, -1, -2, -3]  
    sens = [ 1, 1, 1, -1, -1, -1, 1, 1, 1, -1, -1, -1, 1, 1, 1, 1, 1, -1, -1, -1, -1, -1]
    offsets = [[20, 19], [20, 15], [20, 11], 
               [18,  8], [18, 12], [18, 16],
               [16, 19], [16, 15], [16, 11], 
               [14,  8], [18, 12], [14, 16],
               [12, 19], [12, 15], [12, 11], [12, 7], [12, 3],
               [10,  0], [10,  4], [10,  8], [10, 12], [10, 16]
               ]
    # Pour chaque octet de la patrice           
    for octet in range(22) :
        offset = offsets[octet] # position de départ
        for j in y :        # scurtation en y
            for i in x :    # scrutayion en x
                bit = mat[offset[1]+j*sens[octet]] [offset[0]+i] # recupératio n du bit
                data = data + bit*powerbit  # ajout du bit à data à la position en court
                powerbit = powerbit<<1      # décalage à gauche pour bit suivant
    return data

def get_bits(raw_data,debut,n) :
    """ Extrait n bits à partir du bit debut d'un raw_data 
        bits = get_bits(raw_data,debut,n)
        entree
        ------
            raw_data : données brutes extraites d'unQR code V1
            debut : int 
                numéro du premier bit à extraire
            n : int
                nbre de bits à extraire
        Sortie
        ------
            bits : donnée extraite sous forme d'un entier 
    """
    # dans les données brutes les données sont stockées dans le sens MSB-LSB
    # il est nécessaire d'inverser les bits extraits du raw_data
    def reverse(x, n):
        result = 0
        for i in range(n):
            if (x >> i) & 1: result |= 1 << (n - 1 - i)
        return result
    
    data = raw_data>>debut # decalage à droite jusqu'au bit debut
    div = 1<<n             # pour récuperer n bits : reste de la division entiere par 2^n
    bits = data%div        # les bits à extraites sont dans bits
    return reverse(bits,n) # inversion pour avoir les bits dans le bon ordreLSB - MSB

if __name__ == "__main__":
    # Pour le test QR_code non masqué ASCII : data = 'Exemple'
    matrice = [            
    [0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1],
    [1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1],
    [0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1],
    [1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0],
    [1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1],
    [0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1],
    [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    [1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0],
    [0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0],
    [0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
    [1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1],
    [1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0],
    [1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0],
    [0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0],
    [1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0],
    [1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0]
    ]

    data = get_raw_data(matrice)
    print (data)
    print("codage : ", get_bits(data,0,4))
    nb = get_bits(data,4,8)
    print("nbre caractères : ", nb)
    for i in range(nb) :
        print(chr(get_bits(data,12+i*8,8)))