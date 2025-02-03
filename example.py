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

print(model.solve({'t' : 3, 'g' : 2, 'k' : 4, 'b' : 8}))
