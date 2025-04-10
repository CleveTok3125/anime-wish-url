import os, re

# # # # # # # # # # CHANGE THIS # # # # # # # # # #
GENSHIN = r'/path/to/Genshin Impact/'
ZENLESS = r'/path/to/Zenless Zone Zero/'
# # # # # # # # # # # # # # # # # # # # # # # # # #

PATH_PATTERN = r'(.*?(?:\/|\\)(?:GenshinImpact|ZenlessZoneZero)_Data(?:\/|\\)webCaches(?:\/|\\)[0-9.]+(?:\/|\\)Cache(?:\/|\\)Cache_Data(?:\/|\\)data_2)'
LINK_PATTERN = r'(https:\/\/[A-Za-z0-9.]*?hoyoverse\.com.*?gacha(?:\-|[A-Za-z0-9])*?\/index\.html.*?&game_biz=(?:nap_global|hk4e_global))'

def find_files_regex(pattern, search_path):
    result = []
    regex = re.compile(pattern)

    for root, _, files in os.walk(search_path, topdown=False):
        for file in files:
            full_path = os.path.abspath(os.path.join(root, file))

            if regex.search(full_path):
                result.append(full_path)

    if not result:
        raise GameNotFound(search_path)

    return sorted(result, reverse=True)

class GameNotFound(Exception):
    pass

def open_file(path):
    with open(path, 'rb') as file:
        file_content = file.read()
        text = file_content.decode(errors='ignore')
        return text

def find_link_regex(pattern, text):
    match =  re.search(pattern, text)
    if match:
        return match.group(0)
    raise LinkNotFound()

class LinkNotFound(Exception):
    pass

if __name__ == '__main__':
    print('1. Genshin Impact\n2. Zenless Zone Zero')
    user_input = input('>> ')

    choices = {'1': GENSHIN, '2': ZENLESS}
    search_path = choices.get(user_input)

    if search_path:
        paths = find_files_regex(PATH_PATTERN, search_path)
        text = open_file(paths[0])
        link = find_link_regex(LINK_PATTERN, text)
        print(link)
