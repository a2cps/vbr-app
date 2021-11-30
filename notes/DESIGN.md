Each endpoint will be powered by at least one pgREST-based view
Views will be managed via code maintained with this application
Models will be generated for a subset of classes by automated means
All endpoints will require a Tapis Token

System will have a set of roles, keyed on Tapis username
token -> get user -> get roles
return (token, user, roles)

I think I can use custom roles defined by Tapis SK

VBR_READ
VBR_READ_RESTRICTED
VBR_MANAGE

shipments/
    contents/
        containers/
            biosamples/
                measurements/
    history/

common query params:
tracking_id
local_id

integrating identifier is local_id

/shipments?tracking_id=999999999
/shipment/B3hJ7Jkhxj

NIH GDC
sample -> portion

biosample -> sample
measurement -> portion

In our data model, a biosample is a virtual parent to which collection-time metadata are attached. The kit, redcap variables, case ID, case Event. 

Each biosample is divided into measurements (aka portions, but actually some are already analytes). These are individually tracked and handled by the VBR system. Each measurement can be subdivided, depleted, retired, etc. 

To find out how many X are in a biosample, query count of measurements whose status is not retired. 

/biosamples -> 
Biosample
    Redcap.{fields}
    

/biospecimens? -> I think this actually maps to measurements
    tracking_id
    local_id
    box_tracking_id
    box_local_id
    shipment_tracking_id
    shipment_local_id
    case_guid

