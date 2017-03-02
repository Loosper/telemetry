from voluptuous import (
    Schema, Required, MultipleInvalid, All, Any, Number, In,
    Date, Match
)

company_mapping = {
    -1: None,
    0: 'Maverick Cardio-Telemetry',
    1: 'Maverick Water-Telemetry'
}
providers = ['Amazon', 'NewEgg']
device_types = ['cardio', 'medical', 'telemonitoring']
carriers = ['Mtel', 'Vivacom', 'Telenor']

transfer_schema = Schema({
    'couple': All(int, Number(precision=10)),
    'company': All(int, In(company_mapping.keys()))
}, required=True)

enter_device_schema = Schema({
    'id': All(int, Number(precision=10)),
    'delivery_date': All(str, Date()),
    'provider': All(str, In(providers)),
    'type': All(str, In(device_types)),
    'model': str,
    'serial': All(int, Number(precision=14))
}, required=True)

enter_sim_schema = Schema({
    'delivery_date': All(str, Date()),
    'carrier': All(str, In(carriers)),
    'number': All(str, Match(r'/08[789]\d{7}/'))
    # correct regex?
}, required=True)
