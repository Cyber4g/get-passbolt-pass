from passbolt import PassboltAPI
import json

# открывает конф файл
with open("config.json") as config_file:
    dict_config = json.load(config_file)

p = PassboltAPI(dict_config=dict_config)

name = input("enter name: ")
# получение списка УЗ
resource = next((item for item in p.get_resources() if item["name"] == name), None)

# p.get_resource_secret - получение шифрованного пароля для найденной УЗ
# дешифровка пароля с помощью p.decrypt() и преобразование дешифрованного пароля в JSON-формат.
if resource is not None:
    res = (
            dict_config.get("gpg_library", "PGPy") == "gnupg"
            and json.loads(p.decrypt(p.get_resource_secret(resource["id"])).data)
            or json.loads(p.decrypt(p.get_resource_secret(resource["id"])))
    )

    print(res)
    username = resource["username"]
    password = res["password"]
    print("Username: ", username)
    print("Password:", password)
