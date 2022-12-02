from flask import Blueprint, jsonify, request
from dependency_injector.wiring import inject, Provide

from flaskr.container.dependency_container import Module
from flaskr.model.user import User
from flaskr.service.account_service import AccountService

blueprint = Blueprint('account_service_routes', __name__)


@blueprint.route("/", methods=['POST'])
@inject
def create_account(account_service: AccountService = Provide[Module.account_service]):
    name = request.get_json(force=True).get('name')
    status = request.get_json(force=True).get('status')
    email = request.get_json(force=True).get('email')
    seller_rating = request.get_json(force=True).get('seller_rating')
    user_name = request.get_json(force=True).get('user_name')
    user_password = request.get_json(force=True).get('user_password')

    try:
        account_id = account_service.create_user(name, status, email, seller_rating, user_name, user_password)
    except Exception as exception:
        return jsonify(
            {
                "status": "fail",
                "message": str(exception)
            }
        ), 400

    return jsonify(
        {
            "status": "success",
            "id": str(account_id)
         }
    ), 200


@blueprint.route("/<user_id>", methods=['GET'])
@inject
def get_account(user_id: str, account_service: AccountService = Provide[Module.account_service]):
    try:
        user: User = account_service.get_user_by_id(user_id)
    except Exception as exception:
        return jsonify(
            {
                "status": "fail",
                "message": str(exception)
            }
        ), 400

    return jsonify(user.to_json()), 200


@blueprint.route("/<user_id>", methods=['PUT'])
@inject
def update_account(user_id: str, account_service: AccountService = Provide[Module.account_service]):
    name = request.get_json(force=True).get('name')
    status = request.get_json(force=True).get('status')
    email = request.get_json(force=True).get('email')
    seller_rating = request.get_json(force=True).get('seller_rating')
    user_name = request.get_json(force=True).get('user_name')
    user_password = request.get_json(force=True).get('user_password')

    try:
        account_service.update_user(user_id, name, status, email, seller_rating, user_name, user_password)
    except Exception as exception:
        return jsonify(
            {
                "status": "fail",
                "message": str(exception)
            }
        ), 400

    return jsonify({"status": "success"}), 200


@blueprint.route("/<user_id>", methods=['DELETE'])
@inject
def delete_account(user_id: str, account_service: AccountService = Provide[Module.account_service]):
    try:
        account_service.delete_user(user_id)
    except Exception as exception:
        return jsonify(
            {
                "status": "fail",
                "message": str(exception)
            }
        ), 400

    return jsonify({"status": "success"}), 200


@blueprint.route("/ping", methods=['GET'])
@inject
def ping():
    return jsonify({"status": "Ping success"}), 200
