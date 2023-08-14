import json
import operator

from django.views.generic import DetailView  # type: ignore

from .models import Page  # type: ignore


class PageDetailView(DetailView):
    model = Page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contents = json.loads(self.object.contents)
        page_hyperlinks = self.object.hyperlinks.all()
        hyperlinks = {}
        for hyperlink in page_hyperlinks:
            hyperlinks.update({hyperlink.pk: hyperlink.link})
        context.update({"hyperlinks": hyperlinks})
        contents.sort(key=operator.itemgetter("Column", "Row"))
        column_one = []
        column_two = []
        for content_dict in contents:
            try:
                mnemonic = content_dict["Mnemonic"].lower()
            except KeyError:
                mnemonic = None
            if not mnemonic or not mnemonic == "test":
                column = content_dict["Column"]
                if column == 1:
                    column_one.append(content_dict)
                elif column == 2:
                    column_two.append(content_dict)
        for row_i in range(max(column_one, key=operator.itemgetter("Row"))["Row"]):
            try:
                current_row = column_one[row_i]["Row"]
            except IndexError:
                column_one.insert(row_i, {"Row": row_i, "Column": 1})
            try:
                next_row = column_one[row_i + 1]["Row"]
            except IndexError:
                next_row = None
            if next_row:
                row_diff = next_row - current_row
                if row_diff > 1:
                    for x in range(row_diff - 1):
                        column_one.insert(row_i + x + 1, {"Row": current_row + x + 1, "Column": 1})
        if column_two:
            for row_i in range(max(column_two, key=operator.itemgetter("Row"))["Row"]):
                try:
                    current_row = column_two[row_i]["Row"]
                except IndexError:
                    column_two.insert(row_i, {"Row": row_i, "Column": 2})
                try:
                    next_row = column_two[row_i + 1]["Row"]
                except IndexError:
                    next_row = None
                if next_row:
                    row_diff = next_row - current_row
                    if row_diff > 1:
                        for x in range(row_diff - 1):
                            column_two.insert(row_i + x + 1, {"Row": current_row + x + 1, "Column": 2})
        context["column_one"] = column_one
        context["column_two"] = column_two
        return context

    def get_queryset(self):
        return Page.objects.filter(pk=self.kwargs["pk"]).prefetch_related("hyperlinks")
