from src.resources.appointment import AppointmentResource
from src.services.appointment import AppointmentService
from src.base.middleware import AuthMiddleware
import settings
from src import app, api

app.wsgi_app = AuthMiddleware(
    app.wsgi_app, settings=settings,
    ignored_endpoints=["/register", "/appointments"])


appointment = AppointmentResource.initiate(
    serializers=AppointmentResource.serializers,
    service_klass=AppointmentService)
api.add_resource(appointment, '/appointments',
                 '/appointments/<string:obj_id>',
                 '/appointments/<string:obj_id>/<string:resource_name>')


if __name__ == '__main__':
    app.run(debug=True)