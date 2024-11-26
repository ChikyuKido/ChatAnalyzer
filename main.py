import os.path
from chat_message import Chat, ChatType
from tqdm import tqdm
from plotter import Plotter
from util import Util
import argparse

def loadChats(path,chat_type):
    if not os.path.exists(path):
        return []
    if os.path.isdir(path):
        files = os.listdir(path)
        files = [path+"/"+file for file in files]
    else:
        files = [path]
    chats = []
    for file in tqdm(files, desc=f"Loading {chat_type.name.lower()} chats", unit="file"):
        chat = Chat(file, chat_type)
        chat.parse()
        chats.append(chat)
    return chats

def loadWhatsappChats(path):
    chats = loadChats(path,ChatType.WHATSAPP)
    if len(chats) == 0:
        print(f"Failed to find path {path} for whatsapp chats")
        exit(-1)
    return chats
def loadSignalChats(path):
    chats = loadChats(path,ChatType.SIGNAL)
    if len(chats) == 0:
        print(f"Failed to find path {path} for signal chats")
        exit(-1)
    return chats

def main():
    Util.load_slurs_from_file("blacklist.txt")
    parser = argparse.ArgumentParser(
        description="A simple cli tool to create paths from an exported signal chat"
    )
    parser.add_argument(
        "-is", "--input-signal", action="store",
        help="The input file or folder for the signal chats"
    )
    parser.add_argument(
        "-iw", "--input-whatsapp", action="store",
        help="The input file or folder for the whatsapp chats"
    )
    parser.add_argument(
        "-c", "--chart", action="store",
        required=True,
        choices=["pie_all_messages_per_user",
                 "pie_all_messages_per_chat",
                 "pie_over_n_words_over_user",
                 "pie_over_slur_words_over_user",
                 "pie_over_n_words_over_chat",
                 "line_over_messages_per_period",
                 "line_over_messages_per_chat_per_period"]
    )
    parser.add_argument(
        "-p" "--period", action="store",
        help="The period for the chart",
        choices=["d", "w", "m", "y"]
    )

    args = parser.parse_args()
    print(args)
    if not args.input_signal and not args.input_whatsapp:
        print("Error: You must provide at least one of --input-signal or --input-whatsapp.")
        return

    chats = []

    if args.input_signal:
        chats.extend(loadSignalChats(args.input_signal))
    if args.input_whatsapp:
        chats.extend(loadWhatsappChats(args.input_whatsapp))

    operation_mapping = {
        "pie_all_messages_per_user": Plotter.showPieOverAllMessagesPerUser,
        "pie_all_messages_per_chat": Plotter.showPieOverMessagesPerChat,
        "pie_over_n_words_over_user": Plotter.showPieOverNWordsOverUser,
        "pie_over_slur_words_over_user": Plotter.showPieOverSlurWordsOverUser,
        "pie_over_n_words_over_chat": Plotter.showPieOverNWordsOverChat,
    }
    operation_mapping_additional_period = {
        "line_over_messages_per_period": Plotter.showMessagesPerPeriod,
        "line_over_messages_per_chat_per_period": Plotter.showMessagesPerChatPerPeriod,
    }
    if args.chart in operation_mapping:
        operation_mapping[args.chart](chats)
    elif args.chart in operation_mapping_additional_period:
        if args.p__period is None:
            print(f"Parameter period is missing for {args.chart}")
            return
        operation_mapping_additional_period[args.chart](chats,args.p__period.upper())
if __name__ == "__main__":
    main()