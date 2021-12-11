from phonenumber_field.formfields import PhoneNumberField


class BRPhoneNumberField(PhoneNumberField):

    def to_python(self, value):
        if value:
            value = "+55" + value
        return super().to_python(value)
