import csv
from django.utils import timezone

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
    if first_name:
        first_name = first_name.capitalize()
    last_name = row[column_pos['last_name']]
    if last_name:
        last_name = last_name.capitalize()
    mi = row[column_pos['mi']]
    if mi:
        mi = mi.upper()
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
    :param filename: can be an string representing the full path of the file or a file from django
    :return:
    """
    def real_import(reader):
        i = 0
        for row in reader:
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
                active_contracts = unit.active_contracts(first_day, last_day)
                for contract in active_contracts:
                    contract.move_out_date = first_day
                    contract.save()
                Contract.objects.create(tenant=tenant, unit=unit, first_day=first_day, last_day=last_day)
            i += 1

    required_fields = ['tenant_id', 'first_name', 'mi', 'last_name', 'email', 'cell_phone', 'home_phone',
                       'work_phone', 'first_day', 'last_day', 'unit_id',
                       'address', 'apartment', 'city', 'state', 'zip_code']
    if isinstance(filename, str):
        with open(filename, 'rb') as csvfile:
            rows = csv.reader(csvfile, dialect='excel')
            real_import(rows)
    else:
        rows = csv.reader(filename, dialect='excel')
        real_import(rows)


def import_move_outs(filename):
    """
    The structure of the file should be like:
    [tenant_id] or [first_name, mi, last_name] or email, unit_id or [address, apartment, city, state, zip_code],
    move_out_day
    :param filename:
    :return:
    """
    required_fields = ['tenant_id', 'first_name', 'mi', 'last_name', 'email', 'unit_id',
                       'address', 'apartment', 'city', 'state', 'zip_code',
                       'move_out_day']

    def real_import(reader):
        i = 0
        for row in reader:
            if i == 0:
                row0 = row

                ok, column_pos = validate_csv(row0, required_fields)
                if not ok:
                    raise Exception('Required fields are not present in the documents')
            else:
                tenant = import_tenant(column_pos, row)
                unit = import_unit(column_pos, row)
                move_out_day = row[column_pos['move_out_day']]
                contract = unit.current_contract
                if contract and contract.tenant == tenant:
                    contract.move_out_date = move_out_day
                    contract.save()
                else:
                    active_contracts = Contract.objecta.filter(tenant=tenant, unit=unit).order_by('-last_day')
                    if active_contracts.exists():
                        contract = active_contracts[0]
                        contract.move_out_date = move_out_day
                        contract.save()
            i += 1


    if isinstance(filename, str):
        with open(filename, 'rb') as csvfile:
            rows = csv.reader(csvfile, dialect='excel')
            real_import(rows)
    else:
        rows = csv.reader(filename, dialect='excel')
        real_import(rows)


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


def value(x):
    if x:
        return x
    else:
        return ""


def export_housing(filename_or_response):
    """
    :param filename_or_response: can be a real filename or a django response
    :return:
    """
    def export(writer):
        row = ['unit_id', 'address', 'apartment', 'city', 'state', 'zip_code']
        writer.writerow(row)
        for unit in Unit.objects.all():
            code = unit.zip_code
            row = [value(unit.unit_id),
                   unit.address, value(unit.apartment), code.city.name, code.state, code.zip_code]
            print(row)
            writer.writerow(row)

    if isinstance(filename_or_response, str):
        with open(filename_or_response, 'wb') as f:
            csv.writer(f)
    else:
        w = csv.writer(filename_or_response, dialect='excel')
        export(w)


def export_active_tenants(filename_or_response):
    """
    :param filename_or_response: can be a real filename or a django response
    :return:
    """
    def export(writer):
        now = timezone.now()
        active_contracts = Contract.objects.filter(first_day__lt=now, last_day__gt=now)
        row = ['tenant_id', 'first_name', 'mi', 'last_name', 'email',
               'cell_phone', 'home_phone', 'work_phone',
               'contract_first_day', 'contract_last_day',
               'unit_id', 'address', 'apartment', 'city', 'state', 'zip_code']
        writer.writerow(row)
        for contract in active_contracts:
            tenant = contract.tenant
            unit = contract.unit
            code = unit.zip_code
            row = [value(tenant.tenant_id), tenant.first_name, tenant.mi, tenant.last_name, tenant.email,
                   value(tenant.cell_phone), value(tenant.home_phone), value(tenant.work_phone),
                   contract.first_day.strftime('%Y-%m-%d'), contract.last_day.strftime('%Y-%m-%d'),
                   value(unit.unit_id),
                   unit.address, value(unit.apartment), code.city.name, code.state, code.zip_code]
            print(row)
            writer.writerow(row)

    if isinstance(filename_or_response, str):
        with open(filename_or_response, 'wb') as f:
            w = csv.writer(f, dialect='excel')
            export(w)
    else:
        w = csv.writer(filename_or_response, dialect='excel')
        export(w)