from flask_restful import abort

from src.base.resource import BaseResource
from src.schema import AppointmentSchema, AppointmentResponseSchema, CancelAppointmentSchema, \
    RescheduleAppointmentSchema


class AppointmentResource(BaseResource):
    """

    """

    serializers = {
        "default": AppointmentSchema,
        "response": AppointmentResponseSchema,
        "cancel": CancelAppointmentSchema,
        "reschedule": RescheduleAppointmentSchema,
    }

    def save(self, data, user_context=None):
        """

        :param data:
        :type data:
        :param user_context:
        :type user_context:
        :return:
        :rtype:
        """

        return self.service_klass.register(data=data)

    def cancel(self, obj_id, data, user_context=None):
        """

        :param obj_id:
        :param data:
        :param user_context:
        :return:
        """
        if not self.service_klass.find_one(id=obj_id, customer_id=data.get("customer_id")):
            abort(401, message='not allowed to cancel')
        data['user'] = user_context
        return self.service_klass.cancel(obj_id, data)

    def reschedule(self, obj_id, data, user_context=None):
        """

        :param obj_id:
        :param data:
        :param user_context:
        :return:
        """
        if not self.service_klass.find_one(id=obj_id, customer_id=data.get("customer_id")):
            abort(401, message='not allowed to reschedule')
        data['user'] = user_context
        return self.service_klass.reschedule(obj_id, data)