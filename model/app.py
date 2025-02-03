from flask import Flask, request, jsonify
import chat_qwen
import re
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

# Qwen2.5 Model
@app.route("/chat-qwen", methods=["POST"])
def chatQwen():
    json_content = request.json
    message = json_content.get("message")
    conversation_history = json_content.get("conversation_history", "")

    # Model processing
    response = chat_qwen.answer_question_with_context(conversation_history, message)

    # Post-processing of the response
    if isinstance(response, dict) and "response" in response:
        if "Alibaba Cloud" in response["response"]:
            response["response"] = response["response"].replace("Alibaba Cloud", "Badan Pengembangan dan Pembinaan Bahasa, Kementerian Pendidikan, Kebudayaan")
        elif "please" in response["response"]:
            response["response"] = response["response"].replace("please", "ya")
        elif "Berapa harganya " in response["response"]:
            response["response"] = response["response"].replace("Berapa harganya ", "Berapa harga ")
        elif "Indonesian" in response["response"]:
            response["response"] = response["response"].replace("Indonesian", "Bahasa Indonesia")
        response["response"] = re.sub(r'"(.*?)"', r'*\1*', response["response"])

    return jsonify(response)

# @app.route("/chat-model", methods=["POST"])
# def chatModel():
#     json_content = request.json
#     message = json_content.get("message")

#     # Proses model
#     response = chat_model.answer_question_with_context(message)

#     # Cek jika response adalah dictionary dan mengandung key "response"
#     if isinstance(response, dict) and "response" in response:
#         # Ganti kata "Alibaba Cloud" jika ada dalam response
#         if "Alibaba Cloud" in response["response"]:
#             response["response"] = response["response"].replace("Alibaba Cloud", "Badan Pengembangan dan Pembinaan Bahasa, Kementerian Pendidikan, Kebudayaan")
#         elif "please" in response["response"]:
#             response["response"] = response["response"].replace("please", "ya")
#         elif "Berapa harganya " in response["response"]:
#             response["response"] = response["response"].replace("Berapa harganya ", "Berapa harga ")
#         elif "Indonesian" in response["response"]:
#             response["response"] = response["response"].replace("Indonesian", "Bahasa Indonesia")
#         # Format respons dengan menambahkan tanda * untuk setiap kata dalam tanda kutip
#         response["response"] = re.sub(r'"(.*?)"', r'*\1*', response["response"])

#     return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6845, debug=True)