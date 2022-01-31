Partition Biospecimen
---------------------

Parition a Biospecimen into two Biospecimens

- POST /biospecimen/{biospecimen_id}
- Hit the Try it out Button to unlock the Request body fields.
- Enter the *biospecimen_id* field. (**required**)
- Modify the request body with the correct *tracking_id* and *comment fields* as shown below

.. code-block:: bash

   {
        "tracking_id": "string",
        "comment": "string"
   }

A successful response would look like: