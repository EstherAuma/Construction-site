import requests
from .models import AggregatedContent
from decouple import config

class StrapiAPI:
    def __init__(self):
        self.url = config('STRAPI_URL')
        self.access_token = config('STRAPI_ACCESS_TOKEN')
        self.headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
    
    def get_content(self):
        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            content = data.get('data', [])
          
            formatted_data = {}

            for item in content:
                custom_type = item.get('custom_type')
                locale = item.get('locale') 
                print(f"Processing {custom_type}")
             
                if locale not in formatted_data:
                    formatted_data[locale] = []

                content_item = None

                if custom_type == "form_questions":
                    content_item = {
                        "id": item.get("id"),
                        "theme": item.get("theme"),
                        "locale": locale,
                        "page_id": item.get("page_id"),
                        "createdAt": item.get("createdAt"),
                        "updatedAt": item.get("updatedAt"),
                        "page_title": item.get("page_title"),
                        "published_at": item.get("published_at"),
                        "custom_type": custom_type,
                        "publishedAt": item.get("publishedAt"),
                        "dynamic_zone": []  
                    }

                    for component in item.get("dynamic_zone", []):
                        component_data = {
                            "id": component.get("id"),
                            "Key": component.get("Key"),
                            "Label": component.get("Label"),
                            "Options": component.get("Options"),
                            "Category": component.get("Category"),
                            "HelpText": component.get("HelpText"),
                            "Required": component.get("Required"),
                            "Placeholder": component.get("Placeholder"),
                            "__component": component.get("__component"),
                            "QuestionType": component.get("QuestionType"),
                            "DisplayQuestion": component.get("DisplayQuestion"),
                            "OptionTranslations": component.get("OptionTranslations"),
                            "repeatable_zone": [] 
                        }

                        if "repeatable_zone" in component:
                            for repeatable_item in component["repeatable_zone"]:
                                repeatable_data = {
                                    "id": repeatable_item.get('id'),
                                    "key": repeatable_item.get('key'),
                                    "value": repeatable_item.get('value')
                                }
                                component_data["repeatable_zone"].append(repeatable_data)
                                
                        content_item["dynamic_zone"].append(component_data)

                elif custom_type == "common_text":
                    content_item = {
                        "id": item.get("id"),
                        "locale": locale,
                        "page_title": item.get("page_title"),
                        "custom_type": custom_type,
                        "dynamic_zone": []
                    }

                    for component in item.get("dynamic_zone", []):
                        component_data = {
                            "id": component.get("id"),
                            "key": component.get("key"),
                            "value": component.get("value"),
                            "__component": component.get("__component")
                        }
                        content_item["dynamic_zone"].append(component_data)

                elif custom_type == "menu_content":
                    content_item = {
                        "page_title": item.get("page_title"),
                        "published_at": item.get("published_at"),
                        "cover_image": item.get("cover_image"),
                        "custom_type": custom_type,
                        "publishedAt": item.get("publishedAt"),
                        "title_audio": item.get("title_audio"),
                        "dynamic_zone": []
                    }

                    for component in item.get("dynamic_zone", []):
                        component_data = {
                            "id": component.get("id"),
                            "url": component.get("Url"),
                            "Icon": component.get("Icon"),
                            "Order": component.get("Order"),
                            "Title": component.get("Title"),
                            "Enabled": component.get("Enabled"),
                            "__component": component.get("__component"),
                            "Label(Translate)": component.get("Label(Translate)"),
                        }
                        content_item["dynamic_zone"].append(component_data)

                elif custom_type == "crop_type":
                    content_item = {
                        "page_title": item.get("page_title"),
                        "publish_at": item.get("publish_at"),
                        "cover_image": item.get("cover_image"),
                        "custom_type": custom_type,
                        "publishedAt": item.get("publishedAt"),
                        "title_audio": item.get("title_audio"),
                        "dynamic_zone": []
                    }

                    for component in item.get("dynamic_zone", []):
                        component_data = {
                            "id": component.get("id"),
                            "name": component.get("name"),
                            "label": component.get("label"),
                            "enabled": component.get("enabled"),
                            "hs_code": component.get("hs_code"),
                            "cpc_code": component.get("cpc_code"),
                            "hs07_code": component.get("hs07_code"),
                            "hs12_code": component.get("hs12_code"),
                            "__component": component.get("__component"),
                            "description": component.get("description"),
                            "helpers_config": component.get("helpers_config"),
                        }
                        content_item["dynamic_zone"].append(component_data)

                
                if content_item:
                    formatted_data[locale].append(content_item)

            self.save_to_database(formatted_data)
            return formatted_data

        except requests.RequestException as e:
            print(f"Error fetching data from Strapi API: {e}")
            return None

    def save_to_database(self, aggregated_data):
        for locale, content_list in aggregated_data.items():
            for content_item in content_list:
                AggregatedContent.objects.create(data=content_item)
        print("Data saved to the database.")
