import tcod as libtcod

import textwrap


class Message:
    def __init__(self, text, color=libtcod.white):
        self.text = text
        self.color = color


class MessageLog:
    def __init__(self, x, width, height):
        self.messages = []
        self.x = x
        self.width = width
        self.height = height

    def add_message(self, message):
        # 必要に応じてメッセージを複数行に分割する
        new_msg_lines = textwrap.wrap(message.text, self.width)

        for line in new_msg_lines:
            # 行が溢れた場合最初の行を削除してスペース確保
            if len(self.messages) == self.height:
                del self.messages[0]

            # 新しいメッセージオブジェクトと色の指定
            self.messages.append(Message(line, message.color))

