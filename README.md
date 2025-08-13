# make_24
A small gadget to play the game of make24.
Given 4 integers, with basic arithmetic operations alone (add, subtract, multiply, divide), compute 24.


## Usage
```
git clone https://github.com/paul0403/make_24.git
python3 example.py
```

Tweak the numbers to your liking. As an example, for the numbers `2, 1, 4, 7`, the package would print
```
7 + 4 -> 11
11 + 1 -> 12
12 * 2 -> 24
```

Of course, you can also use the package in your own python scripts:
```python
import make24
```

This project is not currently on PyPI, so git cloning from source is the only way to use it. 


## Development and Conribution
Feel free to contribute this project by submitting a pull request. 
I will take a look.

When submitting PRs, please fully test your code by running 
`make pytest`