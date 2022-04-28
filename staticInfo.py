pokemons = {}


def xor_int(inta, intb):
    return inta ^ intb


def xor_hex(hexa, hexb):
    return hex(xor_int(int(hexa, 16), int(hexb, 16)))


def get_pokemon_name(dec_val):
    global pokemons
    if len(pokemons) == 0:
        load_pokemons()
    return pokemons[dec_val]['name']


def get_fields(group):
    fields = {}
    if group == "G":
        fields['Species'] = (0, 2, None)
        fields['Item Held'] = (2, 2, None)
        fields['Experience'] = (4, 4, None)
        fields['PP bonuses'] = (8, 1, None)
        fields['Friendship'] = (9, 1, None)
        fields['Unknown'] = (10, 2, None)
    elif group == "A":
        fields['Move 1'] = (0, 2, None)
        fields['Move 2'] = (2, 2, None)
        fields['Move 3'] = (4, 2, None)
        fields['Move 4'] = (6, 2, None)
        fields['PP 1'] = (8, 1, None)
        fields['PP 2'] = (9, 1, None)
        fields['PP 3'] = (10, 1, None)
        fields['PP 4'] = (11, 1, None)
    elif group == "E":
        fields['HP EV'] = (0, 1, None)
        fields['Attack EV'] = (1, 1, None)
        fields['Defense EV'] = (2, 1, None)
        fields['Speed EV'] = (3, 1, None)
        fields['Special Attack EV'] = (4, 1, None)
        fields['Special Defense EV	'] = (5, 1, None)
        fields['Coolness'] = (6, 1, None)
        fields['Beauty'] = (7, 1, None)
        fields['Cuteness'] = (8, 1, None)
        fields['Smartness'] = (9, 1, None)
        fields['Toughness'] = (10, 1, None)
        fields['Feel'] = (11, 1, None)
    elif group == "M":
        fields['Pokérus status'] = (0, 1, None)
        fields['Met location'] = (1, 1, None)
        fields['Origins info'] = (2, 2, None)
        fields['IVs, Egg, and Ability'] = (4, 4, None)
        fields['Ribbons and Obedience'] = (8, 4, None)
    return fields


def load_pokemons():
    global pokemons
    with open("pokemons.csv", "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            vals = line.split(";")
            try:
                vals[1] = int(vals[1])
                dicts_vals = {}
                dicts_vals['hex_value'] = vals[0]
                dicts_vals['dec_value'] = vals[1]
                dicts_vals['img'] = vals[2]
                dicts_vals['name'] = vals[3]
                dicts_vals['type1'] = vals[4]
                dicts_vals['type2'] = vals[5]
                pokemons[vals[1]] = dicts_vals
            except:
                continue

    print("Loaded pokemons : ", len(pokemons))


def get_data_order(personality_value):
    orderd = {}
    orderd["0"] = "GAEM"
    orderd["1"] = "GAME"
    orderd["2"] = "GEAM"
    orderd["3"] = "GEMA"
    orderd["4"] = "GMAE"
    orderd["5"] = "GMEA"

    orderd["6"] = "AGEM"
    orderd["7"] = "AGME"
    orderd["8"] = "AEGM"
    orderd["9"] = "AEMG"
    orderd["10"] = "AMGE"
    orderd["11"] = "AMEG"

    orderd["12"] = "EGAM"
    orderd["13"] = "EGMA"
    orderd["14"] = "EAGM"
    orderd["15"] = "EAMG"
    orderd["16"] = "EMGA"
    orderd["17"] = "EMAG"

    orderd["18"] = "MGAE"
    orderd["19"] = "MGEA"
    orderd["20"] = "MAGE"
    orderd["21"] = "MAEG"
    orderd["22"] = "MEGA"
    orderd["23"] = "MEAG"

    return orderd[str(int(personality_value, 16) % 24)]
