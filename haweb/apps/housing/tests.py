from django.test import TestCase

from csvmgr import validate_csv, import_new_admissions
from ..core.models import Tenant, Unit, Contract, ZipCode, City


class CsvMgrTest(TestCase):
    def test_validate_csv(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        row0 = ['tenant_id', 'firstname']
        require_fields = ['first_name']
        ok, column_pos = validate_csv(row0, require_fields)
        self.assertEqual(ok, False)

        row0 = ['tenant_id', 'first_name']
        require_fields = ['first_name']
        ok, column_pos = validate_csv(row0, require_fields)
        self.assertEqual(ok, True)

        expected_pos = {
            'tenant_id': 0,
            'first_name': 1
        }
        self.assertDictEqual(column_pos, expected_pos)

    def test_import_new_admissions(self):
        import_new_admissions("/Users/ediliogallardo/Downloads/New Admissions Sample - Sheet1.csv")

        self.assertEqual(City.objects.count(), 1)
        self.assertEqual(ZipCode.objects.count(), 1)
        self.assertEqual(Contract.objects.count(), 1)
        self.assertEqual(Unit.objects.count(), 1)
        self.assertEqual(Tenant.objects.count(), 1)