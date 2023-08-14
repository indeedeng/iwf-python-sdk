class Parent:
    def __init__(self, *args, **kwargs):
        self.somevar = "test"
        self.anothervar = "anothertest"

        # important part, call the init surrogate pass through args:
        self._init(*args, **kwargs)

    # important part, a placeholder init surrogate:
    def _init(self, *args, **kwargs):
        print("Parent class _init; ", self, args, kwargs)

    def some_base_method(self):
        print("some base method in Parent")
        self.a_new_dict = {}


class Child1(Parent):
    # when omitted, the parent class's __init__() is run
    # def __init__(self):
    #    pass

    # overloading the parent class's  _init() surrogate
    def _init(self, *args, **kwargs):
        print(f"Child1 class _init() overload; ", self, args, kwargs)

        self.a_var_set_from_child = "This is a new var!"


class Child2(Parent):
    def __init__(self, onevar, twovar, akeyword):
        super().__init__()
        print(f"Child2 class __init__() overload; ", self)

        # call some_base_method from parent
        self.some_base_method()

        # the parent's base method set a_new_dict
        print(self.a_new_dict)


class Child3(Parent):
    pass


def test_placeholder() -> None:
    print("\nRunning Parent()")
    Parent()
    Parent("a string", "something else", akeyword="a kwarg")

    print(
        "\nRunning Child1(), keep Parent.__init__(), overload surrogate Parent._init()"
    )
    Child1()
    Child1("a string", "something else", akeyword="a kwarg")

    print("\nRunning Child2(), overload Parent.__init__()")
    # Child2() # __init__() requires arguments
    Child2("a string", "something else", akeyword="a kwarg")

    print("\nRunning Child3(), empty class, inherits everything")
    Child3().some_base_method()
