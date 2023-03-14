class dog:

    @staticmethod
    def bark():
        result = dog.wanwan()
        return result

    @staticmethod
    def wanwan():
        return "わんわん"


print(dog.bark())