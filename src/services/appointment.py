from ..base.service import ServiceFactory
from ..models import Appointment, db, Customer

BaseAppointmentService = ServiceFactory.create_service(Appointment, db_session=db)
BaseCustomerService = ServiceFactory.create_service(Customer, db_session=db)


class CustomerService(BaseCustomerService):

    @classmethod
    def register(cls, data, **kwargs):
        """

        :param data:
        :param kwargs:
        :return:
        """
        email = data['email']

        # Handle customer creation or retrieval
        if customer := cls.find_one(email=email):
            return customer
        return cls.create(**data)


class AppointmentService(BaseAppointmentService):
    """
    Service class to handle business logic for Appointment entities.
    """

    @classmethod
    def register(cls, data, **kwargs):
        """

        :param data:
        :param kwargs:
        :return:
        """

        room_id = data['room_id']
        appointment_time = data['appointment_time']
        customer = CustomerService.register(data=dict(email=data['email'],
                                                      phone=data['phone'],
                                                      name=data['name']))
        # Create the appointment
        return cls.create(customer_id=customer.id, room_id=room_id,
                          status='scheduled',
                          appointment_time=appointment_time)

    @classmethod
    def cancel(cls, obj_id, data, **kwargs):
        """

        :param obj_id:
        :param data:
        :param kwargs:
        :return:
        """

        return cls.update(obj_id, status='cancelled')

    @classmethod
    def reschedule(cls, obj_id, data, **kwargs):
        """

        :param obj_id:
        :param data:
        :param kwargs:
        :return:
        """

        return cls.update(obj_id, appointment_time=data['appointment_time'])
