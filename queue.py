queues = {}

def add_song(chat_id, song):
    if chat_id not in queues:
        queues[chat_id] = []
    queues[chat_id].append(song)

def get_queue(chat_id):
    return queues.get(chat_id, [])
