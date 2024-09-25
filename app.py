from config import TOKEN
from quart import Quart, jsonify
from quart_cors import cors
from telegram import Bot
import os

app = Quart(__name__)
bot = Bot(token=TOKEN)
app = cors(app, allow_origin="*") 

@app.route('/user/<int:user_id>', methods=['GET'])
async def get_user_info(user_id):
    try:
        user = await bot.get_chat(user_id)
        
        user_photos = await bot.get_user_profile_photos(user_id)
        
        avatar_url = None
        if user_photos.total_count > 0:
            file_id = user_photos.photos[0][0].file_id
            file = await bot.get_file(file_id)
            avatar_url = f"https://api.telegram.org/file/bot{TOKEN}/{file.file_path}"
        
        user_info = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'avatar_url': avatar_url
        }

        return jsonify(user_info)

    except Exception as e:
        return jsonify({'error': str(e)}), 400
    

@app.route('/token', methods=['GET'])
def get_bot_token():
    return TOKEN

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
