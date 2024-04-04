def arrondi_au_mutilple(x, a=5):
    return int((int(x) + int(a/2)) / a) * a

def recalcul_prix_centimes(prix: int):
    if prix < 30:
        return {"Coutant": prix,
                "Exté": arrondi_au_mutilple(prix) + 20,
                "CETEN": arrondi_au_mutilple(prix) + 10,
                 "Staff": arrondi_au_mutilple(prix) + 5,
                 "Privilège": arrondi_au_mutilple(prix) + 5 ,
                 "Menu": arrondi_au_mutilple(prix) + 10,}
    elif prix >= 30 and prix < 130:
        return {"Coutant": prix,
                "Exté": arrondi_au_mutilple((prix * 3) / 2),
                "CETEN": arrondi_au_mutilple((prix * 113) / 100),
                 "Staff": arrondi_au_mutilple((prix * 108) / 100),
                 "Privilège": arrondi_au_mutilple((prix * 11) / 10),
                 "Menu": arrondi_au_mutilple((prix * 13) / 10),}
    elif prix >= 130 and prix <= 300:
        return {"Coutant": prix,
                "Exté": arrondi_au_mutilple(prix * 1.4) ,
                "CETEN": arrondi_au_mutilple(prix * 1.1),
                 "Staff": arrondi_au_mutilple(prix * 1.08),
                 "Privilège": arrondi_au_mutilple(prix * 1.1),
                 "Menu": arrondi_au_mutilple(prix * 1.2),}
    elif prix >= 300:
        return {"Coutant": prix,
                "Exté": arrondi_au_mutilple((prix * 125) / 100),
                "CETEN": arrondi_au_mutilple(prix * 1.1),
                 "Staff": arrondi_au_mutilple((prix * 105)/ 100),
                 "Privilège": arrondi_au_mutilple(prix * 1.1),
                 "Menu": arrondi_au_mutilple((prix * 1125) / 1000),}

if __name__ == '__main__':
    print(recalcul_prix_centimes(int(3199*0.9)/50).items())
    #i = 0.0
    # while i < 3:
    #     round(i, 2)
    #     for s in recalcul_prix(i).values():
    #         if len(str(s)) > 4:
    #             print(i, s)
    #     i += 0.01