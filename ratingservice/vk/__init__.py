import vk


# TODO remove somewhere
ACCESS_TOKEN = '19ab16214628d22328204b664a91911047b805be8b0aca00d74f5fc23177fd5c96ecd9de51ebc12a5ec16'


class VkService:
    def __init__(self):
        self.vkapi = vk.api.API(vk.api.Session(ACCESS_TOKEN))

