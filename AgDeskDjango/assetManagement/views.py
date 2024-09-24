import datetime
from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from .models import SmallEquipment, LargeEquipment, lightVehicle, heavyVehicle
from . import forms
from UserAuth.models import UserProfile
from FarmAcc.models import FarmInfo
from assetOperation.models import OperationLog
from assetOperation.forms import checkOutForm
from itertools import chain
from django.contrib import messages


class AssetStructures():

    assetLabelMapper = {
        "SE": "Small Equipment",
        "LE": "Large Equipment",
        "LV": "Standard Vehicles",
        "HV": "Heavy Vehicles"
    }

    assetModelMapper = {
        "SE": SmallEquipment,
        "LE": LargeEquipment,
        "LV": lightVehicle,
        "HV": heavyVehicle
    }

    assetCreationFormMapper = {
        "SE": forms.createSmallAssetForm,
        "LE": forms.createLargeAssetForm,
        "LV": forms.createLightVehicleForm,
        "HV": forms.createHeavyVehicleForm
    }

    assetEditFormMapper = {
        "SE": forms.editSmallAssetForm,
        "LE": forms.editLargeAssetForm,
        "LV": forms.editLightVehicleForm,
        "HV": forms.editHeavyVehicleForm
    }

    # Used to generate asset forms when they are part of a POST request.
    def generatePOSTForm(self, assetClass, request, postRequest = None, additionalrequest = None, formType = "create", ):
        if formType == "create":
            return AssetStructures.assetCreationFormMapper.get(assetClass)(request, postRequest , additionalrequest)
        elif formType == "edit":
            return AssetStructures.assetEditFormMapper    .get(assetClass)(request, postRequest , additionalrequest)
        else:
            raise Exception("Invalid formType")

# I'm not sure where this docstring belongs, or if it even is a docstring.
"""
- Asset Category should be passed in via the URL as one of the following.
    - SE
    - LE
    - SV
    - HV
    - ALL
Capitalisation is not relevant. This is handled in the below method.
"""

