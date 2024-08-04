import requests


class EagleAPI:
    def __init__(self, base_url="http://localhost:41595"):
        self.base_url = base_url

    # #########################################
    # 画像をEagleに送信
    def add_item_from_path(self, data, folder_id=None):
        print(self._get_all_folder_list())

        if folder_id:
            data["folderId"] = folder_id
        return self._send_request("/api/item/addFromPath", method="POST", data=data)


    # #########################################
    # Eagle のフォルダID、名前の一覧を取得
    def _get_all_folder_list(self):
        try:
            json = self._send_request("/api/folder/list")
            return self._extract_id_name_pairs(json["data"])
        except requests.RequestException:
            return []


    # #########################################
    # Private method for sending requests
    def _send_request(self, endpoint, method="GET", data=None):
        url = self.base_url + endpoint
        headers = {"Content-Type": "application/json"}

        try:
            if method == "GET":
                response = requests.get(url, headers=headers)
            elif method == "POST":
                response = requests.post(url, headers=headers, json=data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            return response.json()

        except requests.RequestException as e:
            print(f"Eagle request failed: {e}")
            raise


    # #########################################
    # フォルダリストを作成
    def _extract_id_name_pairs(self, data):
        result = []

        def recursive_extract(item):
            if isinstance(item, dict):
                if 'id' in item and 'name' in item:
                    result.append({'id': item['id'], 'name': item['name']})
                if 'children' in item and isinstance(item['children'], list):
                    for child in item['children']:
                        recursive_extract(child)
            elif isinstance(item, list):
                for element in item:
                    recursive_extract(element)

        recursive_extract(data)
        return result
