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
            formatted_data = []
            locale_content = {}
            menu = {} 

            for item in content:
                custom_type = item.get('custom_type')
                locale = item.get('locale')
                print(f"Processing {custom_type}")

                locale_content.setdefault(locale, {})
                if locale not in menu:
                    menu[locale] = []

                if custom_type == "form_questions":
                    content_item = {
                        "pageId": item.get("page_id"),
                        "pageTitle": item.get("page_title"),
                        "lastUpdated": item.get("updatedAt"),
                        "previewTitle": item.get("preview_title"),
                        "formQuestions": [],
                        "additionalText": []
                    }

                    for component in item.get("dynamic_zone", []):
                        if component.get("QuestionType"):
                            component_data = {
                                "key": component.get("Key"),
                                "label": component.get("Label"),
                                "options": component.get("Options") or [],
                                "category": component.get("Category"),
                                "helpText": component.get("HelpText"),
                                "required": component.get("Required"),
                                "placeholder": component.get("Placeholder"),
                                "questionType": component.get("QuestionType"),
                                "displayQuestion": component.get("DisplayQuestion"),
                            }
                            content_item["formQuestions"].append(component_data)

                        if "repeatable_zone" in component:
                            for repeatable_item in component["repeatable_zone"]:
                                repeatable_data = {
                                    "key": repeatable_item.get('key'),
                                    "value": repeatable_item.get('value'),
                                }
                                content_item["additionalText"].append(repeatable_data)

                    locale_content[locale][item.get("page_id")] = content_item

                elif custom_type == "menu_content":
                    menu_item = {
                        "data": [],
                    }

                    for component in item.get("dynamic_zone", []):
                        if component.get("__component") == "okolabor.menu-content":
                            menu_component = {
                                "url": component.get("Url"),
                                "icon": component.get("Icon"),
                                "label": component.get("Label(Translate)"),
                                "order": component.get("Order"),
                                "title": component.get("Title"),
                                "enabled": component.get("Enabled"),
                                
                            }
                            menu_item["data"].append(menu_component)

                    menu[locale].append(menu_item)

            for item in content:
                formatted_data.append({
                    "id": item.get("id"),
                    "deleted": False,
                    "createdAt": item.get("createdAt"),
                    "updatedAt": item.get("updatedAt"),
                    "deletedAt": item.get("deletedAt"),
                    "createdBy": item.get("createdBy"),
                    "updatedBy": item.get("updatedBy"),
                    "deletedBy": item.get("deletedBy"),
                    "content": locale_content,
                    "menu": menu
                })

            self.save_to_database(formatted_data)
            return formatted_data

        except requests.RequestException as e:
            print(f"Error fetching data from Strapi API: {e}")
            return None

    def save_to_database(self, aggregated_data):
        for data_item in aggregated_data:
            for locale, content in data_item["content"].items():
                for content_item in content.values():
                    AggregatedContent.objects.create(
                        data=content_item
                    )
        print("Data saved to the database.")
