from config import TOKEN
from quart import Quart, jsonify
from quart_cors import cors
from telegram import Bot
import requests
import aiohttp
import os

app = Quart(__name__)
bot = Bot(token=TOKEN)
app = cors(app, allow_origin="*")


async def get_avatar_url(user_id: int):
    try:
        user_photos = await bot.get_user_profile_photos(user_id)
        if user_photos.total_count > 0:
            file_id = user_photos.photos[0][0].file_id
            file = await bot.get_file(file_id)
            return f"{file.file_path}"
    except Exception as e:
        return None

@app.route('/user/<int:user_id>', methods=['GET'])
async def get_user_info(user_id: int):
    print(f"Received request for user: {user_id}")
    try:
        user = await bot.get_chat(user_id)
        avatar_url = await get_avatar_url(user_id)

        user_info = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'avatar_url': avatar_url
        }

        return jsonify(user_info)
    except Exception as e:
        print(f"Error in get_user_info: {e}")
        return jsonify({'error': str(e)}), 400

@app.route('/get_user_avatar/<int:user_id>')
async def get_user_avatar(user_id: int):
    print(f"Received request for avatar of user: {user_id}")
    try:
        avatar_url = await get_avatar_url(user_id)
        print(f"Avatar URL: {avatar_url}")
        if not avatar_url:
            return jsonify({'error': 'Avatar not found'}), 404

        async with aiohttp.ClientSession() as session:
            async with session.get(avatar_url) as response:
                if response.status == 200:
                    content = await response.read()
                    return content, 200, {'Content-Type': 'image/jpeg'}
                else:
                    return jsonify({'error': f'Failed to fetch avatar. Status code: {response.status}'}), 400
    except Exception as e:
        print(f"Error in get_user_avatar: {e}")
        return jsonify({'error': str(e)}), 500



@app.route('/token', methods=['GET'])
def get_bot_token():
    return TOKEN


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
