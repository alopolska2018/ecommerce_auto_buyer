from api_allegro.ModifyBuyNowPrice import ModifyBuyNowPrice
from AllegroAutoBuyer import AllegroAutoBuyer
from api_allegro.GetAllFieldsOfTheParticularOffer import GetAllFieldsOfTheParticularOffer


def read_file(filename):
    file = open(filename, 'r')

    auction_numbers = []

    for line in file:
        line = line.strip()
        auction_numbers.append(line)

    return auction_numbers

def decrease_by_percentage(number, percentage):
    result = number - (float(number)/100 * float(percentage))
    return result

allegro_price_checker = GetAllFieldsOfTheParticularOffer('alopl')
print(allegro_price_checker.get_user_info())
original_price = allegro_price_checker.get_offer_price('8479414005')
print(original_price)
allegro_price_modifier = ModifyBuyNowPrice()


percentage_decrease = input('What percentage do you want to decrease price by:  ')
account_name = input('Provide allegro account name you are going to buy from: ')
choice = input('Read auctions numbers from file? [y/n]: ')
if choice == 'y':
    filename = input('Enter filename [{file must be inside script dir} ex. auctions.txt]: ')
    auction_numbers = read_file(filename)
    auto_buyer = AllegroAutoBuyer()
    print('Chosen account: {}'.format(account_name))
    for auction_number in auction_numbers:
        print('Auction number: {}'.format(auction_number))
        original_price = allegro_price_checker.get_offer_price(auction_number, account_name)
        print('Orginal price: {}'.format(original_price))
        modified_price = decrease_by_percentage(float(original_price), float(percentage_decrease))
        if (float(original_price) - modified_price) > 50:
            modified_price = float(original_price) - 49
        print('Modified price: {}'.format(int(modified_price)))
        allegro_price_modifier.modify_price(auction_number, int(modified_price), account_name)
        print('price has been modified')
        current_price = allegro_price_checker.get_offer_price(auction_number, account_name)
        print('current price {}'.format())
        auto_buyer.perform(auction_number)
        current_price = allegro_price_modifier.modify_price(auction_number, original_price)
        print('orginal price restored, current price: {}'.format(current_price))


elif choice == 'n':
    auction_number = input('Enter auction number: ')
    original_price = allegro_price_checker.get_offer_price(auction_number)
    modified_price = decrease_by_percentage(1440, float(percentage_decrease))
    allegro_price_modifier.modify_price(auction_number, modified_price)
    auto_buyer = AllegroAutoBuyer()
    auto_buyer.perform(auction_number)
    allegro_price_modifier.modify_price(auction_number, original_price)
else:
    print('Wrong choice')
