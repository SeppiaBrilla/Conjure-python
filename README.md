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

### The python-native types
There are (currently) four native python types supported: int, bool, function and matrix. The int and bool implementations are pretty straight forward. For the matrix and function implementations it was necessary to create a custom type which derives from ```EssenceType```. 
For the function implementation, you can simply call the function with your parameter and get the corresponding output. You can also check the function domain and codomain via their respective variables.
For the matrix implementation you can simply access its content via indexing. You can also check the matrix index types via the ```index_types``` variable and the matrix shape via the ```shape``` variable. 

### check for conjure 
if you want to check if conjure is available on your system by using the ```is_conjure_available()``` function which returns a boolean value.
```py
from conjure_python import is_conjure_available
print("Is conjure available?", is_conjure_available())
```
