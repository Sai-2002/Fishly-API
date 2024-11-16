from src.db.setup_db import db, fs
from bson import ObjectId
import json
import base64


collection_products = db['products']

def serialize_product(product):


    image_data = fs.get(product["image_id"]).read()
    encodedImage = base64.b64encode(image_data).decode('utf-8')
    image1_data = fs.get(product["image1_id"]).read()
    encodedImage1 = base64.b64encode(image1_data).decode('utf-8')
    image2_data = fs.get(product["image2_id"]).read()
    encodedImage2 = base64.b64encode(image2_data).decode('utf-8')

    print(image_data)

    return {
        "_id": str(product["_id"]),
        "name": product["name"],
        "weight": product["weight"],
        "servings": product["servings"],
        "pieces": product["pieces"],
        "description": product["description"],
        "macros":product["macros"],
        "price" : product["price"],
        "gravy": product["gravy"],
        "fry": product["fry"],
        "barbeque": product["barbeque"],
        "image": encodedImage,
        "image1": encodedImage1,
        "image2": encodedImage2,
    }


# returning all the available prodcuts in the db
def getAll():
    products = collection_products.find({})

    products_list = [serialize_product(product) for product in products]  # Serialize each product
    
    return json.dumps(products_list), 200

def getProductById(id):

    product = collection_products.find_one({"_id": ObjectId(id)})

    return serialize_product(product=product), 200

def updateProductById(id, newValue, image, image1, image2):

    prevImageId = collection_products.find_one({"_id": ObjectId(id)})

    fs.delete(prevImageId["image_id"])
    fs.delete(prevImageId["image_id1"])
    fs.delete(prevImageId["image_id2"])

    newImageId = fs.put(image, filename = image.filename)
    newImageId1 = fs.put(image1, filename = image1.filename)
    newImageId2 = fs.put(image2, filename = image2.filename)

    newValue["image_id"] = newImageId
    newValue["image1_id"] = newImageId1
    newValue["image2_id"] = newImageId2

    result = collection_products.update_one(
        {"_id": ObjectId(id)},
        {"$set": newValue}
    )

    if result.matched_count == 0:
        return "No such product Exists"

    return "Product has been updated"

def insertProduct(product, image, image1, image2):

    image_id = fs.put(image, filename = image.filename)
    image1_id = fs.put(image1, filename = image1.filename)
    image2_id = fs.put(image2, filename = image2.filename)

    product['image_id'] = image_id
    product['image1_id'] = image1_id
    product['image2_id'] = image2_id

    collection_products.insert_one(product)
    return "Product added"

def deleteProduct(id):

    prevImageId = collection_products.find_one({"_id": ObjectId(id)})

    fs.delete(prevImageId["image_id"])

    result = collection_products.delete_one({"_id": ObjectId(id)})

    if result.deleted_count == 0:
        return json.dumps({"error": "Document not found"}), 404
    else:
        return json.dumps({"message": "Document deleted successfully"}), 200