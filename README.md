# Welcome to Conjure-python!

This python library allow you to blend your python app with conjure and find solutions for your models.

## A simple tutorial
First, let's import the necessary dependencies. The only mandatory one is the ```EssenceModel``` class, all the others are accessory you can skip.

### Solving an instance
To solve an instance you have to declare a model via the ```EssenceModel``` class. You can either add the model directly while declaring the class or afterwards in your code.

```py 
from conjure_python import EssenceModel

model = EssenceModel()

#add your model
model_str = """
...
"""
model.append(model_str)
```

To add your parameters you can either add them one by one via the ```add_parameters(name, value)``` method or you can pass all your parameters as a dictionary to the ```solve``` method.

Once you call the solve method it will return an instance of the ```EssenceSolution``` class which will contain a ```state``` variable indicating if conjure was able to find a solution and a list of solutions found by the solver. The solutions can be indexed using an integer index and they can be accessed as raw solutions (by setting the ```mode``` variable to "raw") or a python-native solution (by setting the ```mode``` variable to "python"). In the second case, all variables will have the correct type and you will be able to use them as native python objects.

```py
solutions = model.solve({})
if solutions.state == "SAT":
    for sol in solutions:
        print(sol)
else:
    print("solution not found")
```

## The python-native types
Currently the following native python types are supported: int, bool, function, matrix, record, tuples and relation. 
For the int, bool and tuple types are simple python types.
All the other types derive from the base class ```EssenceType``` which implements the ```___hash___```, ```___len___``` and ```___str___``` methods.
### The matrix type (EssenceMatrix)
The matrix type has a tuple called ```shape``` which contains an integer value that represents the number of elements for each dimension of the matrix.
Another tuple, ```index_types``` contains the type of each index (in order) of the matrix.
Finally, the matrix can be directly indexed with a single value or a tuple of value to get the elements of the matrix.
### The function type (EssenceFunction)
The function type can be directly called to access its values. It also has a dictionary ```types``` with two keys: ```"codomain"``` and ```"domain"``` containing, respectively the codomain type and domain type of the function. The property ```domain_values``` is a set with all the values of the domain while the property ```codomain_values``` is a set with all the values of the codomain.
### The relation type (EssenceRelation)
The relation type can also be indexed via an integer value to get the corresponding element. The relation values are simple tuples. The type of each element of the tuple can be accessed via the property ```relation_type``` of the relation type. The property ```relations_len``` represents the number of elements in each tuple.
## The record type (EssenceRecord)
The record type is a simple dictionary and can be used as such. It implements the ```keys()```, ```items()``` and ```values()``` methods. It can also has a property ```record_types``` which is a dictionary containing the type of each key of the record.

## check for conjure 
if you want to check if conjure is available on your system by using the ```is_conjure_available()``` function which returns a boolean value.
```py
from conjure_python import is_conjure_available
print("Is conjure available?", is_conjure_available())
```
