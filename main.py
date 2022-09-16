from api_football_oop import ApiFootball

api = ApiFootball()

api.set_params('leagues')
api.make_request()
api.save_data('leagues_converted')