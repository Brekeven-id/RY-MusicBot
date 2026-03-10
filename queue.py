queues = {}

def add(chat_id, song):
    queues.setdefault(chat_id, []).append(song)

def get(chat_id):
    return queues.get(chat_id, [])

def clear(chat_id):
    queues[chat_id] = []
