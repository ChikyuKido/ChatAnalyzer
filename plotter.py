import os.path

import pandas as pd
import plotly.express as px

class Plotter:
    @staticmethod
    def getDataFromChats(chats):
        data = []
        for chat in chats:
            for message in chat.messages:
                data.append(message.convertToMap())
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])
        return df
    @staticmethod
    def showPieOverAllMessagesPerUser(chats):
        df = Plotter.getDataFromChats(chats)
        user_message_counts = df['user'].value_counts()
        fig_pie = px.pie(names=user_message_counts.index, values=user_message_counts.values,
                         title=f"Messages per User. All messages: {len(df)}")
        fig_pie.show()
    @staticmethod
    def showPieOverMessagesPerChat(chats):
        data = [{
            "chat": chat.chat_name,
            "message_count": len(chat.messages),
        } for chat in chats]
        all_message_count = 0
        for chat in data:
            all_message_count += chat['message_count']
        df = pd.DataFrame(data)
        fig_pie = px.pie(names=df["chat"], values=df["message_count"],
                         title=f"Messages per User. All messages: {all_message_count}")
        fig_pie.show()
    @staticmethod
    def showPieOverNWordsOverUser(chats):
        df = Plotter.getDataFromChats(chats)
        df = df[df['countN'] != 0]
        all_n_words = 0
        for chat in chats:
            for message in chat.messages:
                all_n_words += message.countN
        messages = df.groupby('user')['countN'].sum()
        fig_pie = px.pie(names=messages.index, values=messages.values,
                         title=f"N words per User. All n word {all_n_words}")
        fig_pie.show()
    @staticmethod
    def showPieOverNWordsOverChat(chats):
        df = Plotter.getDataFromChats(chats)
        df = df[df['countN'] != 0]
        all_n_words = 0
        for chat in chats:
            for message in chat.messages:
                all_n_words += message.countN
        messages = df.groupby('chatName')['countN'].sum()
        fig_pie = px.pie(names=messages.index, values=messages.values,
                         title=f"N words per Chat. All n word {all_n_words}")
        fig_pie.show()
    @staticmethod
    def showPieOverSlurWordsOverUser(chats):
        df = Plotter.getDataFromChats(chats)
        df = df[df['countSlurs'] != 0]
        all_slur_words = 0
        for chat in chats:
            for message in chat.messages:
                all_slur_words += message.countSlurs
        messages = df.groupby('user')['countSlurs'].sum()
        fig_pie = px.pie(names=messages.index, values=messages.values,
                         title=f"Slurs per User. All slur words {all_slur_words}")
        fig_pie.show()
    @staticmethod
    def showMessagesPerPeriod(chats,period):
        df = Plotter.getDataFromChats(chats)
        df['period'] = df['date'].dt.to_period(period)
        messages_per_period = df.groupby('period').size().reset_index(name='message_count')
        messages_per_period['period_start'] = messages_per_period['period'].apply(lambda x: x.start_time)
        fig_line_week = px.line(messages_per_period, x='period_start', y='message_count',
                                title=f"Messages per {period}. All messages: {len(df)}")
        fig_line_week.show()

    @staticmethod
    def showMessagesPerChatPerPeriod(chats,period):
        df = Plotter.getDataFromChats(chats)
        df['period'] = df['date'].dt.to_period(period)
        messages_per_period = df.groupby(['chatName','period']).size().reset_index(name='message_count')
        messages_per_period['period_start'] = messages_per_period['period'].apply(lambda x: x.start_time)
        fig_line_week = px.line(messages_per_period, x='period_start', y='message_count',color="chatName",
                                title=f"Messages per {period} per chat. All messages: {len(df)}")
        fig_line_week.show()