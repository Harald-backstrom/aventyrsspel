import random as rand

class spelar_skapare:
    def __init__(self, hp, styrka,inventory,level,exp):
        self.hp = hp
        self.styrka = styrka
        self.inventory = inventory
        self.level = level
        self.exp = exp

class monster_skapare:
    def __init__(self, hp, styrka, namn):
        self.namn = namn
        self.hp = hp
        self.styrka = styrka


class föremål:
    def __init__(self, namn, styrka_bonus):
        self.namn = namn
        self.styrka_bonus = styrka_bonus

def level_up(hjälte):
    hjälte.styrka += 1
    hjälte.level += 1
    print(f"Du har gått upp till level {hjälte.level} och din styrka har ökat! Din styrka är nu {hjälte.styrka}.")


def strid(hjälte, aktivt_vapen):
    mosnter_lista = [
        monster_skapare(rand.randint(3, 7) + hjälte.level, rand.randint(3, 6) * hjälte.level, "skelett"),
        monster_skapare(rand.randint(5, 10) + hjälte.level, rand.randint(5, 10) * hjälte.level, "goblin"),
        monster_skapare(rand.randint(8, 15) + hjälte.level, rand.randint(8, 15) * hjälte.level, "jätte"),
        monster_skapare(rand.randint(12, 20) + hjälte.level, rand.randint(12, 20) * hjälte.level, "drake")
    ]
    monster = rand.choice(mosnter_lista)
    total_styrka = hjälte.styrka

    if aktivt_vapen:
        total_styrka += aktivt_vapen.styrka_bonus

    print(f"du möter en {monster.namn} som har {monster.styrka} styrka")
    print(f"du har {hjälte.styrka} styrka och {hjälte.hp} hp kvar och du får {total_styrka - hjälte.styrka} styrka från ditt vapen")
    if total_styrka >= monster.styrka:
        print("du vann, du fick 2 xp")
        hjälte.exp +=2
        if hjälte.exp >= 10:
            level_up(hjälte)
            hjälte.exp -= 10
    else:
        print("du förlorade")
        hjälte.hp -=1
    return hjälte

def rum_med_kista(inventory):
    if len(inventory) < 7:
        föremål = skapa_föremål()
        print("du kom in i ett rum med en kista ")
        print(f"innuti kistan hittar du {föremål.namn}")
        inventory.append(föremål)
    else:
        print("ditt invetory är fullt, du fick inget")
    return inventory

def slumpad_labyrint(storlek):
    labyrint_karta = []
    for _ in range(storlek):
        row = []
        for _ in range(storlek):
            cell = rand.choice(["Väg", "Fälla"])
            row.append(cell)
        labyrint_karta.append(row)
    labyrint_karta[0][0] = "Start"
    labyrint_karta[storlek - 1][storlek - 1] = "Mål"
    return labyrint_karta

def labyrint(hjälte):
    storlek = 4
    labyrint_karta = slumpad_labyrint(storlek)

    nuvarande_position = [0, 0]
    mål_position = [storlek - 1, storlek - 1]

    print("Välkommen till labyrinten! Din uppgift är att nå målet utan att hamna i fällorna.")
    print("Använd 'vänster', 'höger', 'upp' och 'ner' för att navigera.")

    while True:
        for i in range(storlek):
            for j in range(storlek):
                if nuvarande_position == [i, j]:
                    print("P", end=' ')
                else:
                    print("-", end=' ')
            print()


        if nuvarande_position == mål_position:
            print("Grattis! Du har nått målet och du fick 2 xp")
            hjälte.exp +=2
            return hjälte

        val = input("Välj riktning ('vänster', 'höger', 'upp', 'ner'): ")

        if val == 'vänster':
            if nuvarande_position[1] > 0:
                nuvarande_position[1] -= 1
            else:
                print("Du kan inte gå åt vänster här.")
        elif val == 'höger':
            if nuvarande_position[1] < storlek - 1:
                nuvarande_position[1] += 1
            else:
                print("Du kan inte gå åt höger här.")
        elif val == 'upp':
            if nuvarande_position[0] > 0:
                nuvarande_position[0] -= 1
            else:
                print("Du kan inte gå upp här.")
        elif val == 'ner':
            if nuvarande_position[0] < storlek - 1:
                nuvarande_position[0] += 1
            else:
                print("Du kan inte gå ner här.")
        else:
            print("Ogiltigt kommando. Försök igen.")

        if labyrint_karta[nuvarande_position[0]][nuvarande_position[1]] == "Fälla":
            print("Du har hamnat i en fälla! du förlorar 1 hp")
            hjälte.hp -=1
            return hjälte
       
def skapa_föremål():
    föremål_lista = ("svärd","yxa","sten","katana")
    return föremål(rand.choice(föremål_lista), rand.randint(1,4))


def main():
    inventory = []
    hjälte = spelar_skapare(10, rand.randint(3, 6), inventory, 1, 0)
    aktivt_vapen = []


    while hjälte.hp >= 0:
        print(
            """
            Vad vill du göra?
            1. Gå genom dörr
            2. Kolla inventory
            3. Kolla stats
            """
        )


        val = input("")


        if val == "1":
            if rand.randint(0, 2) == 0:
                    hjälte = strid(hjälte, aktivt_vapen)
            elif rand.randint(0, 2) == 1:
                inventory = rum_med_kista(inventory)
            elif rand.randint(0, 2) == 2:
                labyrint(hjälte)
            else:
                print("Det var inget i rummet, din lilla råtta")
        elif val == "2":
            print("Ditt inventory:")
            for i, sak in enumerate(inventory):
                print(f"{i + 1}. {sak.namn} som ger dig {sak.styrka_bonus} styrka")


            vald_sak = input("""Välj ett vapen att hålla i (skriv numret bredvid vapnet eller '0' för att återgå),
eller 'radera' för att ta bort ett föremål: """)


            if vald_sak.isdigit() and 0 < int(vald_sak) <= len(inventory):
                aktivt_vapen = inventory[int(vald_sak) - 1]
                print(f"Du håller nu i {aktivt_vapen.namn}")
            elif vald_sak == '0':
                aktivt_vapen = None
                print("Du håller inte i något vapen.")
            elif vald_sak.lower() == 'radera':
                index_to_remove = input("Ange numret bredvid föremålet du vill ta bort: ")
                if index_to_remove.isdigit() and 0 < int(index_to_remove) <= len(inventory):
                    removed_item = inventory.pop(int(index_to_remove) - 1)
                    print(f"{removed_item.namn} har tagits bort från ditt inventory.")
                else:
                    print("Ogiltigt val. Återgår till huvudmenyn.")
            else:
                print("Ogiltigt val. Återgår till huvudmenyn.")
       
        elif val == "3":
            print(f"Du har {hjälte.styrka} styrka och {hjälte.hp} hp och din level är {hjälte.level}")
        else:
            print("Välj 1, 2 eller 3!")


    print("Du förlorade, din lilla råtta")


main()