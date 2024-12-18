from minio import Minio

minio_client = Minio("minio:9000",
                     access_key="admin",
                     secret_key="admin123",
                     secure=False
                     )

def upload_photo_minio(name, surname, iin):
    file = "photos/2024-12-18T14:06:53.092810.png"
    b_name = "employees-bucket"
    # with open(file, 'rb') as file:
    #     file = file.read()
    print("Прочитали файл")


    if not minio_client.bucket_exists(bucket_name=b_name):
        try:
            print("Внутри try")
            minio_client.make_bucket(b_name)
            print("Создали бакет")
        except Exception as e:
            print(f"Ошибка при создании бакета: {e}")

    obj_name = f"{name}-{surname}-{iin}.png"
    try:
        minio_client.fput_object(b_name, obj_name, file)
        print("Вставили фото в минИО")
    except:
        print("Не получилось загрузить фото")
    return minio_client.presigned_get_object(b_name, obj_name)

# upload_photo_minio("sag", "zhak", "87047")

# http://172.18.0.4:9000 
