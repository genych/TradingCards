import TradingCards as tc
import gui
import os


def test_packs():
    for pack in tc.packs.values():
        cards = pack.openPack()
        for card in cards:
            print('{} from {}'.format(card.cardName, pack.packName))

def test_download():
    image = gui.get_image('dummy')
    assert os.path.exists(image)

if __name__ == '__main__':
    # test_packs()
    test_download()
