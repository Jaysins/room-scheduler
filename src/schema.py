from marshmallow import Schema, EXCLUDE, fields as _fields, validates_schema, ValidationError
from .models import Appointment
from datetime import datetime


class ExcludeSchema(Schema):
    class Meta:
        unknown = EXCLUDE


class CustomerResponseSchema(ExcludeSchema):
    id = _fields.String(required=False, allow_none=True)
    date_created = _fields.DateTime(required=False,
                                    allow_none=True)
    name = _fields.String(required=True, allow_none=False)
    email = _fields.String(required=True, allow_none=False)
    phone = _fields.String(required=True, allow_none=False)


class AppointmentSchema(ExcludeSchema):
    """ Schema for creating and storing information
    about an appointment. """

    name = _fields.String(required=True, allow_none=False)
    email = _fields.String(required=True, allow_none=False)
    phone = _fields.String(required=True, allow_none=False)
    room_id = _fields.String(required=True, allow_none=False)
    appointment_time = _fields.DateTime(required=True, allow_none=False)

    @validates_schema()
    def validate_schema(self, data, **kwargs):
        """

        """
        room_id = data['room_id']
        appointment_time = data['appointment_time']
        if Appointment.query.filter_by(
                room_id=room_id, status='scheduled',
                appointment_time=appointment_time.replace(hour=0, minute=0, second=0)
        ).first():
            raise ValidationError(
                message="Room unavailable",
                field_names=["room_id"]
            )


class CancelAppointmentSchema(ExcludeSchema):
    customer_id = _fields.String(required=True, allow_none=False)


class RescheduleAppointmentSchema(ExcludeSchema):
    customer_id = _fields.String(required=True, allow_none=False)
    appointment_time = _fields.DateTime(required=True, allow_none=False)
    room_id = _fields.String(required=True, allow_none=False)
    @validates_schema()
    def validate_schema(self, data, **kwargs):
        """

        """
        room_id = data['room_id']
        appointment_time = data['appointment_time']
        if Appointment.query.filter_by(
                room_id=room_id, status='scheduled',
                appointment_time=appointment_time.replace(hour=0, minute=0, second=0)
        ).first():
            raise ValidationError(
                message="Room unavailable",
                field_names=["room_id"]
            )


class AppointmentResponseSchema(AppointmentSchema):
    """ Schema for returning appointment
    information including metadata. """

    pk = _fields.String(required=False, allow_none=True)
    status = _fields.String(required=True, allow_none=False)
    appointment_time = _fields.DateTime(required=True, allow_none=False)
    customer = _fields.Nested(CustomerResponseSchema, required=False, )
    date_created = _fields.DateTime(required=True, allow_none=False)
    last_updated = _fields.DateTime(required=True, allow_none=False)
