problem_causers = ["cold", "chilled", "free-range", "plain", "beaten"]


if amount != "" and amount != " " and type(amount) != type(None):
    name = name.lower()
    amount = amount.lower()
   # todo this does not fully work

#
    try:
        # fixes the name issues like plain, caster, cold...
        for problems in problem_causers:
            if problems in name:
                name = name.replace(problems, " ")
                newname = ""
                for char in name:
                    if char.isalpha():
                        newname += char
                name = newname
            if "caster" in name:
                name = name.replace("caster", "powdered")




def fix_amounts(amount, name):
    """measurements that we can handle:
                                        gramm*
                                        tablespoon*
                                        teaspoon*
                                        mililiter*
                                        cup*
                                        slice
                                        clove
                                        litre
                                        jar
                                        whole, chopped, sliced,""*
                                        """


    #this is not used for anything, I only collected every different measurement in the recepie, so we need to deal with all of these, and this is only in the B startingletter recepies
    # TODO look for all the recepies, to deal with every different measurement shit
    measurements = ("kg", "g", "oz", "tbsp", "tablespoon", "slices", "cup", "cloves", "teaspoon", "t", "tsp", "sprig",
                    "florets", "packet", "drizzle", "dash", "ancho (it's a bug)", "tbls", "ml", "Topping", "litre", "jar",
                    "pinch", "spinkling", "splash", "finely slices", "dusting", "parts (2 parts yeast)", "lb",
                    "juice of", "grated zest of", "to taste", "grated, to taste")
    GR_list = ["g", "gramm", "gramms", "gr"] # I'm 99% sure it's spelt "gram" not "gramm"
    #start to implement slices and pieces
    measurements_to_gram= {"slice":28, "clove":4.5}

    #le kell választani a számot
    separated = number_separator(amount)
    number = separated[0]
    measurement = separated[1]
    means_the_whole_thing = ["whole", "chopped", "sliced", " ", "", "beaten"]





    #check if the value is gramm
    if measurement in GR_list:
        return (number)
    elif measurement in means_the_whole_thing:
        number = number * get_weight(name)
    elif "lb" in measurement or "pound" in measurement:
        return number * 454

        return number
    for x in measurements_to_gram:
        if fuzz.partial_token_set_ratio(x, measurement) > 95:
            return (measurements_to_gram[x]*number)
    #else: we assume it's tablespoon teaspoon or cup or ml, otherwise this will not work
    #todo fix this for 1 whole egg or 4 carrots
    #right now the program acts like 1 whole egg = 1 gramm egg
    else:
        tomililiters = consvalues.determinator(measurement)
        densitydata = get_density(name)
        return (number * tomililiters * densitydata[1].density)


def number_separator(amount):
    try: #it's needed to filter out ¼½¾ and no numbers
        try:
            amount = amount[:amount.index("/")]
        except ValueError:
            amount = amount
        except TypeError:
            amount = None
        except AttributeError:
            amount = None
        if "-" in amount: #needed to filter out e.g. 1-2 tablespoon and average it
            unit_name = ""
            numbers = []
            number = ""
            for char in amount:
                if char.isdigit() or char == "-":
                    number += char
                elif not(char.isdigit() or char == "-" or char == " "):
                    unit_name += char
            numbers = number.split("-", 1)
            number = (int(numbers[0]) + int(numbers[1])) / 2
        else:
            number = ""
            unit_name = ""
            for char in amount:
                if char.isdigit():
                    number += char
                elif char.isalpha():
                    unit_name += char
            number = int(number)
    except ValueError:
        if "¼" in amount:
            number = 0.25
        elif "½" in amount:
            number = 0.5
        elif "¾" in amount:
            number = 0.75
        else:
            number = 0

    return number, unit_name


