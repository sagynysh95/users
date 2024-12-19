from minio import Minio
from core.config import settings

minio_client = Minio(endpoint=settings.MINIO_ENDPOINT,
                     access_key=settings.MINIO_ACCESS_KEY,
                     secret_key=settings.MINIO_SECRET_KEY,
                     secure=False
                     )

def upload_photo_minio(name, surname, iin):
    file = "photos/2024-12-18T14:06:53.092810.png"
    b_name = "employees"

    if not minio_client.bucket_exists(bucket_name=b_name):
        try:
            minio_client.make_bucket(b_name)
            print("Создали бакет")
        except Exception as e:
            print(f"Ошибка при создании бакета: {e}")

    obj_name = f"{name}-{surname}-{iin}.png"
    try:
        minio_client.fput_object(b_name, obj_name, file)
    except:
        print("Не получилось загрузить фото")

    return f"http://localhost:9000/{b_name}/{obj_name}"
