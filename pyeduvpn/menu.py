import sys
from itertools import chain
from pyeduvpn.remote import extract_translation, list_orgs, list_institutes


def menu() -> str:
    """
    Print options, returns target URL on success, exits client with error code 1 on failure.
    """
    if len(sys.argv) == 1:
        print("# Institute access \n")
        for i, row in enumerate(list_institutes()):
            print(f"[{i}] {extract_translation(row['display_name'])}")

        print("# Secure internet \n")

        for i, row in enumerate(list_orgs()):
            print(f"[{i}] {extract_translation(row['display_name'])}")
        sys.exit(1)

    if len(sys.argv) == 2:
        search = sys.argv[1].lower()

        institute_match = [i for i in list_institutes() if search in extract_translation(i['display_name']).lower()]

        org_match = [i for i in list_orgs() if search in i['display_name'] or
                     ('keyword_list' in i and search in i['keyword_list'])]

        if len(institute_match) == 0 and len(org_match) == 0:
            print(f"The filter '{search}' had no matches")
            sys.exit(1)
        elif len(institute_match) == 1 and len(org_match) == 0:
            institute = institute_match[0]
            print(f"filter {search} matched with institute '{institute['display_name']}'")
            return institute['base_uri']
        elif len(institute_match) == 0 and len(org_match) == 1:
            org = org_match[0]
            print(f"filter {search} matched with organisation '{org['display_name']}'")
        else:
            matches = [i['display_name'] for i in chain(institute_match, org_match)]
            print(f"filter '{search}' matched with {len(matches)} organisations, please be more specific.")
            print("Matches:")
            [print(f" - {extract_translation(m)}") for m in matches]
            sys.exit(1)
