#!/usr/bin/env python3
"""
James L. Rogers | github.com/DarkWinged
basic classes overviwe
"""

#Basic class
class My_class:
    #When called crates a new My_class object and creates entries for the attributes and methods
    #It is automatically called when you make an object with My_class()
    #You only need to define this function if you need to do specific modifications while inheriting from multiple classes
    #generally don't touch this as all classes have a default version of this method
    """
    def __new__(self):
        pass
    """

    #Automatically called at the end of the __new__() sets the values of the objects attributes
    #It is generally bad practice to do more than format arguments and assign them to attributes
    def __init__(self, name: str):
        self.name = name.capitalize()
        # _hidden attributes are used for internal values that shouldn't be accessed from outside the object
        self._nick_name = 'the Red'
        """ Bad practice:
        me = My_class('ragnar')
        print(me._nick_name)
        """#'the Red'
        """ Good practice
        me = My_class('ragnar')
        print(me.get_title())   
        """#'Ragnar the Red'

    #Methods are functions that a bundled inside an object
    #They have access to the object's attributes and other methods through the self variable
    def get_title(self) -> str:
        return f'{self.name} {self._nick_name}'
    
    
    #If you do require a _hidden attribute it is best practice to use a getter function to access it
    #Getter methods return a copy of the _hidden attribute
    #This prevents external functions from modifying the internal value of the _hidden attribute
    #They can also allow you to format a _hidden attribute before returning it
    @property
    def nick_name(self) -> str:
        return self._nick_name.lower()
    
    #Like getter methods setter methods allow structured access to _hidden attributes
    #They can allow you to format or reject changes to _hidden attributes before applying them
    @nick_name.setter
    def nick_name(self, new_nick_name: str):
        if new_nick_name.lower() != 'the lame':
            self._nick_name = new_nick_name.capitalize()

    #The Static Method decorator defines a method that is bundled inside the class definition
    #They act on the class as a whole and don't have access to an object's attributes through the self variable
    #Typically used for helper methods that don't require access to an object's attributes or methods
    @staticmethod
    def make_a_title():
        return 'the lame'


if __name__ == '__main__':
    ragnar = My_class('ragnar')
    print(ragnar.get_title())
    print(My_class.make_a_title())
    ragnar.new_nick_name = My_class.make_a_title()
    print(ragnar.nick_name)
