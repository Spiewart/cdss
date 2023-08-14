import json

from django.core.serializers.json import DjangoJSONEncoder


def create_hyperlink_dict(name, link, page: int, pk: int) -> dict:
    return {
        "model": "hyperlinks.hyperlink",
        "pk": pk,
        "fields": {
            "name": name,
            "link": link,
            "page": page,
        },
    }


def create_page_dict(name, term, displaytext, version, contents: dict, pk: int) -> dict:
    return {
        "model": "pages.page",
        "pk": pk,
        "fields": {"name": name, "term": term, "displaytext": displaytext, "version": version, "contents": contents},
    }


def create_list_hyperlink_dicts() -> list[dict]:
    # NOTE: need to tidy up the json file to escape "\" characters (line 5)
    with open("cdss/json/MinneapolisItemLinks.json") as f:
        hyperlinks_json = json.load(f)
    return hyperlinks_json["json"]


def create_list_page_dicts() -> list[dict]:
    with open("cdss/json/MinneapolisOMJSON.json") as f:
        pages_json = json.load(f)
    return pages_json["json"]


def create_name_pk_dict(pages_json: str) -> dict:
    pk = 0
    name_pk_dict = {}
    for page_dict in pages_json:
        name = page_dict.get("Name")
        pk += 1
        name_pk = pk
        name_pk_dict[name] = name_pk
    return name_pk_dict


def create_fixtures_lists() -> tuple[list[dict], list[dict]]:
    hyperlink_list = []
    page_list = []
    # {item: {"pk": pk, "page": page}'s}
    item_pk_page_dict = {}
    hyperlink_pk = 0
    pages_json = create_list_page_dicts()
    hyperlinks_json = create_list_hyperlink_dicts()
    name_pk_dict = create_name_pk_dict(pages_json)
    for page_dict in pages_json:
        name = page_dict.get("Name")
        name_pk = name_pk_dict[name]
        displaytext = page_dict.get("DisplayText", None)
        term = page_dict.get("Term", None)
        version = page_dict.get("Version")
        contents_dict_list = page_dict.get("Contents")
        for contents_dict in contents_dict_list:
            item = contents_dict.get("Item", None)
            if item is not None:
                # Create hyperlink var to modify the value inserted into the context_dict later
                hyperlink = False
                # Check if item is already a page in the pk_dict
                try:
                    item_pk = name_pk_dict[item]
                except KeyError:
                    item_pk = None
                    # If the item is not a page, it is a hyperlink
                    # Iterate over the list of hyperlinks to try to find the item
                    for hyperlink_dict in hyperlinks_json:
                        if hyperlink_dict.get("Item") == item:
                            # if the item is found, mark it as a hyperlink
                            hyperlink = True
                            # Check if that item/page combination is already in the item_pk_page_dict
                            item_dict_list = [
                                (item, item_dict)
                                for (item, item_dict) in item_pk_page_dict.items()
                                if item == item and item_dict["page"] == name_pk
                            ]
                            # If so, just change hyperlink to True and pass
                            if item_dict_list:
                                pass
                            else:
                                hyperlink_pk += 1
                                item_pk = hyperlink_pk
                                if item not in item_pk_page_dict.keys():
                                    item_pk_page_dict.update({item: {}})
                                item_pk_page_dict[item].update({"pk": item_pk, "page": name_pk})
                                url = hyperlink_dict.get("URL")
                                page = name_pk
                                hyperlink_list.append(
                                    create_hyperlink_dict(
                                        name=item,
                                        link=url,
                                        page=page,
                                        pk=item_pk,
                                    )
                                )
                # If the item is a page, add 3000 to the pk to avoid pk conflicts
                if hyperlink and item_pk is not None:
                    contents_dict["Item"] = item_pk + 3000
                else:
                    contents_dict["Item"] = item_pk
        contents = json.dumps(contents_dict_list)
        page_list.append(
            create_page_dict(
                name=name, term=term, displaytext=displaytext, version=version, contents=contents, pk=name_pk
            )
        )
    return page_list, hyperlink_list


def create_fixtures_json() -> dict:
    page_list, hyperlink_list = create_fixtures_lists()
    with open("cdss/fixtures/pages.json", "w", encoding="utf-8") as f:
        json.dump(page_list, f, indent=4, cls=DjangoJSONEncoder)
    with open("cdss/fixtures/hyperlinks.json", "w", encoding="utf-8") as f:
        json.dump(hyperlink_list, f, indent=4, cls=DjangoJSONEncoder)
