from application.API.BusinessLogic.BusinessLogic import BusinessLogic


class LocationBL(BusinessLogic):
    def update(self, request, columnName, columnValue):
        return super().update_model(request, model_name="user",
                                    column_name=columnName,
                                    column_value=columnValue,
                                    is_dump=True, verify_user=False)
