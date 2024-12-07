from flask import Flask, request, jsonify

from yt_dlp import YoutubeDL



app = Flask(__name__)



@app.route('/download', methods=['GET'])

def download_video():

    url = request.args.get('url')

    if not url:

        return jsonify({"error": "Missing 'url' parameter."}), 400



    # Configure yt-dlp options

    ydl_opts = {

        'quiet': True

    }



    try:

        # Get video info without downloading

        with YoutubeDL(ydl_opts) as ydl:

            info_dict = ydl.extract_info(url, download=False)

            video_title = info_dict.get('title', 'video')

            formats = info_dict.get('formats', [])



            # Extract available formats

            available_formats = [

                {

                    "format_id": fmt.get("format_id"),

                    "format_note": fmt.get("format_note"),

                    "ext": fmt.get("ext"),

                    "filesize": fmt.get("filesize"),

                    "url": fmt.get("url")

                }

                for fmt in formats

            ]



            return jsonify({

                "title": video_title,

                "available_formats": available_formats

            })



    except Exception as e:

        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':

    app.run(debug=True, host="0.0.0.0", port=8080)