# If the uncommented code is not working, try the commented code.
# Uncommented code has not been tested yet
class AssetManager():

    def retrieveAssets(self, assetCategory, currentUser):
        """
        This function will indiscriminately return all assets of a given type from the farm
        type = Large or Small Equipment & Heavy or standard Vehicles.
        """

        currentFarmID = currentUser.currentFarm_id
        assetStructures = AssetStructures()
        queryCategory = None
        for key, value in assetStructures.assetModelMapper.items():
            if key == assetCategory:
                queryCategory = value.objects.filter(farmID = currentFarmID, deleted = 0).values()

        if assetCategory == "all":
            #Query for all assets
            allAssetsQuerySet = chain(
                SmallEquipment.objects.filter(farmID = currentFarmID).values(), 
                LargeEquipment.objects.filter(farmID = currentFarmID).values(), 
                lightVehicle  .objects.filter(farmID = currentFarmID).values(), 
                heavyVehicle  .objects.filter(farmID = currentFarmID).values()
            )

            return allAssetsQuerySet
        else:
            return queryCategory

    def retrieveAssetByID(self, assetCategory, currentUser, assetID):
        assetStructures = AssetStructures()
        currentFarmID = currentUser.currentFarm_id
        assetValues = assetStructures.assetModelMapper.get(assetCategory).objects.get(farmID=currentFarmID, assetID=assetID).__dict__
        assetValues["datePurchased"] = assetValues["datePurchased"].strftime("%d/%m/%Y")
        assetValues["dateManufactured"] = assetValues["dateManufactured"].strftime("%d/%m/%Y")

        return assetValues

    def createAsset(self, assetCategory, assetData):
        """
        creates a new asset in the database.
        takes assetData as an argument.
        asset data: information passed in from the front-end containing data about the task via a request.
        asset data should open with a title of what class of asset is being added -> this will be passed through the url.
        asset data is a dictionary that must adhere to the following formats depoending on whether it is a small/large asset or a vehicle/heavy vehicle.

        All Asset Dictionaries must contain the following:
        {
        "assetID": <insert value>,
        "assetName": <insert value>,
        "farmID": <insert value>,
        "datePurchased": <insert value>,
        }

        All vehicle asset dictionaries must contain the following in addition to the asset dictionary contents:
        {
        vin: <insert value>,
        Manufacturer: <insert value>,
        Age: <insert value>,
        partsList: <insert value>,
        Location: <insert value>,
        }

        the following information should be added conditional to the asset class.

        Small Asset:
        {
        "serialNumber": <insert value>,
        "Manufacturer": <insert value>,
        "Age": <insert value>,
        "partsList": <insert value>,
        "Location": <insert value>
        }

        Large Asset:
        {
        vin: <insert value>,
        Manufacturer: <insert value>,
        Age: <insert value>,
        partsList: <insert value>,
        Location: <insert value>
        }

        Light Vehicle:
        {
        currentlyInUse: <insert value>
        }

        Heavy Vehicle:
        {
        interFarmTransport: <insert value>
        }
        """

        farmQuery = FarmInfo.objects.filter(id = assetData["farmID"])

        if assetCategory == "SE":
            newSmallEquipment = SmallEquipment(
                assetPrefix      = "SE",
                assetName        = assetData["formData"]["assetName"       ], 
                farmID           = farmQuery[0], 
                dateManufactured = assetData["formData"]['dateManufactured'],
                datePurchased    = assetData["formData"]['datePurchased'   ], 
                serialNumber     = assetData["formData"]["serialNumber"    ], 
                Manufacturer     = assetData["formData"]["Manufacturer"    ], 
                partsList        = assetData["formData"]["partsList"       ], 
                Location         = assetData["formData"]["Location"        ],
                assetImage       = assetData["formData"]["assetImage"      ]
            )
            newSmallEquipment.save()

        elif assetCategory == "LE":
            newLargeEquipment = LargeEquipment(
                assetPrefix      = "LE",
                assetName        = assetData["formData"]["assetName"       ], 
                farmID           = farmQuery[0], 
                dateManufactured = assetData["formData"]['dateManufactured'],
                datePurchased    = assetData["formData"]['datePurchased'   ], 
                vin              = assetData["formData"]["vin"             ], 
                Manufacturer     = assetData["formData"]["Manufacturer"    ], 
                partsList        = assetData["formData"]["partsList"       ], 
                Location         = assetData["formData"]["Location"        ],
                assetImage       = assetData["formData"]["assetImage"      ]
            )
            newLargeEquipment.save()

        elif assetCategory == "LV":
            newLightVehicle = lightVehicle(
                assetPrefix      = "LV",
                assetName        = assetData["formData"]["assetName"       ], 
                farmID           = farmQuery[0], 
                dateManufactured = assetData["formData"]['dateManufactured'],
                datePurchased    = assetData["formData"]['datePurchased'   ], 
                vin              = assetData["formData"]["vin"             ], 
                Manufacturer     = assetData["formData"]["Manufacturer"    ], 
                partsList        = assetData["formData"]["partsList"       ], 
                Location         = assetData["formData"]["Location"        ],
                Registration     = assetData["formData"]["Registration"    ],
                currentlyInUse   = assetData["formData"]["currentlyInUse"  ],
                assetImage       = assetData["formData"]["assetImage"      ]
            )
            newLightVehicle.save()

        elif assetCategory == "HV":
            newHeavyVehicle = heavyVehicle(
                assetPrefix        = "HV",
                assetName          = assetData["formData"]["assetName"         ], 
                farmID             = farmQuery[0],
                dateManufactured   = assetData["formData"]['dateManufactured'  ], 
                datePurchased      = assetData["formData"]['datePurchased'     ], 
                vin                = assetData["formData"]["vin"               ], 
                Manufacturer       = assetData["formData"]["Manufacturer"      ], 
                partsList          = assetData["formData"]["partsList"         ], 
                Location           = assetData["formData"]["Location"          ],
                Registration       = assetData["formData"]["Registration"      ],
                inTransport        = assetData["formData"]["inTransport"       ],
                interFarmTransport = assetData["formData"]["interFarmTransport"],
                assetImage         = assetData["formData"]["assetImage"        ]
            )
            newHeavyVehicle.save()

    def editAsset(self, assetCategory,  assetData, assetID):
        assetStructures = AssetStructures()
        targetAsset = assetStructures.assetModelMapper.get(assetCategory).objects.get(assetID=assetID)

        if assetData["assetImage"] == None:
            assetData["assetImage"] = "images/asset_images/defaultImage.jpg"

        if assetCategory == "SE":
            #Edit a small equipment object
            targetAsset.assetName        = assetData["assetName"       ]
            targetAsset.dateManufactured = assetData["dateManufactured"]
            targetAsset.datePurchased    = assetData["datePurchased"   ]
            targetAsset.serialNumber     = assetData["serialNumber"    ]
            targetAsset.Manufacturer     = assetData["Manufacturer"    ]
            targetAsset.partsList        = assetData["partsList"       ]
            targetAsset.Location         = assetData["Location"        ]
            targetAsset.assetImage       = assetData["assetImage"      ]

        elif assetCategory == "LE":
            #update target asset fields.
            targetAsset.assetName     = assetData["assetName"    ]
            targetAsset.datePurchased = assetData["datePurchased"]
            targetAsset.vin           = assetData["vin"          ]
            targetAsset.Manufacturer  = assetData["Manufacturer" ]
            targetAsset.partsList     = assetData["partsList"    ]
            targetAsset.Location      = assetData["Location"     ]
            targetAsset.assetImage    = assetData["assetImage"   ]

        elif assetCategory == "LV":
            #update target asset fields.
            targetAsset.assetName      = assetData["assetName"     ]
            targetAsset.datePurchased  = assetData["datePurchased" ]
            targetAsset.vin            = assetData["vin"           ]
            targetAsset.Manufacturer   = assetData["Manufacturer"  ]
            targetAsset.partsList      = assetData["partsList"     ]
            targetAsset.Location       = assetData["Location"      ]
            targetAsset.Registration   = assetData["Registration"  ]
            targetAsset.currentlyInUse = assetData["currentlyInUse"]
            targetAsset.assetImage     = assetData["assetImage"    ]

        elif assetCategory == "HV":
            #update target asset fields.
            targetAsset.assetName          = assetData["assetName"         ]
            targetAsset.datePurchased      = assetData["datePurchased"     ]
            targetAsset.vin                = assetData["vin"               ]
            targetAsset.Manufacturer       = assetData["Manufacturer"      ]
            targetAsset.partsList          = assetData["partsList"         ]
            targetAsset.Location           = assetData["Location"          ]
            targetAsset.Registration       = assetData["Registration"      ]
            targetAsset.inTransport        = assetData["inTransport"       ]
            targetAsset.interFarmTransport = assetData["interFarmTransport"]
            targetAsset.assetImage         = assetData["assetImage"        ]

        targetAsset.save()

    def deleteAsset(self, assetID, assetCategory):
        """
        Soft deletes a task from the database by setting the deleted field to True.
        """

        assetStructures = AssetStructures()
        targetAsset = assetStructures.assetModelMapper.get(assetCategory).objects.get(assetID=assetID)

        try:
            targetAsset.deleted = True
            targetAsset.save()

            return {"deletionStatus": "Success"}
        except:
            return {"deletionStatus": "Failed, Asset already deleted."}

    def calculateAssetAge(self, assetClass, assetID):
        """
        This function will calculate the age of an asset based on the date of manufacture or  purchase.
        """

        assetStructures = AssetStructures()
        target = assetStructures.assetModelMapper.get(assetClass).objects.get(assetID=assetID)
        currentDate = datetime.date.today()

        if target.dateManufactured is not None:
            age = currentDate - target.dateManufactured
        #else block is for assets where the date of manufacture is unkown
        else:
            age = currentDate - target.datePurchased

        return age


