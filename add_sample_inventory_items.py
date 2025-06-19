from db import with_cursor


@with_cursor
def add_sample_records(conn,cursor):
  # Insert the sample data
  sql = """
  INSERT INTO medicine_m (MedicineCode, MedicineName, MedicineCategory, Qty, Price, Amount, ManufactureDate, ExpiryDate, RackNumber)
  VALUES ('M1', 'Paracetamol', 'Tablet', 100, 10, 1000, '2023-01-01', '2023-12-01', 'R1'),
  ('M2', 'Ibuprofen', 'Capsule', 50, 5, 250, '2023-02-01', '2023-12-01', 'R2'),
  ('M3', 'Aspirin', 'Tablet', 25, 2, 50, '2023-03-01', '2023-12-01', 'R3'),
  ('M4', 'Amoxicillin', 'Capsule', 75, 7, 525, '2023-04-01', '2024-04-01', 'R4'),
  ('M5', 'Azithromycin', 'Suspension', 100, 10, 1000, '2023-05-01', '2024-05-01', 'R5'),
  ('M6', 'Metformin', 'Tablet', 60, 5, 300, '2023-06-01', '2024-06-01', 'R6'),
  ('M7', 'Atorvastatin', 'Tablet', 30, 5, 150, '2023-07-01', '2024-07-01', 'R7'),
  ('M8', 'Lisinopril', 'Tablet', 30, 2, 60, '2023-08-01', '2024-08-01', 'R8'),
  ('M9', 'Clopidogrel', 'Tablet', 30, 5, 150, '2023-09-01', '2024-09-01', 'R9'),
  ('M10', 'Omeprazole', 'Capsule', 30, 2, 60, '2023-10-01', '2024-10-01', 'R10')
  """
  cursor.execute(sql)

  # Commit the changes
  conn.commit()
