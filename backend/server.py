from flask import Flask, request, jsonify, send_from_directory
import time
import os
import redis

app = Flask(__name__, static_folder='logs')

# Follow-up questions for different reaction types
FOLLOW_UPS = {
    'sn1': ["What is the substrate?", "What is the solvent?", "What is the temperature?"],
    'sn2': ["What is the nucleophile?", "What is the leaving group?", "Is it primary or secondary carbon?"],
    'add': ["What are the reactants?", "Is a catalyst used?", "What is the expected product?"],
    'subs': ["What is the electrophile?", "What is the nucleophile?", "Any side reactions?"]
}

# Connect to Redis on port 6380
r = redis.Redis(host='localhost', port=6380, db=0, decode_responses=True)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_id = data.get('user_id')
    message = data.get('message')

    user_key = f"user:{user_id}"  # Unique key for each user
    user_data = r.hgetall(user_key)  # Retrieve user's chat state from Redis

    if not user_data:
        # Initialize user data if it's the first interaction
        user_data = {
            'reaction_type': '',
            'follow_up_index': '0',
            'log_filename': ''
        }

    reaction_type = user_data.get('reaction_type', '')
    follow_up_index = int(user_data.get('follow_up_index', 0))

    # Determine reaction type based on message
    if not reaction_type:
        if "sn1" in message.lower():
            reaction_type = 'sn1'
        elif "sn2" in message.lower():
            reaction_type = 'sn2'
        elif "add" in message.lower():
            reaction_type = 'add'
        elif "subs" in message.lower():
            reaction_type = 'subs'
        user_data['reaction_type'] = reaction_type

    # Handle follow-up questions based on reaction type
    if reaction_type:
        follow_up_messages = FOLLOW_UPS.get(reaction_type, [])

        if follow_up_index < len(follow_up_messages):
            follow_up_message = follow_up_messages[follow_up_index]

            if not user_data.get('log_filename'):
                user_data['log_filename'] = f"{user_id}_{int(time.time())}.txt"

            log_path = os.path.join('logs', user_data['log_filename'])

            # Create logs folder if it doesn't exist
            if not os.path.exists('logs'):
                os.makedirs('logs')

            # Log the conversation
            with open(log_path, 'a') as log_file:
                log_file.write(f"User: {user_id}\nMessage: {message}\nResponse: {follow_up_message}\n\n")

            follow_up_index += 1
            user_data['follow_up_index'] = str(follow_up_index)

            # Store updated user data in Redis
            r.hset(user_key, mapping=user_data)

            return jsonify({
                'done': False,
                'response': follow_up_message,
                'log': user_data['log_filename']
            })

    # End of conversation
    log_path = os.path.join('logs', user_data['log_filename'])
    with open(log_path, 'a') as log_file:
        log_file.write(f"User: {user_id}\nMessage: {message}\nResponse: No further follow-ups needed.\n")

    # Clear user data from Redis after chat is complete
    r.delete(user_key)

    return jsonify({
        'done': True,
        'log': user_data['log_filename'],
        'response': "Thank you! Log file generated."
    })

@app.route('/logs/<filename>')
def get_log(filename):
    return send_from_directory('logs', filename)

@app.route('/reset', methods=['POST'])
def reset_chat():
    user_id = request.get_json().get('user_id')
    r.delete(f"user:{user_id}")  # Reset specific user's session in Redis
    return jsonify({'status': 'success', 'message': 'Chat reset successfully'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
