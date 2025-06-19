import datetime
import random
from db import  with_cursor



@with_cursor
def create_store_billing_table(conn,cur):
  cur.execute(
"""CREATE TABLE IF NOT EXISTS `billing_tran` (
  `id` int NOT NULL AUTO_INCREMENT,
  `bill_number` varchar(20) ,
  `PatientName` varchar(200) NOT NULL,
  `MobileNum` varchar(20) DEFAULT NULL,
  `Address` varchar(200) DEFAULT NULL,
  `PrescribedByDr` varchar(200) NOT NULL,
  `ModeOfPayment` varchar(100) DEFAULT NULL,
  `medicine_id` int DEFAULT NULL,
  `MedicineName` varchar(200) NOT NULL,
  `Qty` int DEFAULT NULL,
  `Price` float DEFAULT NULL,
  `Discount` float DEFAULT NULL,
  `Amount` float DEFAULT NULL,
  `createdBy` varchar(100) DEFAULT 'SystemGen',
  `createdOn` date DEFAULT (curdate()),
  `updatedBy` varchar(100) DEFAULT 'SystemGen',
  `updatedOn` date DEFAULT (curdate()),
  PRIMARY KEY (`id`)
)
"""
)



@with_cursor
def create_billing(conn,cur, bill_number, mobile_number, patient_name, address, prescribed_by_doctor, mode_of_payment,medicine_name , qty,price,discount,amount):
    """Creates a new billing record in the `billing_m` table."""

    cur.execute('INSERT INTO billing_m (billnumber, MobileNum, PatientName, Address, PrescribedByDr, ModeOfPayment,MedicineName, Qty , Price ,Discount , Amount ) VALUES (%s, %s, %s, %s, %s, %s,%s,%s,%s,%s)', (bill_number, mobile_number, patient_name, address, prescribed_by_doctor, mode_of_payment,medicine_name , qty,price,discount,amount))
    conn.commit()

@with_cursor
def read_billings(conn,cur):
    """Returns all billing records from the `billing_m` table."""

    cur.execute('SELECT * FROM billing_m')
    results = cur.fetchall()
    return results

@with_cursor
def update_billing(conn,cur, id, bill_number, mobile_number, patient_name, address, prescribed_by_doctor, mode_of_payment):
    """Updates a billing record in the `billing_m` table."""

    cur.execute('UPDATE billing_m SET bill_number = %s, mobile_number = %s, patient_name = %s, address = %s, prescribed_by_doctor = %s, mode_of_payment = %s WHERE id = %s', (bill_number, mobile_number, patient_name, address, prescribed_by_doctor, mode_of_payment, id))
    conn.commit()

@with_cursor
def delete_billing(conn,cur, id):
    """Deletes a billing record from the `billing_m` table."""

    cur.execute('DELETE FROM billing_m WHERE id = %s', (id,))

@with_cursor
def filter_billings(conn,cur, filters):
    """Returns billing records from the `billing_m` table that match the given filters."""

    where_clause = ' AND '.join(['{} = %s'.format(key) for key, value in filters.items()])

    cur.execute('SELECT * FROM billing_m WHERE {}'.format(where_clause), tuple(filters.values()))
    results = cur.fetchall()
    return results

@with_cursor
def sort_billings(conn,cur, order_by_clause):
    """Returns billing records from the `billing_m` table sorted by the given order by clause."""

    cur.execute('SELECT * FROM billing_m ORDER BY {}'.format(order_by_clause))
    results = cur.fetchall()
    return results

def generate_bill_number():
    """Generates a dynamic bill number."""

    # Get the current date and time
    current_date_time = datetime.datetime.now()

    # Create a unique identifier based on the date and time
    unique_identifier = f"{current_date_time.year}{current_date_time.month}{current_date_time.day}{current_date_time.hour}{current_date_time.minute}{current_date_time.second}{random.randint(1000, 9999)}"
    return unique_identifier