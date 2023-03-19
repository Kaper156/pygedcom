from src import gedcom_parser


def test_parse_00():
    parser = gedcom_parser.GedcomParser("test/samples/00_simple_individual_record.ged")
    result = parser.parse()
    assert len(result["individuals"]) == 1
    assert result["individuals"][0].get_name() == "John /Doe/"
    assert str(result["individuals"][0].get_date_of_birth()) == "1 JAN 1900"
    assert str(result["individuals"][0].get_date_of_death()) == "1 JAN 1970"


def test_parse_01():
    parser = gedcom_parser.GedcomParser("test/samples/01_simple_family_record.ged")
    result = parser.parse()
    assert len(result["families"]) == 1


def test_parse_04():
    parser = gedcom_parser.GedcomParser("test/samples/04_simple_date_formats.ged")
    result = parser.parse()
    assert len(result["individuals"]) == 2
    assert str(result["individuals"][0].get_date_of_birth()) == "15 MAR 2023"
    assert str(result["individuals"][0].get_date_of_death()) == "15 MAR 2043"
    assert str(result["individuals"][1].get_date_of_birth()) == "MAR 2025"
    assert str(result["individuals"][1].get_date_of_death()) == "MAR 2075"
