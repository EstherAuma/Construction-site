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

    def camel_case(self, snake_str):
        """Convert snake_case string to camelCase."""
        components = snake_str.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])

    def get_content(self):
        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            content = data.get('data', [])

            formatted_data = []

            for item in content:
                custom_type = item.get('custom_type')
                locale = item.get('locale')  
                print(f"Processing {custom_type}")

                if custom_type == "form_questions":
                    content_item = {
                        "id": item.get("id"),
                        "theme": item.get("theme"),
                        "locale": locale,
                        "pageId": item.get("page_id"),
                        "createdAt": item.get("createdAt"),
                        "updatedAt": item.get("updatedAt"),
                        "pageTitle": item.get("page_title"),
                        "publishedAt": item.get("published_at"),
                        "customType": custom_type,
                        "dynamicZone": {}
                    }

                    for component in item.get("dynamic_zone", []):
                        component_data = {
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
                            "repeatableZoneItems": {}  
                        }

                        if "repeatable_zone" in component:
                            for repeatable_item in component["repeatable_zone"]:
                                repeatable_data = {
                                    "key": repeatable_item.get('key'),
                                    "value": repeatable_item.get('value')
                                }
                                component_data["repeatableZoneItems"][repeatable_item.get("id")] = repeatable_data

                        content_item["dynamicZone"][component.get("id")] = component_data

                    formatted_data.append(content_item)

            self.save_to_database(formatted_data)
            return formatted_data

        except requests.RequestException as e:
            print(f"Error fetching data from Strapi API: {e}")
            return None

    def save_to_database(self, aggregated_data):
        for content_item in aggregated_data:
            
            AggregatedContent.objects.create(
                data=content_item  
            )
        print("Data saved to the database.")
