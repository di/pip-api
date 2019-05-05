try:
    import urllib2 as url
except ImportError:
    import urllib.request as url

import json


def _get_release_data(package_name):
    response = url.urlopen("https://pypi.org/pypi/{0}/json".format(package_name))
    data = json.loads(str(response)).get("releases")
    return data


def get_releases(package_name):
    data = _get_release_data(package_name).keys()
    return list(data)


def get_latest_release(package_name):
    release_versions = _get_release_data(package_name)

    def extract_release_date(dict_item):
        version = dict_item[0]
        upload_data = dict_item[1]

        if len(upload_data) == 0:
            return version, ""
        else:
            return version, upload_data[0].get("upload_time", None)

    release_date = list(map(extract_release_date, release_versions.items()))
    sorted(release_date, key = lambda x: x[1])
    return release_date[-1][0]
