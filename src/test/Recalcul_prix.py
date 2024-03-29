def arrondi_au_mutilple(x, a=0.05):
    return round(round(x / a) * a,2)

def recalcul_prix(prix):
    if prix < 0.30:
        return {"Coutant": round(prix,2),
                "Exté": arrondi_au_mutilple(prix + 0.3) ,
                "CETEN": arrondi_au_mutilple(prix + 0.15) ,
                 "Staff": arrondi_au_mutilple(prix + 0.05) ,
                 "Privilège": arrondi_au_mutilple(prix + 0.05) ,
                 "Menu": arrondi_au_mutilple(prix + 0.1) ,}
    elif prix >= 0.30 and prix < 1.3:
        return {"Coutant": round(prix,2),
                "Exté": arrondi_au_mutilple(prix * 2),
                "CETEN": arrondi_au_mutilple(prix * 1.4),
                 "Staff": arrondi_au_mutilple(prix * 1.25),
                 "Privilège": arrondi_au_mutilple(prix * 1.2),
                 "Menu": arrondi_au_mutilple(prix * 1.3),}
    elif prix >= 1.3 and prix <= 3:
        return {"Coutant": round(prix,2),
                "Exté": arrondi_au_mutilple(prix * 1.5) ,
                "CETEN": arrondi_au_mutilple(prix * 1.25),
                 "Staff": arrondi_au_mutilple(prix * 1.15),
                 "Privilège": arrondi_au_mutilple(prix * 1.1),
                 "Menu": arrondi_au_mutilple(prix * 1.2),}
    elif prix >= 3:
        return {"Coutant": round(prix,2),
                "Exté": arrondi_au_mutilple(prix * 1.3),
                "CETEN": arrondi_au_mutilple(prix * 1.15) ,
                 "Staff": arrondi_au_mutilple(prix * 1.1) ,
                 "Privilège": arrondi_au_mutilple(prix * 1.1) ,
                 "Menu": arrondi_au_mutilple(prix * 1.125) ,}

if __name__ == '__main__':
    print(recalcul_prix(0.57584).items())
    #i = 0.0
    # while i < 3:
    #     round(i, 2)
    #     for s in recalcul_prix(i).values():
    #         if len(str(s)) > 4:
    #             print(i, s)
    #     i += 0.01