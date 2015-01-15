import csv

from ..core.models import Tenant, Unit, ZipCode, City, Contract


def validate_csv(row0, required_fields):
    """
    :param row0:
    :param required_fields:
    :return: a tuple, True if all requirements are met and a dictionary with the index for all the fields
    """
    for field in required_fields:
        if field not in row0:
            return False, {}
    field_pos = {}
    for idx, field in enumerate(row0):
        field_pos[field] = idx
    return True, field_pos


def get_tenant_per_tenant_id(tenant_id):
    tenants = Tenant.objects.filter(tenant_id=tenant_id)
    if tenants.exists():
        return tenants[0]
    else:
        return None


def get_tenant_per_email(email):
    tenants = Tenant.objects.filter(email=email)
    if tenants.exists():
        return tenants[0]
    else:
        return None


def get_tenant_per_name(first_name, mi, last_name):
    tenants = Tenant.objects.filter(first_name=first_name, last_name=last_name, mi=mi)
    if tenants.exists():
        return tenants[0]
    else:
        return None


def get_tenant(tenant_id, first_name, mi, last_name, email):
    """
    if tenant_d then search per tenant id
    :param tenant_id:
    :param first_name:
    :param mi:
    :param last_name:
    :param email:
    :return:
    """
    if tenant_id:
        return get_tenant_per_tenant_id(tenant_id)
    elif email:
        return get_tenant_per_email(email)
    else:
        return get_tenant_per_name(first_name, mi, last_name)


def import_tenant(column_pos, row):
    tenant_id = row[column_pos['tenant_id']]
    first_name = row[column_pos['first_name']]
    last_name = row[column_pos['last_name']]
    mi = row[column_pos['mi']]
    email = row[column_pos['email']]
    tenant = get_tenant(tenant_id, first_name, mi, last_name, email)
    if not tenant:
        tenant = Tenant(
            tenant_id=tenant_id,
            first_name=first_name,
            mi=mi,
            last_name=last_name,
        )
        if email:
            tenant.email = email

        val = row[column_pos['cell_phone']]
        if val:
            tenant.cell_phone = val
        val = row[column_pos['home_phone']]
        if val:
            tenant.home_phone = val
        val = row[column_pos['work_phone']]
        if val:
            tenant.work_phone = val
        tenant.save()
    return tenant


def get_unit_by_unit_id(unit_id):
    units = Unit.objects.filter(unit_id=unit_id)
    if units.exists():
        return units[0]
    else:
        return None


def get_unit_by_address(address, apartment, city, state, zip_code):
    units = Unit.objects.filter(address=address, zip_code__city__name=city, zip_code__state=state,
                                zip_code__zip_code=zip_code)
    if apartment:
        units = units.filter(apartment=apartment)
    if units.exists():
        return units[0]
    else:
        return None


def get_unit(unit_id, address, apartment, city, state, zip_code):
    if unit_id:
        return get_unit_by_unit_id(unit_id)
    else:
        return get_unit_by_address(address, apartment, city, state, zip_code)


def get_or_create_zip_code(city_str, state, zip_code):
    city_str = city_str.title()
    cities = City.objects.filter(name=city_str)
    if cities:
        city = cities[0]
    else:
        city = City.objects.create(name=city_str)
    state = state.upper()
    codes = ZipCode.objects.filter(city=city, state=state, zip_code=zip_code)
    if codes:
        return codes[0]
    else:
        return ZipCode.objects.create(city=city, state=state, zip_code=zip_code)


def import_unit(column_pos, row):
    unit_id = row[column_pos['unit_id']]
    address = row[column_pos['address']].lower()
    apartment = row[column_pos['apartment']]
    city = row[column_pos['city']]
    state = row[column_pos['state']]
    zip_code_str = row[column_pos['zip_code']]
    unit = get_unit(unit_id, address, apartment, city, state, zip_code_str)
    if not unit:
        zip_code = get_or_create_zip_code(city, state, zip_code_str)
        unit = Unit(
            unit_id=unit_id,
            address=address,
            zip_code=zip_code
        )
        if apartment:
            unit.apartment = apartment

        unit.save()
    return unit


def import_new_admissions(filename):
    """
    The structure of the file should be like:
    [tenant_id], first_name, mi, last_name, email, cell_phone, home_phone, work_phone, first_day, last_day, unit_id or
        address, apartment, city, state, zip_code
    :param filename:
    :return:
    """
    required_fields = ['tenant_id', 'first_name', 'mi', 'last_name', 'email', 'cell_phone', 'home_phone',
                        'work_phone', 'first_day', 'last_day', 'unit_id',
                        'address', 'apartment', 'city', 'state', 'zip_code']
    with open(filename, 'rb') as csvfile:
        rows = csv.reader(csvfile, dialect='excel')
        i = 0
        for row in rows:
            if i == 0:
                row0 = row

                ok, column_pos = validate_csv(row0, required_fields)
                if not ok:
                    raise Exception('Required fields are not present in the documents')
            else:
                tenant = import_tenant(column_pos, row)
                unit = import_unit(column_pos, row)
                first_day = row[column_pos['first_day']]
                last_day = row[column_pos['last_day']]
                # current_tenant = unit.current_tenant
                contract = Contract.objects.create(tenant=tenant, unit=unit, first_day=first_day, last_day=last_day)
            i += 1



def import_move_outs(filename):
    """
    The structure of the file should be like:
    [tenant_id] or [first_name, mi, last_name], unit_id or [address, apartment, city, state, zip_code], move_out_day
    :param filename:
    :return:
    """
    pass


def import_active_contracts(filename):
    """
    The structure of the file should be like:
    [tenant_id], first_name, mi, last_name, email, cell_phone, home_phone, work_phone, first_day, last_day, unit_id or
        address, apartment, city, state, zip_code
    :param filename:
    :return:
    """
    pass


def import_housing(filename):
    """
    The structure of the file should be like:
    unit_id, address, apartment, city, state, zip_code
    :param filename:
    :return:
    """
    pass


def export_housing():
    return ""


def export_active_tenants():
    return ""