from src.elements.sub_elements.commonEvent import GedcomCommonEvent
from ..element import GedcomElement


class GedcomIndividual(GedcomElement):
    """This class represents an individual in the gedcom file.
    
    :param level: The level of the individual.
    :type level: int
    :param xref: The xref of the individual.
    :type xref: str
    :param tag: The tag of the individual.
    :type tag: str
    :param sub_elements: The sub elements of the individual.
    :type sub_elements: list
    :return: The individual.
    :rtype: GedcomIndividual
    """

    def __init__(self, level: int, xref: str, tag: str, sub_elements: list):
        """Initialize the individual."""
        super().__init__(level, tag, sub_elements)
        self.__xref = xref
        self.__name = self.find_sub_element("NAME")[0].value
        self.__birth = self.__init_birth()
        self.__death = self.__init_death()
        self.__sex = self.__find_sex()

    def __init_birth(self) -> GedcomCommonEvent:
        """Initialize the birth of the individual.

        :return: The birth of the individual.
        :rtype: GedcomCommonEvent
        """
        if self.find_sub_element("BIRT") != []:
            birth = self.find_sub_element("BIRT")[0]
            birth.__class__ = GedcomCommonEvent
            birth.init_properties()
            return birth
        else:
            return None

    def __init_death(self) -> GedcomCommonEvent:
        """Initialize the death of the individual.

        :return: The death of the individual.
        :rtype: GedcomCommonEvent
        """
        if self.find_sub_element("DEAT") != []:
            death = self.find_sub_element("DEAT")[0]
            death.__class__ = GedcomCommonEvent
            death.init_properties()
            return death
        else:
            return None

    def __find_sex(self):
        """Find the sex of the individual.

        :return: The sex of the individual.
        :rtype: str
        """
        return (
            self.find_sub_element("SEX")[0].value
            if self.find_sub_element("SEX") != []
            else None
        )

    def get_name(self) -> str:
        """Get the name of the individual.

        :return: The name of the individual.
        :rtype: str
        """
        return self.__name

    def get_birth(self) -> GedcomCommonEvent:
        """Get the birth of the individual.

        :return: The birth of the individual.
        :rtype: GedcomCommonEvent
        """
        return self.__birth

    def get_death(self) -> GedcomCommonEvent:
        """Get the death of the individual.

        :return: The death of the individual.
        :rtype: GedcomCommonEvent
        """
        return self.__death

    def get_xref(self) -> str:
        """Get the xref of the individual.

        :return: The xref of the individual.
        :rtype: str
        """
        return self.__xref

    def get_first_name(self) -> str:
        """Get the first name of the individual.

        :return: The first name of the individual.
        :rtype: str
        """
        return self.__name.split("/")[0].split(" ")[0].strip()

    def get_last_name(self) -> str:
        """Get the last name of the individual.

        :return: The last name of the individual.
        :rtype: str
        """
        return self.__name.split("/")[-2].strip()

    def __str__(self):
        """Get the string representation of the individual.

        :return: The string representation of the individual.
        :rtype: str
        """
        return self.get_first_name() + " " + self.get_last_name()

    def get_data(self):
        """Get the data of the individual. The result contains name, first_name, last_name, sex, birth and death.

        :return: The data of the individual.
        :rtype: dict
        """
        return {
            "name": self.__name,
            "first_name": self.get_first_name(),
            "last_name": self.get_last_name(),
            "sex": self.__sex,
            "birth": self.__birth.get_data() if self.__birth else "",
            "death": self.__death.get_data() if self.__death else "",
        }