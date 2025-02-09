from conjure_python import EssenceModel

model = EssenceModel(model="""language Essence 1.3
    given t : int(1..) $ strength (size of subset of rows)
    given k : int(1..) $ rows
    given g : int(2..) $ number of values
    given b : int(1..) $ columns
    where k>=t, b>=g**t
    find CA: matrix indexed by [int(1..k), int(1..b)] of int(1..g)
    such that
        forAll rows : sequence (size t) of int(1..k) .
            (forAll i : int(2..t) . rows(i-1) < rows(i)) ->
            forAll values : sequence (size t) of int(1..g) .
                exists column : int(1..b) .
                    forAll i : int(1..t) .
                        CA[rows(i), column] = values(i)
    such that forAll i : int(2..k) . CA[i-1,..] <=lex CA[i,..]
    such that forAll i : int(2..b) . CA[..,i-1] <=lex CA[..,i]
    """)

model.set_solver("chuffed")
model.set_random_seed(0)
model.set_time_limit(1000)
print(model.solve({'t' : 3, 'g' : 2, 'k' : 4, 'b' : 8}))

model.clear()
model.append("""language Essence 1.3
given n_cars, n_classes, n_options : int(1..)
letting Slots  be domain int(1..n_cars),
        Class  be domain int(1..n_classes),
        Option be domain int(1..n_options),
given quantity      : function (total) Class  --> int(1..),
      maxcars       : function (total) Option --> int(1..),
      blksize_delta : function (total) Option --> int(1..),
      usage         : relation (minSize 1) of ( Class * Option )
where n_cars >= n_classes
where ( sum quant : Class . quantity(quant) ) = n_cars
$ where forAll option: Option . maxcars(option) < blksize(option)
where  forAll option: Option .  |toSet(usage(_,option))| >= 1
where  forAll class: Class .  |toSet(usage(class,_))| >= 1
find car : function (total) Slots --> Class
such that
    forAll c : Class . |preImage(car,c)| = quantity(c),
    forAll opt : Option .
        forAll s : int(1..n_cars+1-(maxcars(opt)+blksize_delta(opt))) .
            (sum i : int(s..s+(maxcars(opt)+blksize_delta(opt))-1) . toInt(usage(car(i),opt))) <= maxcars(opt)""")
instance = {
    "blksize_delta": {"1": 1, "2": 1, "3": 2, "4": 3, "5": 4}, 
    "maxcars": {"1": 1, "2": 2, "3": 1, "4": 2, "5": 1}, "n_cars": 100, "n_classes": 18, "n_options": 5, 
    "quantity": {"1": 5, "10": 6, "11": 12, "12": 1, "13": 1, "14": 5, "15": 9, "16": 5, "17": 12, "18": 1, 
                 "2": 3, "3": 7, "4": 1, "5": 10, "6": 2, "7": 11, "8": 5, "9": 4},
    "usage":[[1, 1], [1, 2], [1, 5], [2, 1], [2, 2], [2, 4], [3, 1], [3, 2], [3, 3], [4, 2], [4, 3], [4, 4], [5, 1], [5, 2],
             [6, 1], [6, 5], [7, 1], [7, 4], [8, 1], [8, 3], [9, 2], [9, 5], [10, 2], [10, 4], [11, 2], [11, 3], [12, 3],
             [12, 5], [13, 3], [13, 4], [14, 1], [15, 2], [16, 5], [17, 4], [18, 3]]
}
print(model.solve(instance))

model.clear()
model.append("""language Essence 1.3
find r : relation (minSize 4) of (int(1..3) * int(1..3))
""")
print(model.solve())

model.clear()
model.append("""language Essence 1.3
find t : tuple(int(1..5), int(9..15), int(1..5))
""")
print(model.solve()[0,"t"])
