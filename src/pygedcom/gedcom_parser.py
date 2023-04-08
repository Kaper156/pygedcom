import json
from .elements.rootElements.family import GedcomFamily
from .elements.rootElements.head import GedcomHead
from .elements.rootElements.individual import GedcomIndividual
from .elements.rootElements.object import GedcomObject
from .elements.rootElements.repository import GedcomRepository
from .elements.rootElements.source import GedcomSource
from .elements.element import GedcomElement
from .FormatException import FormatException


class GedcomParser:
    """The GEDCOM parser main class.

    Use this class to initialize the parsing of a GEDCOM file.
    You can then verify, parse, access the elements and export the data.

    :param path: The path to the GEDCOM file.
    :type path: str
    :return: The GEDCOM parser.
    :rtype: GedcomParser
    """

    def __init__(self, path: str):
        self.path = path
        self.head = None
        self.individuals = []
        self.families = []
        self.sources = []
        self.objects = []
        self.repositories = []

    def __open(self) -> str:
        """Open the GEDCOM file and return the content.

        :return: The content of the GEDCOM file.
        :rtype: str
        """
        with open(self.path, "r") as file:
            data = file.read()
        return data

    def __parse_line(self, line: str) -> dict:
        """Parse a line of a GEDCOM file.

        :param line: The line to parse.
        :type line: str
        :return: A dictionary with the level, the xref, the tag and the value.
        :rtype: dict
        """
        chars = line.split(" ")
        level = int(chars.pop(0))
        xref = chars.pop(0) if chars[0].startswith("@") else None
        tag = chars.pop(0)
        value = " ".join(chars) if chars != [] else ""
        return {"level": level, "xref": xref, "tag": tag, "value": value}

    def verify(self) -> dict:
        """Verify the file is a valid GEDCOM file. This only checks the level of each line, not the content.

        :return: A dictionary with the status and the message.
        :rtype: dict
        """
        file = self.__open()
        lines = file.split("\n")
        current_level = 0
        current_line = 0
        for line in lines:
            current_line += 1
            if line != "":
                # Check if the level is valid
                parsed_line = self.__parse_line(line)
                if parsed_line["level"] > current_level + 1:
                    return {
                        "status": "error",
                        "message": "Invalid level on line "
                        + str(current_line)
                        + ": "
                        + line,
                    }
                current_level = parsed_line["level"]
        return {"status": "ok", "message": ""}

    def __create_element(self, parsed_line: dict, element_lines: list):
        """Create an element based on the parsed line and the element lines.

        :param parsed_line: The parsed line.
        :type parsed_line: dict
        :param element_lines: The lines of the element.
        :type element_lines: list
        """
        if parsed_line["tag"] == "INDI":
            self.individuals.append(
                GedcomIndividual(
                    parsed_line["level"],
                    parsed_line["xref"],
                    parsed_line["tag"],
                    element_lines,
                )
            )
        elif parsed_line["tag"] == "FAM":
            self.families.append(
                GedcomFamily(
                    parsed_line["level"],
                    parsed_line["xref"],
                    parsed_line["tag"],
                    element_lines,
                )
            )
        elif parsed_line["tag"] == "HEAD":
            self.head = GedcomHead(
                parsed_line["level"],
                "",  # No xref for HEAD
                parsed_line["tag"],
                element_lines,
            )
        elif parsed_line["tag"] == "SOUR":
            self.sources.append(
                GedcomSource(
                    parsed_line["level"],
                    parsed_line["xref"],
                    parsed_line["tag"],
                    element_lines,
                )
            )
        elif parsed_line["tag"] == "REPO":
            self.repositories.append(
                GedcomRepository(
                    parsed_line["level"],
                    parsed_line["xref"],
                    parsed_line["tag"],
                    element_lines,
                )
            )
        elif parsed_line["tag"] == "OBJE":
            self.objects.append(
                GedcomObject(
                    parsed_line["level"],
                    parsed_line["xref"],
                    parsed_line["tag"],
                    element_lines,
                )
            )

    def parse(self) -> dict:
        """Parse the GEDCOM file and return a dictionary with the parsed elements

        :return: A dictionary with the parsed elements.
        :rtype: dict
        """
        self.head = None
        self.individuals = []
        self.families = []
        self.sources = []
        self.objects = []
        self.repositories = []
        file = self.__open()
        lines = file.split("\n")
        current_parsed_line = self.__parse_line(lines[0])
        element_lines = []
        if lines != []:
            for line in lines[1:]:
                if line != "":
                    tmp_parsed_line = self.__parse_line(line)
                    if tmp_parsed_line["level"] > 0:
                        element_lines.append(line)
                    else:
                        self.__create_element(current_parsed_line, element_lines)
                        current_parsed_line = tmp_parsed_line
                        element_lines = []
            self.__create_element(current_parsed_line, element_lines)
        return {
            "individuals": self.individuals,
            "families": self.families,
            "sources": self.sources,
            "objects": self.objects,
            "repositories": self.repositories,
        }

    def get_stats(self) -> dict:
        """Get statistics about the GEDCOM file.

        :return: A dictionary with the statistics.
        :rtype: dict
        """
        return {
            "head": "OK" if self.head is not None else "None",
            "individuals": len(self.individuals),
            "families": len(self.families),
            "sources": len(self.sources),
            "objects": len(self.objects),
            "repositories": len(self.repositories),
        }

    def export(self, format: str = "json", empty_fields=True) -> str:
        """Export the GEDCOM file to another format.

        :param format: The format to export to. Default is "json".
        :type format: str
        :param empty_fields: If True, empty fields will be exported. Default is True.
        :type empty_fields: bool
        :return: The exported file's content.
        :rtype: str
        """
        if format not in ["json", "gedcom"]:
            raise FormatException("Format " + format + " is not supported.")
        if format == "json":
            export = {}
            if empty_fields or self.head:
                export["head"] = (
                    self.head.export(empty_fields=empty_fields) if self.head else ""
                )
            if empty_fields or self.individuals:
                export["individuals"] = {}
                for individual in self.individuals:
                    export["individuals"][individual.get_xref()] = individual.export(
                        empty_fields=empty_fields
                    )
            if empty_fields or self.families:
                export["families"] = {}
                for family in self.families:
                    export["families"][family.get_xref()] = family.export(
                        empty_fields=empty_fields
                    )
            if empty_fields or self.sources:
                export["sources"] = {}
                for source in self.sources:
                    export["sources"][source.get_xref()] = source.export(
                        empty_fields=empty_fields
                    )
            if empty_fields or self.objects:
                export["objects"] = {}
                for object in self.objects:
                    export["objects"][object.get_xref()] = object.export(
                        empty_fields=empty_fields
                    )
            if empty_fields or self.repositories:
                export["repositories"] = {}
                for repository in self.repositories:
                    export["repositories"][repository.get_xref()] = repository.export(
                        empty_fields=empty_fields
                    )
            return json.dumps(export, indent=4, ensure_ascii=False)
        if format == "gedcom":
            content = ""
            if self.head:
                content += self.head.extract_gedcom()
            for individual in self.individuals:
                content += individual.extract_gedcom()
            for family in self.families:
                content += family.extract_gedcom()
            for source in self.sources:
                content += source.extract_gedcom()
            for object in self.objects:
                content += object.extract_gedcom()
            for repository in self.repositories:
                content += repository.extract_gedcom()
            content += "0 TRLR\n"
            return content

    def get_parents(self, individual: GedcomIndividual) -> list:
        """Get the parents of an individual.

        :param individual: The individual to get the parents of.
        :type individual: GedcomIndividual
        :return: A list of GedcomIndividual objects.
        :rtype: list
        """
        parents = []
        for family in self.families:
            if individual.get_xref() in family.get_children():
                if family.get_husband() != "":
                    parents.append(self.find_individual(family.get_husband()))
                if family.get_wife() != "":
                    parents.append(self.find_individual(family.get_wife()))
        return parents

    def get_children(self, individual: GedcomIndividual) -> list:
        """Get the children of an individual.

        :param individual: The individual to get the children of.
        :type individual: GedcomIndividual
        :return: A list of GedcomIndividual objects.
        :rtype: list
        """
        children = []
        for family in self.families:
            if individual.get_xref() in family.get_parents():
                for child in family.get_children():
                    children.append(self.find_individual(child))
        return children

    def __find_root_element(self, collection: list, xref: str) -> GedcomElement:
        """Find an element in a collection by its xref.

        :param collection: The collection to search in.
        :type collection: list
        :param xref: The xref to search for.
        :type xref: str
        :return: The element if found, None otherwise.
        :rtype: GedcomElement
        """
        for element in collection:
            if element.get_xref() == xref:
                return element
        return None

    def find_individual(self, xref: str) -> GedcomIndividual:
        """Find an individual by its xref.

        :param xref: The xref to search for.
        :type xref: str
        :return: The individual if found, None otherwise.
        :rtype: GedcomIndividual
        """
        return self.__find_root_element(self.individuals, xref)

    def find_family(self, xref: str) -> GedcomFamily:
        """Find a family by its xref.

        :param xref: The xref to search for.
        :type xref: str
        :return: The family if found, None otherwise.
        :rtype: GedcomFamily
        """
        return self.__find_root_element(self.families, xref)

    def find_source(self, xref: str) -> GedcomSource:
        """Find a source by its xref.

        :param xref: The xref to search for.
        :type xref: str
        :return: The source if found, None otherwise.
        :rtype: GedcomSource
        """
        return self.__find_root_element(self.sources, xref)

    def find_object(self, xref: str) -> GedcomObject:
        """Find an object by its xref.

        :param xref: The xref to search for.
        :type xref: str
        :return: The object if found, None otherwise.
        :rtype: GedcomObject
        """
        return self.__find_root_element(self.objects, xref)

    def find_repository(self, xref: str) -> GedcomRepository:
        """Find a repository by its xref.

        :param xref: The xref to search for.
        :type xref: str
        :return: The repository if found, None otherwise.
        :rtype: GedcomRepository
        """
        return self.__find_root_element(self.repositories, xref)