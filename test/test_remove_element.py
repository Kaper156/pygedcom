import json
from ..src.pygedcom import gedcom_parser


def test_remove_individual():
    parser = gedcom_parser.GedcomParser("test/samples/01_simple_family_record.ged")
    parser.parse()
    result = json.loads(parser.export())
    assert result["individuals"]["@I1@"]["name"] == "John /Travolta/"
    assert result["individuals"]["@I2@"]["name"] == "Jane /Travolta/"
    assert result["families"]["@F1@"]["husband"] == "@I1@"
    assert result["families"]["@F1@"]["wife"] == "@I2@"
    assert result["families"]["@F1@"]["children"] == ["@I3@"]
    assert result["families"]["@F1@"]["marriage"]["date"]["day"] == "01"
    assert result["families"]["@F1@"]["marriage"]["date"]["month"] == "JAN"
    assert result["families"]["@F1@"]["marriage"]["date"]["year"] == "1925"

    parser.remove_individual("@I1@")
    result = json.loads(parser.export())
    assert len(result["individuals"]) == 1
    assert result["individuals"]["@I2@"]["name"] == "Jane /Travolta/"
    assert result["families"]["@F1@"]["husband"] == ""
    assert result["families"]["@F1@"]["wife"] == "@I2@"
    assert result["families"]["@F1@"]["children"] == ["@I3@"]
    assert result["families"]["@F1@"]["marriage"]["date"]["day"] == "01"
    assert result["families"]["@F1@"]["marriage"]["date"]["month"] == "JAN"
    assert result["families"]["@F1@"]["marriage"]["date"]["year"] == "1925"
