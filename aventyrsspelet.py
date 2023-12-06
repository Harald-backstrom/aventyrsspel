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
        self.namn = namn

class föremål:
    def __init__(self, namn, styrka_bonus):
        self.namn = namn
        self.styrka_bonus = styrka_bonus


def level_up(hjälte):
    hjälte.styrka += 1
    hjälte.level += 1
    print(f"Du har gått upp till level {hjälte.level} och din styrka har ökat! Din styrka är nu {hjälte.styrka}.")

def strid(hjälte):
    mosnter_lista = [

        monster_skapare(rand.randint(3, 7) + hjälte.level, rand.randint(3, 10) * hjälte.level, "skelett"),
        monster_skapare(rand.randint(5, 10) + hjälte.level, rand.randint(5, 12) * hjälte.level, "goblin"),
        monster_skapare(rand.randint(8, 15) + hjälte.level, rand.randint(8, 18) * hjälte.level, "jätte"),
        monster_skapare(rand.randint(12, 20) + hjälte.level, rand.randint(12, 25) * hjälte.level, "drake")

    ]

    monster = rand.choice(mosnter_lista)
    total_styrka = hjälte.styrka

    for sak in hjälte.inventory:
        total_styrka += sak.styrka_bonus

    print(f"du möter en {monster.namn} som har {monster.styrka} styrka")
    print(f"du har {hjälte.styrka} styrka och {hjälte.hp} hp kvar och du får {total_styrka - hjälte.styrka} styrka från dina vapen")
    if total_styrka >= monster.styrka:
        print("du vann")
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
        print("ditt invetory är fullt du fick inget")
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

    print("Välkommen till den mindre slumpade labyrinten! Din uppgift är att nå målet utan att hamna i fällorna.")
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
            print("Grattis! Du har nått målet.")
            break

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
    hjälte = spelar_skapare(10,rand.randint(3,6),inventory, 1, 0)

    while hjälte.hp >= 0:        
        print(
            """

            Vad vill du göra?
            1. gå genom dörr
            2. Kolla inventory
            3. Kolla stats
            
            """)
        
        val = input("")

        if val == "1":
            if rand.randint(0,2) == 0:
                hjälte = strid(hjälte)
            elif rand.randint(0,2) == 1:
                rum_med_kista(inventory)
            elif rand.randint(0,2) == 2:
                labyrint(hjälte)
            else:
                print("det var inget i rummet, din lilla råtta")
        elif val == "2":
            for sak in inventory:
                print(f"{sak.namn} som ger dig {sak.styrka_bonus} styrka")
        elif val == "3":
            print(f"du har {hjälte.styrka} styrka och {hjälte.hp} hp och din level är {hjälte.level}")
        else:
            print("Välj 1, 2 eller 3!")
            
    print("du förlorade, din lilla råtta")
main()