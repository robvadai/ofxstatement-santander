import tempfile
from datetime import datetime
from decimal import Decimal

import pytest

from ofxstatement.ui import UI

from ..ofxstatement_santander.santander_uk_qif import SantanderUKQIFPlugin

QIF_FILE_CONTENT = """!Type:Oth L
D30/03/2024
T-1080.00
PTRANSFER REFERENCE R&amp;D                                                                , 1080.00
^
D20/04/2024
T-2.75
PFOREIGN CURRENCY CONVERSION FEE                                                           , 2.75
^
D10/03/2024
T1200.00
PFASTER PAYMENTS RECEIPT                                                                   , 1200.00
^
D27/02/2024
T-1000.00
PBILL PAYMENT VIA FASTER PAYMENT , MANDATE NO 94                                           , 1000.00
^
D15/02/2024
T-120.00
PDIRECT DEBIT PAYMENT TO TAX, MANDATE NO 0011                                              , 120.00
^"""

EXPECTED_CURRENCY_USD = "USD"


@pytest.mark.integration
def test_parse_qif_file():

    plugin = SantanderUKQIFPlugin(UI(), {"day-first": True, "currency": "USD"})

    with tempfile.NamedTemporaryFile(delete_on_close=False, suffix=".qif") as fp:
        fp.writelines([f"{line}\n".encode() for line in QIF_FILE_CONTENT.splitlines()])
        fp.close()

        parser = plugin.get_parser(fp.name)
        statement = parser.parse()

        assert len(statement.lines) == 5

        first_line = statement.lines[0]
        assert first_line.date == datetime(2024, 3, 30)
        assert first_line.date_user == datetime(2024, 3, 30)
        assert first_line.amount == Decimal(-1080)
        assert first_line.trntype == "DEBIT"
        assert first_line.currency.symbol == EXPECTED_CURRENCY_USD
        assert first_line.payee is None
        assert first_line.memo == "TRANSFER REFERENCE R&D"

        second_line = statement.lines[1]
        assert second_line.date == datetime(2024, 4, 20)
        assert second_line.date_user == datetime(2024, 4, 20)
        assert second_line.amount == Decimal(-2.75)
        assert second_line.trntype == "DEBIT"
        assert second_line.currency.symbol == EXPECTED_CURRENCY_USD
        assert second_line.payee is None
        assert second_line.memo == "FOREIGN CURRENCY CONVERSION FEE"

        third_line = statement.lines[2]
        assert third_line.date == datetime(2024, 3, 10)
        assert third_line.date_user == datetime(2024, 3, 10)
        assert third_line.amount == Decimal(1200)
        assert third_line.trntype == "DEBIT"
        assert third_line.currency.symbol == EXPECTED_CURRENCY_USD
        assert third_line.payee is None
        assert third_line.memo == "FASTER PAYMENTS RECEIPT"

        fourth_line = statement.lines[3]
        assert fourth_line.date == datetime(2024, 2, 27)
        assert fourth_line.date_user == datetime(2024, 2, 27)
        assert fourth_line.amount == Decimal(-1000)
        assert fourth_line.trntype == "DEBIT"
        assert fourth_line.currency.symbol == EXPECTED_CURRENCY_USD
        assert fourth_line.payee is None
        assert fourth_line.memo == "BILL PAYMENT VIA FASTER PAYMENT , MANDATE NO 94"

        fifth_line = statement.lines[4]
        assert fifth_line.date == datetime(2024, 2, 15)
        assert fifth_line.date_user == datetime(2024, 2, 15)
        assert fifth_line.amount == Decimal(-120)
        assert fifth_line.trntype == "DEBIT"
        assert fifth_line.currency.symbol == EXPECTED_CURRENCY_USD
        assert fifth_line.payee is None
        assert fifth_line.memo == "DIRECT DEBIT PAYMENT TO TAX, MANDATE NO 0011"