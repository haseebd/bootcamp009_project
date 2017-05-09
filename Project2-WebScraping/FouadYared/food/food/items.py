import scrapy

class FoodItem(scrapy.Item):
    food_categories_text = scrapy.Field()
    food_rating = scrapy.Field()
    food_name = scrapy.Field()
    food_category_text = scrapy.Field()
    food_subcategory_text = scrapy.Field()
    all_comments = scrapy.Field()
    pos_neg_comment = scrapy.Field()
    ingredients = scrapy.Field()
    certified_organic = scrapy.Field()
    allergens = scrapy.Field()
    serving_amount = scrapy.Field()
    serving_unit = scrapy.Field()
    calories = scrapy.Field()
    nutri_fat_perc = scrapy.Field()
    nutri_fat_num = scrapy.Field()
    nutri_carbs_perc = scrapy.Field()
    nutri_carbs_num = scrapy.Field()
    nutri_sugar_num = scrapy.Field()
    nutri_protein_perc = scrapy.Field()
    nutri_protein_num = scrapy.Field()
    nutri_perc_nutriName = scrapy.Field()
    nutri_addedSugars = scrapy.Field()

    Total_Fat = scrapy.Field()
    Total_Carbs = scrapy.Field()
    Sugars = scrapy.Field()
    Protein = scrapy.Field()
    Saturated_Fat = scrapy.Field()
    Cholesterol = scrapy.Field()
    Sodium = scrapy.Field()

    Added_Sugar_Ingredients = scrapy.Field()
    Dietary_Fiber = scrapy.Field()
    Vitamin_A = scrapy.Field()
    Vitamin_C = scrapy.Field()
    Calcium = scrapy.Field()
    Iron = scrapy.Field()
    Potassium = scrapy.Field()