# View functions
def displayAssets(request, assetCategory):
    """
    This view is responsible for displaying all assets of a given class that are currently on the farm.
    It also allows the user to create new assets of a given class. From this view, users can navigate to editing an
    asset or deleting an asset.

    The asset Category is passed into this function via the URL. This is used to determine what assets to display.

    request methods: GET, POST
    request data format: {
        "assetData": {
            "assetName": <string>,
            "datePurchased": <date>,
            "age": <int>,
            "manufacturer": <string>,
            "location": <string>,
            "partsList": <string>,
        }
    }

    Asset Class specific fields should also be passed into request in their respective formats.
    This and the above asset data should be contained in the dictionary as one item, example given at the end.
        small asset request data: {
            "serialNumber": <string>,
        }

        large asset request data: {
            "vin": <string>,
        }

        light vehicle request data: {
            "registration": <string>,
            "currentlyInUse": <bool>
        }

        heavy vehicle request data: {
            "registration": <string>,
            "inTransport": <bool>,
            "interFarmTransport": <bool>
        }

        request: {
            "assetData": {
                "assetName": <string>,
                "datePurchased": <date>,
                "age": <int>,
                "manufacturer": <string>,
                "location": <string>,
                "partsList": <string>,
                "registration": <string>,
                "inTransport": <bool>,
                "interFarmTransport": <bool>
            }
        }
    """

    assetManager = AssetManager()
    assetStructures = AssetStructures()
    currentUser = UserProfile.objects.get(id=request.user.id)

    ### Get Request ###
    if request.method == "GET":
        creationForm = assetStructures.assetCreationFormMapper.get(assetCategory)(request.user)

        assets = assetManager.retrieveAssets(assetCategory, currentUser)
        for asset in assets:
            for key, value in asset.items():
                if key == "dateManufactured" or key == "datePurchased":
                    assetManager.calculateAssetAge(assetCategory, asset["assetID"])

            # True if being used, False if NOT being used
            lastLog = OperationLog.objects.filter(assetID=asset["assetID"], endDateTime__isnull=True)
            asset["opStatus"] = len(lastLog) > 0

        checkoutForm = checkOutForm()

        context = {
            'assetList'    : assets,
            'assetCategory': assetCategory,
            'assetForm'    : assetStructures.assetCreationFormMapper.get(assetCategory),
            'assetLabel'   : assetStructures.assetLabelMapper.get(assetCategory),

            'checkoutForm' : checkoutForm
        }

        return render(request, 'assetManagement/assetOverview.html', context)

    ### Post Request ###
    elif request.method == "POST":
        creationForm = assetStructures.generatePOSTForm(assetCategory, request.user, request.POST, request.FILES, "create")
        if creationForm.is_valid():
            context = {
                "farmID": currentUser.currentFarm_id,
                "formData": creationForm.cleaned_data
            }
            assetManager.createAsset(assetCategory, context)
            messages.add_message(request, messages.SUCCESS, "New Asset Created.")
        # This is for debugging - tells what is broken in the form, why it is invalid.
        else:
            print(creationForm.errors)

        return redirect(f'/asset/{assetCategory}')

    context = {
                "creationForm": creationForm,
    }

    return render(request, 'assetManagement/assetOverview.html', context)


