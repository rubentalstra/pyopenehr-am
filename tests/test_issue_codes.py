from openehr_am.validation.issue import validate_issue_code


def test_validate_issue_code_accepts_known_prefixes_and_ranges() -> None:
    assert validate_issue_code("ADL001")
    assert validate_issue_code("ADL199")

    assert validate_issue_code("ODN100")
    assert validate_issue_code("ODN199")

    assert validate_issue_code("AOM200")
    assert validate_issue_code("AOM499")

    assert validate_issue_code("BMM500")
    assert validate_issue_code("BMM699")

    assert validate_issue_code("OPT700")
    assert validate_issue_code("OPT899")

    assert validate_issue_code("PATH900")
    assert validate_issue_code("PATH999")

    assert validate_issue_code("CLI001")
    assert validate_issue_code("CLI199")


def test_validate_issue_code_rejects_wrong_format_or_range() -> None:
    assert not validate_issue_code("")
    assert not validate_issue_code("adl001")  # must be uppercase
    assert not validate_issue_code("ADL01")  # must be ###
    assert not validate_issue_code("ADL000")  # below range
    assert not validate_issue_code("ADL200")  # above range

    assert not validate_issue_code("ODN099")
    assert not validate_issue_code("ODN200")

    assert not validate_issue_code("AOM199")
    assert not validate_issue_code("AOM500")

    assert not validate_issue_code("PATH089")
    assert not validate_issue_code("PATH1000")

    assert not validate_issue_code("CLI000")
    assert not validate_issue_code("CLI200")
    assert not validate_issue_code("CLI999")

    assert not validate_issue_code("XYZ123")  # unknown prefix
