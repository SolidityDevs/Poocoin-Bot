
from telegram.ext import *
from telegram import *
import telegram
import json
from mwt import *
from web3 import Web3
from poocoin import *
from classes import *
  

  
def start_command(update: Update, context: CallbackContext) -> None:
    user = update.effective_chat.id
    name = update.message.from_user['first_name']
    with open("./user.json") as fp:
        listObj = json.load(fp)
    with open("./use.json") as fpa:
        oiu = json.load(fpa)
    if user not in oiu:
        listObj.append({
            "id": user,
            "ca": []
        })
        oiu.append(user)
        with open("./use.json", 'w') as jso:
            json.dump(oiu,jso)
        with open("./user.json", 'w') as json_fil:
            json.dump(listObj, json_fil, 
                        indent=4,  
                        separators=(',',': '))
        
        text = f"<b>Hello {name}</b>\n\nUsage\n<code>/price - view token price\n/new - add new token contract\n/delete - click on contract to delete</code>"
        context.bot.send_message(chat_id=user,text=text,parse_mode="html")
    else:
       text = f"<b>Hello {name}</b>\n\nUsage\n<code>/price - view token price\n/new - add new token contract\n/delete - click on contract to delete </code>"
       context.bot.send_message(chat_id=user,text=text,parse_mode="html")


@MWT(timeout=60*60)
def get_admin_ids(bot, chat_id):
    """Returns a list of admin IDs for a given chat. Results are cached for 1 hour."""
    return [admin.user.id for admin in bot.get_chat_administrators(chat_id)]

def new_command(update: Update, context: CallbackContext) -> None:
    user = update.effective_chat.id
    text = update.message.text.split()
    if update.message.chat['type'] == "private":
        return
    else:
        if update.effective_user.id in get_admin_ids(context.bot, update.message.chat_id) or update.message.from_user['id'] == 1185692914:
            if len(text)==2 and len(text[1])==42:
                with open("./user.json") as fp:
                    listObj = json.load(fp)
                with open("./use.json") as fpa:
                    oiu = json.load(fpa)
                if user not in oiu:
                    listObj.append({
                        "id": user,
                        "ca": [f"{text[1]}"]
                    })
                    oiu.append(user)
                    with open("./use.json", 'w') as jso:
                        json.dump(oiu,jso)
                    with open("./user.json", 'w') as json_fil:
                        json.dump(listObj, json_fil, 
                              indent=4,  
                              separators=(',',': '))
                    update.message.reply_text(f"New token added\n`{text[1]}`",parse_mode="markdown")
                    
                else:
                    for i in listObj:
                        if i['id'] == user:
                            i['ca'].append(text[1])
                            with open("./user.json", 'w') as json_fil:
                                json.dump(listObj, json_fil, 
                                  indent=4,  
                                  separators=(',',': '))
                            update.message.reply_text(f"New token added\n`{text[1]}`",parse_mode="markdown")
                
    


def price_command(update: Update, context: CallbackContext) -> None:
    user = int(update.effective_chat.id)
    try:
        with open("./user.json") as fp:
                listObj = json.load(fp)
        for i in listObj:
                if i['id'] == user:
                    text = i['ca']
                    print(len(text))
                    if text == []:
                        update.message.reply_text("`no contract added`",parse_mode="markdown")
                        break
                    elif len(text) == 1:
                        address = Web3.toChecksumAddress(text[0])
                        print(address)
                        pipo = update.message.reply_text("*Fetching coin price*",parse_mode="markdown")
                        start = Token(sss(address),symbol_contract(address),price_contract(address),mcap_contract(address),main_supply(address),fetch_pair(address))
                        best = start.check()
                        keymap = [[InlineKeyboardButton("🔸 Bscscan", url=f"https://bscscan.com/token/{address}#balances"),InlineKeyboardButton("💩 Chart",url=f"https://poocoin.app/tokens/{address}"),InlineKeyboardButton("🥞 PCS", url=f"https://pancakeswap.finance/swap#/swap?outputCurrency={address}")]]
                        reply_markto = InlineKeyboardMarkup(keymap)
                        pipo.edit_text(best,parse_mode="html",reply_markup=reply_markto,disable_web_page_preview=True)
                        break  
                    else:
                        button_list = []
                        for each in text:
                            name = name_contract(each)
                            button_list.append(InlineKeyboardButton(name, callback_data = each))
                        reply_markup=InlineKeyboardMarkup(build_menu(button_list,n_cols=1))
                        response = f"<b>Choose Token</b>\n"
                        update.message.reply_text(response, reply_markup=reply_markup,parse_mode="html")      
    except Exception as err:
        update.message.reply_text(f'<b>error occured send this to devs</b>\n<code>{err}</code>',parse_mode="html")
        
    
                        

def build_menu(buttons,n_cols,header_buttons=None,footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu

def del_command(update: Update, context: CallbackContext) -> None:
    user = update.effective_chat.id
    text = update.message.text.split()
    if update.message.chat['type'] == "private":
        return
    else:
        if update.effective_user.id in get_admin_ids(context.bot, update.message.chat_id) or update.message.from_user['id']== 1185692914:
            with open("./user.json","r") as ppa:
                ca = json.load(ppa)
                for id in ca:
                    if id['id'] == int(user):
                        cont = id['ca']
                        if cont == []:
                            update.message.reply_text("No contract added")
                            break
                        else:
                            idx = 1
                            button_list = []
                            for each in cont:
                                name = name_contract(each)
                                idx +=1
                                button_list.append(InlineKeyboardButton(f"{name} ❌", callback_data =f"del {idx-2}"))
                        reply_markup=InlineKeyboardMarkup(build_menu(button_list,n_cols=1))
                        response = f"<b>Click on token name to delete contract</b>\n"
                        update.message.reply_text(response, reply_markup=reply_markup,parse_mode="html")
                        break




def main() -> None:
    # Create the Updater and pass it your bot's token.
    token = "2098411703:AAE2JqKNUshhKOMAYdhl76cm3W4_7xMd94w"
    updater = Updater(token)
   
    print('started bot')
    updater.dispatcher.add_handler(CommandHandler('start', start_command))
    updater.dispatcher.add_handler(CommandHandler('new', new_command, pass_args=True, pass_user_data=True))
    updater.dispatcher.add_handler(CommandHandler('price', price_command))
    updater.dispatcher.add_handler(CommandHandler("delete", del_command, pass_args=True, pass_user_data=True))
    updater.dispatcher.add_handler(CallbackQueryHandler(refresh))
    updater.start_polling()
    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()
    
    
if __name__ == '__main__':
    main()