def createAsset(request):
    assetManager = AssetManager()
    currentUser = UserProfile.objects.get(id=request.user.id)


def viewAsset(request, assetCategory, assetID):
    assetManager = AssetManager()
    assetStructures = AssetStructures()
    currentUser = UserProfile.objects.get(id=request.user.id)
    asset = assetManager.retrieveAssetByID(assetCategory, currentUser, assetID)
    # Get the form for the asset type & set the initial values of the form to the asset values.
    form = assetStructures.assetEditFormMapper.get(assetCategory)(initial=asset)

    ### Get Request ###
    if request.method == "GET":
        context = {
            'currentAsset' : asset,
            'assetCategory': assetCategory,
            'assetForm'    : form,
            'assetLabel'   : assetStructures.assetLabelMapper.get(assetCategory)
        }

        return render(request, 'assetManagement/assetDetails.html', context)

    if request.method == "POST":
        form = assetStructures.generatePOSTForm(assetCategory, request.user, request.POST, request.FILES, "edit")

        # Edit Asset
        if "Update" in request.POST: 
            if form.is_valid():
                assetManager.editAsset(assetCategory, form.cleaned_data, assetID)
                messages.add_message(request, messages.SUCCESS, "Successfully saved.")
            else:
                print(form.errors)

            return redirect(f'/asset/{assetCategory}/{assetID}/details')

        # Delete Asset
        elif "delete" in request.POST: # Delete Asset
            assetManager.deleteAsset(assetID, assetCategory)
            messages.add_message(request, messages.WARNING, "Asset Deleted")

            return redirect(f'/asset/{assetCategory}')

        return redirect(f'/asset/{assetCategory}/{assetID}/details')

    return render(request, 'assetManagement/assetDetails.html')
