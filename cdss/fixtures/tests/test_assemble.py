import pytest  # type: ignore
from django.test import TestCase  # type: ignore

from ..assemble_fixtures import create_page_list

pytestmark = pytest.mark.django_db


class TestCreatePageList(TestCase):
    def test__all_pks_unique(self):
        page_list = create_page_list()
        pk_list = [page_dict.get("pk") for page_dict in page_list]
        pk_list.sort()
        pk_set = set(pk_list)
        self.assertEqual(len(pk_list), len(pk_set))
