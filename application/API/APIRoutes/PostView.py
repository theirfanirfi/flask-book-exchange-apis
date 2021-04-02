from flask_classful import FlaskView, route
from flask import request, jsonify
from application.API.utils import AuthorizeRequest, notLoggedIn, b64_to_data
from application.API.Factory.BLFactory import BF
from application.API.Factory.SchemaFactory import SF
class APIPostView(FlaskView):

    def index(self):
        response = dict({"isLoggedIn": True})
        user = AuthorizeRequest(request.headers)
        return 'working'

    @route('/create/', methods=['POST'])
    def create(self):
        response = dict({"isLoggedIn": True})
        user = AuthorizeRequest(request.headers)
        image = None
        if not user:
            return jsonify(notLoggedIn)

        if request.method == "POST":
            if request.form["post_title"] == "" or request.form["description"] == "":
                response.update(
                    {"isPostCreated": False, "message": "Post title and description cannot be empty."}
                )
                return jsonify(response)

            post_title = b64_to_data(request.form["post_title"])
            post_description = b64_to_data(request.form["description"])
            if request.files:
                image = request.files['image']

            if not post_title or not post_description:
                response.update(
                    {"isPostCreated": False, "message": "Post title and description cannot be empty."}
                )
                return jsonify(response)

            isPostAdded, post = BF.getBL("post").add_post(post_title, post_description, image, user)
            if isPostAdded:
                post = SF.getSchema("post", isMany=False).dump(post)
            response.update({"isPostCreated": isPostAdded, "post": post, "isError": not isPostAdded})
            return jsonify(response)
        else:
            return "invalid request"