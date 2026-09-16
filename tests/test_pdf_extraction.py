import unittest
from main import extract_invoice_data


class TestInvoiceExtraction(unittest.TestCase):
    def test_extract_invoice_data_success(self):
        sample_text = """
        DANFE
        NF-e
        Nº 000580
        Série 1
        Destinatário/Remetente
        Nome / Razão Social
        Joao Eduardo Mariano de Souza
        CNPJ/CPF
        390.060.638-27
        """
        result = extract_invoice_data(sample_text)
        self.assertEqual(result["invoice_number"], "000580")
        self.assertEqual(result["recipient_name"], "Joao Eduardo Mariano de Souza")

    def test_extract_invoice_data_missing(self):
        sample_text = "Some random text without matching patterns."
        result = extract_invoice_data(sample_text)
        self.assertIsNone(result["invoice_number"])
        self.assertIsNone(result["recipient_name"])


if __name__ == "__main__":
    unittest.main()
