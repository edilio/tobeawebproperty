import csv
from django.db.models import Q

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
    tenants = Tenant.objets.filter(tenant_id=tenant_id)
    if tenants.exists():
        return tenants[0]
    else:
        return None


def get_tenant_per_email(email):
    tenants = Tenant.objets.filter(email=email)
    if tenants.exists():
        return tenants[0]
    else:
        return None


def get_tenant_per_name(first_name, mi, last_name):
    tenants = Tenant.objets.filter(first_name=first_name, last_name=last_name, mi=mi)
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


def import_new_admissions(filename):
    """
    The structure of the file should be like:
    [tenant_id], first_name, mi, last_name, email, cell_phone, home_phone, work_phone, first_day, last_day, unit_id or
        address, apartment, city, state, zip_code
    :param filename:
    :return:
    """
    with open('eggs.csv', 'rb') as csvfile:
        rows = csv.reader(csvfile, dialect='excel')
        row0 = rows[0]
        required_fields = ['tenant_id', 'first_name', 'mi', 'last_name', 'email', 'cell_phone', 'home_phone',
                           'work_phone', 'first_day', 'last_day', 'unit_id',
                           'address', 'apartment', 'city', 'state', 'zip_code']
        ok, column_pos = validate_csv(row0, required_fields)
        if ok:
            for row in rows[1:]:
                tenant = import_tenant(column_pos, row)


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