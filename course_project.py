import requests
from pprint import pprint

class VkUser:
    
    def __init__(self, token, version, user_id):
        self.url = 'https://api.vk.com/method/'
        self.params = {
            'access_token': vk_token,
            'v': '5.131', 
            'owner_id': '1'
        }
        
    def get_user_photos(self, user_id):
        url = 'https://api.vk.com/method/photos.get'
        params = {
            'q': 'q',
            'access_token': vk_token, 
            'v': '5.131',
            'album_id': 'profile',
            'extended': 1,
            'photo_sizes': 1,
        }
        req = requests.get(url, params)
        dict_photos = {}
        file_list = []
        for dict in req.json()['response']['items']:
            for size in dict['sizes']:
                if size['type'] == 'w':
                    photos_info = {}
                    photos_info['size'] = size['type']
                    photos_info['filename'] = dict['likes']['count']
                    file_list.append(photos_info)
                    dict_photos[dict['likes']['count']] = size['url']
                else:
                    continue  
        pprint(file_list)                             
        return dict_photos

class YandexDisk:

    def __init__(self, directory_name, yandex_token):
        self.token = yandex_token
        self.url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }
        self.directory = self.create_directory(directory_name)
    
    def create_directory(self, directory_name):
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        params = {'path': directory_name}
        if requests.get(url, headers=self.headers, params=params).status_code != 200:
            requests.put(url, headers=self.headers, params=params)
            print(f'\nDirectory {directory_name} created successfully\n')
        else:
            print(f'\nDirectory {directory_name} is already exists.\n')
        return directory_name

    def directory_meta(self, directory_name):
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        params = {'path': f'/{directory_name}'}
        meta = requests.get(url, headers=self.headers, params=params).json()['_embedded']['items']
        directory_list = []
        for elem in meta:
            directory_list.append(elem['name'])
        return directory_list
     
    def upload_file_to_disk(self, directory_name, dict_files):
        check_list = self.directory_meta(self.directory)
        counter = 0
        url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        for key, value in dict_files.items():
            if f'{key}.jpg' not in check_list:
                filename = f'{key}.jpg'
                disk_file_path = value + filename
                params = {'path': directory_name + f'/{filename}', 'url': disk_file_path, 'overwrite': 'false'}
                uploader = requests.post(url, headers=self.headers, params=params)
                counter += 1
                pprint(f'File {key} loaded successfully')
            else:
                pprint(f'File {key} is already exists')
                continue
        return f'Upload is finnished. Successfully added {counter} files.'
        
if __name__ == '__main__':
    yandex_token = input(f'Please, enter your Yandex disk token: ')
    vk_token = input(f'Please, enter your VK disk token: ')
    loadphoto = YandexDisk('backup', yandex_token)
    userphoto = VkUser(vk_token, '5.131', '1')
    pprint(loadphoto.upload_file_to_disk('backup', userphoto.get_user_photos('1')))
