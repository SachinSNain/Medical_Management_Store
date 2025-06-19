from db import  with_cursor


@with_cursor
def create_store_inventory_table(conn,cur):
    cur.execute(
"""
CREATE TABLE IF NOT EXISTS `medicine_m` (
  `id` int NOT NULL AUTO_INCREMENT,
  `MedicineCode` varchar(100) NOT NULL,
  `MedicineName` varchar(200) NOT NULL,
  `MedicineCategory` varchar(200) DEFAULT 'Tablet',
  `Qty` int DEFAULT NULL,
  `Price` float DEFAULT NULL,
  `Amount` float DEFAULT NULL,
  `ManufactureDate` date DEFAULT NULL,
  `ExpiryDate` date DEFAULT NULL,
  `RackNumber` varchar(200) DEFAULT NULL,
  `createdBy` varchar(100) DEFAULT 'SystemGen',
  `createdOn` date DEFAULT (curdate()),
  `updatedBy` varchar(100) DEFAULT 'SystemGen',
  `updatedOn` date DEFAULT (curdate()),
  PRIMARY KEY (`id`)
) """)


# CREATE operation (INSERT)
@with_cursor
def create_inventory(conn, cur, data):
    insert_query = """
    INSERT INTO medicine_m (MedicineCode, MedicineName, MedicineCategory, Qty, Price, Amount, ManufactureDate, ExpiryDate, RackNumber)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cur.execute(insert_query, data)
    conn.commit()

# READ operation
@with_cursor
def read_inventory(conn, cur):
    select_query = "SELECT id , MedicineCode, MedicineName, MedicineCategory, Qty, Price, Amount, ManufactureDate, ExpiryDate, RackNumber FROM medicine_m"
    cur.execute(select_query)
    result = cur.fetchall()
    return result

# UPDATE operation
@with_cursor
def update_inventory(conn, cur, medicine_id, data):
    update_query = """
    UPDATE medicine_m
    SET MedicineCode=%s, MedicineName=%s, MedicineCategory=%s, Qty=%s, Price=%s, Amount=%s,
        ManufactureDate=%s, ExpiryDate=%s, RackNumber=%s, updatedBy=%s, updatedOn=CURDATE()
    WHERE id = %s
    """
    data = data + (medicine_id,)
    cur.execute(update_query, data)
    conn.commit()

# DELETE operation
@with_cursor
def delete_inventory(conn, cur, medicine_id):
    delete_query = "DELETE FROM medicine_m WHERE id = %s"
    cur.execute(delete_query, (medicine_id,))
    conn.commit()