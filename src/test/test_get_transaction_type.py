from ..ofxstatement_santander.santander_uk_qif import SantanderUKQIFParser
from quiffen.core.account import AccountType

other_transaction_type = "OTHER"

expectations = {
    None: None,
    "": None,
    " | ": None,
    "AA , 11": "AA",
    "AA &amp; BB , 22": "AA & BB",
}


def test_get_transaction_memo():
    for transaction_memo, expectation in expectations.items():
        assert (
            SantanderUKQIFParser.get_transaction_memo(transaction_memo) == expectation
        )
