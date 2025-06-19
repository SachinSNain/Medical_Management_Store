# SWARAJ MEDICAL STORE APP


This App Will Serve Medical Stores to track their  inventory requiremnts and their sales metrices.

- To install app dependencies : 

```bash
python -m pip install -r requirements.txt
```

- To start the app :

```bash 
python app.py 
```

*this will bring a window to life as shown below* :
### Welcome Screen
![1699300973249](image/README/1699300973249.png)

*using the menu provided one may navigate to app*
### Menu ITEMS
![1699301020091](image/README/1699301020091.png)


### Billing View
![1699301047736](image/README/1699301047736.png)


### Inventory Management View
![1699301089867](image/README/1699301089867.png)

### Reporting view (before clicking genrate report button)
![1699301170441](image/README/1699301170441.png)

### Reporting view (after clicking generate report button )
![1699301211857](image/README/1699301211857.png)


*to populate the database with some sample records one may use the provided script  `add_sample_inventory_items.py`*
- type the following commands 

```cmd 
python 

```
then in the interactive shell run 
```python 
  from add_sample_inventory_items.py import add_sample_records
  add_sample_records()
```

to change the Database just visit the file `db.py`

---









