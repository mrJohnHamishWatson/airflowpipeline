import uuid
from dataclasses import dataclass

"""1. Заголовок изображения
2. Описание изображения
3. Ключевые слова 
4. Категории
5. Дата публикации
6. Оценки и отзывы.
7. Размер и разрешение отображения
8. Автор изображения
9. Ссылки на связанные изображения
10. Расположение изображения (геотеги)
11. Информация о цвете или фоне изображения
12. Статистика просмотров"""


@dataclass(frozen=True)
class ImageModel:
    source: str
    sub_source: str  # Subreddit in case reddit, channel in case Telegram, etc
    url: str
    caption: str
    file_name: str

    # file_name: Optional[str] = None

    def to_json(self):
        return {"source": self.source,
                "sub_source": self.sub_source,
                "url": self.url,
                "caption": self.caption,
                "file_name": self.file_name}

    @staticmethod
    def photo_prefix():
        return uuid.uuid4().hex

    @staticmethod
    def get_name(source, sub_source, photo_prefix):
        return f"{source}-{sub_source}-{photo_prefix}.png"
