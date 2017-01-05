from voluptuous import Schema, Required, MultipleInvalid, All, Any, Number, In


company_mapping = {
    -1: None,
    0: 'Maverick Cardio-Telemetry',
    1: 'Maverick Water-Telemetry'
}

transfer_schema = Schema({
    'couple': All(int, Number(precision=10)),
    'company': All(int, In(company_mapping.keys()))
}, required=True)

enter_schema = Schema({

})
